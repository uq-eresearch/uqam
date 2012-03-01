#!/bin/bash
 
DEST=$1
MAX=$2
DB=$3
FILES=$4
 
if ! [ -d "$DEST" -a -w "$DEST" -a -n "$MAX" -a -n "$DB" -a -n "$FILES" ]; then
  echo "Usage: $(dirname $0) DEST MAX DB FILES"
  echo "DEST is the directory to write the backup to (must exist and be writable)"
  echo "MAX is the maximum number of backups to keep (old ones are deleted)"
  echo "DB is the name of PostgreSQL database (assumes user root with no password)"
  echo "FILES is a space-separated list of file and/or directory paths to be backed-up"
  exit 1
fi
 
TIMESTAMP=$(date '+%Y%m%d%H%M%S')
DB_BACKUP="$DEST/backup-$TIMESTAMP.sql.bz2"
FS_BACKUP="$DEST/backup-$TIMESTAMP.tar.bz2"
 
su -l -c "pg_dump $DB" postgres | bzip2 -c > $DB_BACKUP
 
tar -c -j -f $FS_BACKUP -P -C / $FILES
 
VICTIMS="$(ls -1 $DEST/backup-*.sql.bz2 | head -n-$MAX) $(ls -1 $DEST/backup-*.tar.bz2 | head -n-$MAX)"
for VICTIM in $VICTIMS; do
  rm $VICTIM
done
