set -e

echo "[init] restoring redash postgres db from /backups/redash.dump (if exists)"
if [ -f /backups/redash.dump ]; then
  echo "[init] ensuring database 'redash' exists"
  psql -U "$POSTGRES_USER" -d "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname='redash'" | grep -q 1 \
    || createdb -U "$POSTGRES_USER" "redash"

  pg_restore -U "$POSTGRES_USER" -d "redash" --clean --if-exists /backups/redash.dump
  echo "[init] redash db restore done"
else
  echo "[init] /backups/redash.dump not found, skipping"
fi