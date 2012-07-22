# Create your views here.


def people_aggregate(request):
    people = Person.objects.raw("""
        select id, name,
          (select count(id) from cat_museumobject where donor_id = parties_person.id) as donated_count,
          (select count(id) from cat_museumobject where collector_id = parties_person.id) as collected_count,
          (select count(id) from parties_person_related_documents where person_id = parties_person.id) as documents_count
        from parties_person
        """)