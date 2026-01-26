set -e

echo "[init] restoring main postgres db from /backups/postgres.dump (if exists)"
if [ -f /backups/postgres.dump ]; then
  pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists /backups/postgres.dump
  echo "[init] main db restore done"
else
  echo "[init] /backups/postgres.dump not found, skipping"
fi