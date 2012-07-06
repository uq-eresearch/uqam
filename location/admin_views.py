from views import find_location
from django.views.decorators.http import require_POST
from models import GlobalRegion
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
import logging

logger = logging.getLogger(__name__)


def jstree(request):
    global_regions = GlobalRegion.objects.all()
    return render(request, "location/jstree.html",
        {'global_regions': global_regions,
         'title': "Geo-locations"})


@require_POST
def move_element(request):
    el_type, el_id = request.POST['obj'].split('-')
    np_type, np_id = request.POST['new-parent'].split('-')
    try:
        process_element_move(el_type, el_id, np_type, np_id)
    except IntegrityError:
        # Return 409 Conflict
        logger.warn('Error moving location. Already exists.')
        return HttpResponse('A location by that name already exists', status=409)

    return HttpResponse('{"success": true}', mimetype="application/json")


def process_element_move(type, id, np_type, np_id):
    element = find_location(type, id)

    element.parent_id = np_id
    element.save()

    field_changes = calc_field_changes(element, np_id)
    element.museumobject_set.update(**field_changes)
    return


def perform_move(new_parent, element):
    if hasattr(element, 'children') and \
      element.children.exists():
        for child in element.children():
            matches = new_parent.children.filter(slug=child.slug)
            if matches:
                # need to merge
                pass
            else:
                child.parent_id = new_parent.id
                child.save()
            pass

    else:
        element.parent_id = new_parent.id
        element.save()



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
    try:
        element.save()
    except IntegrityError:
        # Return 409 Conflict
        logger.warn('Error renaming location: %s', element)
        return HttpResponse('A location by that name already exists', status=409)

    return HttpResponse('success')


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
    try:
        new_location.save()
    except IntegrityError:
        # Return 409 Conflict
        logger.warn('Error creating location: %s', new_location)
        return HttpResponse('A location by that name already exists', status=409)

    return HttpResponse('success')


@require_POST
def delete_element(request):
    el_type, el_id = request.POST['obj'].split('-')
    element = find_location(el_type, el_id)
    try:
        element.delete()
    except ProtectedError:
        # Return 409 Conflict
        logger.warn('Error deleting location: %s', element)
        return HttpResponse("Unable to delete.", status=409)

    return HttpResponse('success')
