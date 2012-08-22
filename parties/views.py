from django.shortcuts import render
from parties.models import Person


def people_aggregate(request, template_name='parties/datatables.html'):
    people = Person.objects.raw("""
        select id, display_name,
          (select count(id) from cat_museumobject where donor_id = parties_person.id) as donated_count,
          (select count(id) from cat_museumobject where collector_id = parties_person.id) as collected_count,
          (select count(id) from parties_person_related_documents where person_id = parties_person.id) as documents_count
        from parties_person
        """)
    return render(request, template_name,
            {'person_list': people})
