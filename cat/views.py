# Create your views here.

import django_tables2 as tables
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django_tables2 import RequestConfig
from models import MuseumObject

def index(request):
    return HttpResponse("Hello, world. You're at the catalogue index.")


class SimpleTable(tables.Table):
    class Meta:
        model = MuseumObject
        attrs = {'class': 'paleblue'}

def table(request):
    queryset = MuseumObject.objects.all()
    table = SimpleTable(queryset)
    RequestConfig(request, paginate={"per_page": 4}).configure(table)
    return render_to_response("simple_list.html", {"table": table},
                              context_instance=RequestContext(request))

def detail(request, artefact_id):
    a = get_object_or_404(MuseumObject, pk=artefact_id)
#    try:
#        a = MuseumObject.objects.get(pk=artefact_id)
#    except MuseumObject.DoesNotExist:
#        raise Http404
    return render_to_response('detail.html', {'artefact': a})
