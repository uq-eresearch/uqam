from views import find_location
from django.views.decorators.http import require_POST
from models import GlobalRegion
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from exceptions import MoveElementException


def jstree(request):
    global_regions = GlobalRegion.objects.all()
    return render(request, "location/jstree.html",
        {'global_regions': global_regions,
         'title': "Geo-locations"})


@require_POST
def move_element(request):
    el_type, el_id = request.POST['obj'].split('-')
    np_type, np_id = request.POST['new-parent'].split('-')
    process_element_move(el_type, el_id, np_type, np_id)

    return HttpResponse('{"success": true}', mimetype="application/json")


def process_element_move(type, id, np_type, np_id):
#    import ipdb; ipdb.set_trace()
    element = find_location(type, id)
    element.parent_id = np_id
    element.save()

    field_changes = calc_field_changes(element, np_id)
    element.museumobject_set.update(**field_changes)
    return


def calc_field_changes(element, np_id):
    """Walk up the tree of geo-locations, finding the new parents

    These will be set onto all the museumobjects.
    """
    fieldname = element._meta.concrete_model.museumobject_set.\
            related.field.name
    field_changes = {}
    field_changes[fieldname] = element.id
    if hasattr(element, 'parent'):
        field_changes.update(
            calc_field_changes(element.parent, element.parent.id))
    return field_changes


@require_POST
def rename_element(request):
    el_type, el_id = request.POST['obj'].split('-')
    new_name = request.POST['new-name']
    element = find_location(el_type, el_id)
    element.name = new_name
    element.save()
    return HttpResponse('success')


from django.template.defaultfilters import slugify


@require_POST
def create_element(request):
    name = request.POST['name']
    model_type = request.POST['type']
    p_type, p_id = request.POST['parent'].split('-')
    parent = find_location(p_type, p_id)
    location_model = ContentType.objects.get(app_label='location',
        model=model_type)

    new_location = location_model.model_class()()
    new_location.name = name
    new_location.parent = parent
    new_location.slug = slugify(name)
    new_location.save()

    return HttpResponse('success')


@require_POST
def delete_element(request):
    el_type, el_id = request.POST['obj'].split('-')
    element = find_location(el_type, el_id)
    element.delete()

    return HttpResponse('success')
