from django.db.models.signals import post_syncdb
from django.db import connection
from django.conf import settings
import reports.models


def setup_readonly_access(verbosity, **kwargs):
    ro_db = settings.RO_DATABASE

    if verbosity >= 2:
        print "Granting read-only user persmissions"

    if ro_db in settings.DATABASES:
        ro_user = settings.DATABASES[ro_db]['USER']
        cursor = connection.cursor()
        query = "GRANT USAGE ON SCHEMA public TO {0};".format(ro_user)
        cursor.execute(query)

        query = """
        SELECT 'GRANT SELECT ON ' || relname || ' TO {0};'
        FROM pg_class
        JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
        WHERE nspname = 'public' AND relkind IN ('r', 'v')
        """.format(ro_user)

        cursor.execute(query)
        results = cursor.fetchall()
        grant_tables = "".join([s[0] for s in results])
        cursor.execute(grant_tables)

post_syncdb.connect(setup_readonly_access, sender=reports.models)
