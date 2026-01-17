set -e

echo "[init] restoring redash postgres db from /backups/redash.dump (if exists)"
if [ -f /backups/redash.dump ]; then
  pg_restore -U "redash" -d "redash" --clean --if-exists /backups/redash.dump
  echo "[init] redash db restore done"
else
  echo "[init] /backups/redash.dump not found, skipping"
fi