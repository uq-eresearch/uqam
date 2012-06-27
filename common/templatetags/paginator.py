#  Based on: http://www.djangosnippets.org/snippets/73/
#
#  Modified by Sean Reifschneider to be smarter about surrounding page
#  link context.  For usage documentation see:
#
#     http://www.tummy.com/Community/Articles/django-pagination/

from django import template

register = template.Library()


def paginator(context, adjacent_pages=2):
    """
    To be used with a Django paginator.

    Must be stored in the context, as either 'objects', or 'page'.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    objects = context.get('objects') or context.get('page')
    paginator = objects.paginator

    startPage = max(objects.number - adjacent_pages, 1)
    if startPage <= 3:
        startPage = 1
    endPage = objects.number + adjacent_pages + 1
    if endPage >= paginator.num_pages - 1:
        endPage = paginator.num_pages + 1
    page_numbers = [n for n in range(startPage, endPage) \
            if n > 0 and n <= paginator.num_pages]

    query = context.get('query', '')
    if query != '':
        query = "&q=" + query

    return {
        'query': query,
        'objects': objects,
        'page': objects.number,
#        'pages': paginator.num_pages,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)
