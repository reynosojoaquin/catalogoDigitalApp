#!/bin/sh
set -eu

locale_root="/tmp/catalogo-digital-locale"
for po_file in /app/locale/*/LC_MESSAGES/*.po; do
    [ -f "$po_file" ] || continue
    locale_dir="$locale_root/$(basename "$(dirname "$(dirname "$po_file")")")/LC_MESSAGES"
    mkdir -p "$locale_dir"
    msgfmt "$po_file" -o "$locale_dir/$(basename "${po_file%.po}.mo")"
done

exec "$@"
