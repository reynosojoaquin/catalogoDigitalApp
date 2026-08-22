import hashlib
import json
from dataclasses import dataclass
from decimal import Decimal

from django.db import IntegrityError, transaction

from audit.models import AuditEvent
from payments.models import CommissionMovement

from .models import CommissionSettlement, CommissionSettlementItem


class SettlementConflictError(Exception):
    pass


@dataclass(frozen=True)
class SettlementResult:
    settlement: CommissionSettlement
    created: bool


def request_fingerprint(*, settlement_id, seller_id, period_ends_at, confirmed_at):
    payload = {
        "settlement_id": str(settlement_id),
        "seller_id": str(seller_id),
        "period_ends_at": period_ends_at.isoformat(),
        "confirmed_at": confirmed_at.isoformat(),
    }
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


@transaction.atomic
def confirm_settlement(
    *, actor, settlement_id, seller_id, period_ends_at, confirmed_at,
    idempotency_key, correlation_id,
):
    request_hash = request_fingerprint(
        settlement_id=settlement_id,
        seller_id=seller_id,
        period_ends_at=period_ends_at,
        confirmed_at=confirmed_at,
    )
    existing = CommissionSettlement.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        if existing.request_hash != request_hash:
            raise SettlementConflictError
        AuditEvent.objects.create(
            actor=actor,
            action="commission_settlement.idempotent_replay",
            resource_type="commission_settlement",
            resource_id=str(existing.id),
            result=AuditEvent.Result.SUCCESS,
            source="web",
            correlation_id=correlation_id,
        )
        return SettlementResult(existing, False)

    movements = list(
        CommissionMovement.objects.select_for_update()
        .filter(
            seller_id=seller_id,
            status=CommissionMovement.Status.AVAILABLE,
            created_at__lte=period_ends_at,
        )
        .order_by("created_at", "id")
    )
    if not movements:
        raise SettlementConflictError

    signed_amounts = [
        movement.amount
        if movement.movement_type == CommissionMovement.MovementType.CREDIT
        else -movement.amount
        for movement in movements
    ]
    total = sum(signed_amounts, Decimal("0.00"))
    if total <= Decimal("0.00"):
        raise SettlementConflictError

    try:
        with transaction.atomic():
            settlement = CommissionSettlement.objects.create(
                id=settlement_id,
                seller_id=seller_id,
                confirmed_by=actor,
                period_ends_at=period_ends_at,
                total=total,
                idempotency_key=idempotency_key,
                request_hash=request_hash,
                confirmed_at=confirmed_at,
            )
            CommissionSettlementItem.objects.bulk_create([
                CommissionSettlementItem(
                    settlement=settlement,
                    movement=movement,
                    movement_type=movement.movement_type,
                    amount=movement.amount,
                    signed_amount=signed_amount,
                )
                for movement, signed_amount in zip(movements, signed_amounts)
            ])
            for movement in movements:
                movement.status = CommissionMovement.Status.SETTLED
                movement.save(update_fields=["status"])
    except IntegrityError as error:
        raise SettlementConflictError from error

    AuditEvent.objects.create(
        actor=actor,
        action="commission_settlement.confirmed",
        resource_type="commission_settlement",
        resource_id=str(settlement.id),
        result=AuditEvent.Result.SUCCESS,
        source="web",
        correlation_id=correlation_id,
        metadata={"seller_id": str(seller_id), "movement_count": len(movements)},
    )
    return SettlementResult(settlement, True)
