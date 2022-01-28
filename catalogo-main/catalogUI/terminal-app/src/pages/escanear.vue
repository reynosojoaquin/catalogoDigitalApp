<template>
  <q-page padding>
   <q-card>
      <q-card-section>
        <span class="text-h4 q-mr-lg ">Total</span>
        <span class="text-h2 ">27.00</span>
      </q-card-section>
    </q-card>
    <q-card bordered class="q-mt-sm jugada-container" >
      <q-card-section>
        <q-banner dense class="bg-primary text-white">
          <div class="row">
            <div class="text-h6 text-weight-bold   column col-4">
              <span>12</span>
              <span>Quiniela</span>
              <span>NA-T</span>
            </div>
            <div class="column flex flex-center col-4"><span class="text-h3">25.0</span></div>
            <div class=" flex flex-center column col-4">
              <q-btn size="30px" flat icon="fas fa-trash-alt" />
            </div>
          </div>
        </q-banner>
      </q-card-section>
    </q-card>
     <q-card  class="q-mt-sm q-pa-sm bg-yellow-1">
      <div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Total General</p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$664.00</p></div>
            </div>
      </div>
      <div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Pagado</p></div>
            </div>
             <div class="column col-4 item-end  ">
              <div class="col"><p class="float-right text-negative text-h4">NO</p></div>
            </div>
      </div><div class="row ">
            <div class="column text-h6 col-4">
              <div class="col"><p>Ganador</p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h4 text-green-10 ">NO</p></div>
            </div>
          </div>
          <div class="row ">
            <div class="column text-h6 col-5">
              <div class="col"><p>Monto Ganado</p></div>
            </div>
             <div class="column col-4 item-end">
              <div class="col"><p class="float-right text-h6">$5000.00</p></div>
            </div>
      </div>
    </q-card>
    <q-page-sticky position="bottom-right" :offset="[14, 120]">
        <q-fab color="purple" icon="keyboard_arrow_up" direction="up">
          <q-fab-action color="primary"  icon="qr_code_scanner" />
          <q-fab-action color="secondary"  icon="far fa-file" />
        <q-fab-action color="primary"  icon="fas fa-ban" />
        <q-fab-action color="secondary"  icon="local_atm" />
      </q-fab>
    </q-page-sticky>
  </q-page>
</template>

<script>
export default {
  name: 'jugada'
}
</script>
