from django.shortcuts import render
from parties.models import Person
from django.shortcuts import get_object_or_404


def people_aggregate(request, template_name='parties/datatables.html'):
    people = Person.objects.raw("""
        select id, display_name,
          (select count(id) from cat_museumobject where donor_id = parties_person.id) as donated_count,
          (select count(id) from cat_museumobject where collector_id = parties_person.id) as collected_count,
          (select count(id) from cat_museumobject where maker_id = parties_person.id) as created_count,
          (select count(id) from parties_person_related_documents where person_id = parties_person.id) as documents_count
        from parties_person
        """)
    return render(request, template_name,
            {'person_list': people})


def person_detail(request, pk, item_type='docs', template_name='parties/person_detail.html'):

    person = get_object_or_404(Person, pk=int(pk))

    if item_type == 'docs':
        items = person.related_documents.all()
    elif item_type == 'created':
        items = person.created_items.all()
    elif item_type == 'collected':
        items = person.collected_objects.all()
    elif item_type == 'donated':
        items = person.donated_objects.all()
    else:
        items = []

    counts = []
    counts.append(('docs', 'Related documents', person.related_documents.count()))
    counts.append(('created', 'Created items', person.created_items.count()))
    counts.append(('collected', 'Collected items', person.collected_objects.count()))
    counts.append(('donated', 'Donated items', person.donated_objects.count()))

    return render(request, template_name, {
        'person': person,
        'items': items,
        'counts': counts,
        'item_type': item_type
        })


def person_objects(request):
    pass
