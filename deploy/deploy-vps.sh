#!/usr/bin/env bash
# Kirim dasbor XAU ke VPS lewat rsync/SSH — dijalankan dari komputer yang
# SUDAH punya akses SSH ke VPS (bukan dari sesi Claude).
#
#   ./deploy/deploy-vps.sh                       # pakai variabel di bawah / environment
#   VPS_HOST=1.2.3.4 VPS_USER=root ./deploy/deploy-vps.sh
#   ./deploy/deploy-vps.sh --host 1.2.3.4 --user root --path /var/www/xau
set -euo pipefail

VPS_HOST="${VPS_HOST:-}"
VPS_USER="${VPS_USER:-root}"
VPS_PATH="${VPS_PATH:-/var/www/xau}"
VPS_PORT="${VPS_PORT:-22}"
SSH_KEY="${SSH_KEY:-}"

while [ $# -gt 0 ]; do
  case "$1" in
    --host) VPS_HOST="$2"; shift 2 ;;
    --user) VPS_USER="$2"; shift 2 ;;
    --path) VPS_PATH="$2"; shift 2 ;;
    --port) VPS_PORT="$2"; shift 2 ;;
    --key)  SSH_KEY="$2";  shift 2 ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *) echo "Opsi tidak dikenal: $1" >&2; exit 1 ;;
  esac
done

if [ -z "$VPS_HOST" ]; then
  echo "VPS_HOST belum diisi. Contoh: ./deploy/deploy-vps.sh --host 1.2.3.4 --user root" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/dashboard/"
[ -f "$SRC/xau-pipeline.html" ] || { echo "Tidak menemukan dashboard/xau-pipeline.html" >&2; exit 1; }

SSH_OPTS="-p $VPS_PORT"
[ -n "$SSH_KEY" ] && SSH_OPTS="$SSH_OPTS -i $SSH_KEY"

echo "→ Membuat folder $VPS_PATH di $VPS_HOST"
# shellcheck disable=SC2086
ssh $SSH_OPTS "$VPS_USER@$VPS_HOST" "mkdir -p '$VPS_PATH'"

echo "→ Mengirim dashboard/ ke $VPS_USER@$VPS_HOST:$VPS_PATH"
# shellcheck disable=SC2086
rsync -avz --delete -e "ssh $SSH_OPTS" "$SRC" "$VPS_USER@$VPS_HOST:$VPS_PATH/"

echo
echo "Selesai. Isi folder di VPS:"
# shellcheck disable=SC2086
ssh $SSH_OPTS "$VPS_USER@$VPS_HOST" "ls -la '$VPS_PATH'"
echo
echo "Kalau nginx sudah dipasang (lihat deploy/nginx-xau.conf), dasbor ada di:"
echo "  http://$VPS_HOST/           (root menampilkan xau-pipeline.html)"
