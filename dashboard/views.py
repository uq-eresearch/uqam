from django.shortcuts import render
from django.db import connection, transaction


def index(request):
    return render(request, 'dashboard/index.html')


def stats(request):
    '''select count(*)
    from cat_museumobject
    where place_id in (select id from location_place
    where australian_state != ''
    and region !=           ''
    and name != '')'''

    s = '''
    select country, count(*)
    from location_place
    group by country
    order by 2 desc;
    '''

    geocode_dups = '''
    select gn_id, gn_name, count(*)
    from location_place
    group by gn_id, gn_name
    having count(*) > 1
    order by count(*) desc
    '''
    cursor = connection.cursor()

    # Data retrieval operation - no commit required
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

    return row


def duplicate_places(request):
    cursor = connection.cursor()

    cursor.execute("""
        select gn_id, gn_name, count(*)
        from location_place
        group by gn_id, gn_name
        having count(*) > 1
        order by 3 desc
    """)

    results = cursor.fetchall()

    return render(request, {'results': results})

