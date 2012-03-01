#!/bin/sh

# This script will fix up incorrect sequences in postgres
# At the moment hardcoded for host: localhost db: uqam
#
# Based on code from: http://wiki.postgresql.org/wiki/Fixing_Sequences

psql -h localhost -U uqam -Atq <<END_TEXT | psql -h localhost -U uqam
SELECT  'SELECT SETVAL(' ||quote_literal(S.relname)|| ', MAX(' ||quote_ident(C.attname)|| ') ) FROM ' ||quote_ident(T.relname)|| ';'
FROM pg_class AS S, pg_depend AS D, pg_class AS T, pg_attribute AS C
WHERE S.relkind = 'S'
    AND S.oid = D.objid
    AND D.refobjid = T.oid
    AND D.refobjid = C.attrelid
    AND D.refobjsubid = C.attnum
ORDER BY S.relname;
END_TEXT
