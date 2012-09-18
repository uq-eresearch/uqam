from django.shortcuts import render
from parties.models import Person
from django.shortcuts import get_object_or_404
from utils.utils import do_paging


def people_aggregate(request, template_name='parties/datatables.html'):
    people = Person.objects.raw("""
        select id, display_name, name,
          (select count(id) from cat_museumobject where donor_id = parties_person.id and public = true) as donated_count,
          (select count(id) from cat_museumobject where collector_id = parties_person.id and public = true) as collected_count,
          (select count(id) from cat_museumobject where maker_id = parties_person.id and public = true) as created_count,
          (select count(mediaman_document.id) from mediaman_document, parties_person_related_documents where person_id = parties_person.id and mediaman_document.id = document_id and public = true) as documents_count
        from parties_person
        """)
    return render(request, template_name,
            {'person_list': people})


def person_detail(request, pk, item_type='default', template_name='parties/person_detail.html'):

    person = get_object_or_404(Person, pk=int(pk))

    mapping = {'docs': ('related_documents', 'Related documents', person.related_documents.filter(public=True).count()),
               'created': ('created_items', 'Created items', person.created_items.filter(public=True).count()),
               'collected': ('collected_objects', 'Collected items', person.collected_objects.filter(public=True).count()),
               'donated': ('donated_objects', 'Donated items', person.donated_objects.filter(public=True).count())}

    if item_type == 'default':
        # Select max count type
        item_count = -1
        for k, v in mapping.items():
            if v[2] > item_count:
                item_count = v[2]
                item_type = k

    # output types in correct order
    types = [(key, mapping[key][1], mapping[key][2]) for key in ('docs', 'created', 'collected', 'donated')]

    if item_type in mapping.keys():
        items = getattr(person, mapping[item_type][0]).select_related().filter(public=True
            ).prefetch_related('category', 'country', 'global_region', 'artefactrepresentation_set'
            ).extra(
                select={'public_images_count': 'select count(*) from mediaman_artefactrepresentation a WHERE a.artefact_id = cat_museumobject.id'})

    else:
        items = []

    objects = do_paging(request, items)

    related_documents = person.related_documents.filter(public=True)

    return render(request, template_name, {
        'person': person,
        'objects': objects,
        'related_documents': related_documents,
        'types': types,
        'item_type': item_type,
        'item_name': mapping[item_type][1]
        })


def person_objects(request):
    pass
