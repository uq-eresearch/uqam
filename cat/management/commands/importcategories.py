from django.core.management.base import BaseCommand, CommandError
from cat.models import Category
from django.template.defaultfilters import slugify

from openpyxl.reader.excel import load_workbook

def delete_all_categories_sqlite():
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("DELETE FROM `cat_category`")
def delete_all_categories_postgres():
    Category.objects.all().delete()

def import_categories(filename):
#    delete_all_categories()
    delete_all_categories_postgres()
    wb = load_workbook(filename = filename)
    categories_sheet = wb.get_sheet_by_name(name = 'Categories')

    _import_sheet(categories_sheet)#, skip=("Equipment",))

    equipment_sheet = wb.get_sheet_by_name(name="Equipment")
    equipment = Category.objects.get(name="Equipment", parent=None)
    equipment.save()
    _import_sheet(equipment_sheet, parent=equipment)


def _import_sheet(sheet, skip=(), parent=None):
    for column in sheet.columns:
        title = column[0].value.strip()
        if title in skip:
            continue
        title = title.title()
        print title
        toplevel = Category(name=title)
        toplevel.parent = parent
        toplevel.slug = slugify(title)
        toplevel.save()
        for cell in column[1:]:
            leaf_title = cell.value
            if leaf_title is None:
                break
            leaf_title = leaf_title.strip().title()
            print "  ", leaf_title
            cat = Category(name=leaf_title)
            cat.parent = toplevel
            cat.slug = slugify(leaf_title)
            cat.save()
            
class Command(BaseCommand):
    help = "Import categories from xlsx"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("need exactly one argument for categories xlsx file")

        filename, = args

        import_categories(filename)


