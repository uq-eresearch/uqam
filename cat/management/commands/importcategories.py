from django.core.management.base import BaseCommand, CommandError
from cat.models import Category

from openpyxl.reader.excel import load_workbook

def import_categories(filename):
    wb = load_workbook(filename = filename)
    categories_sheet = wb.get_sheet_by_name(name = 'Categories')

    _import_sheet(categories_sheet, skip=("Equipment",))

    equipment_sheet = wb.get_sheet_by_name(name="Equipment")
    equipment = Category(name="Equipment")
    equipment.save()
    _import_sheet(equipment_sheet, parent=equipment)


def _import_sheet(sheet, skip=(), parent=None):
    for column in sheet.columns:
        title = column[0].value
        if title in skip:
            continue
        print title
        toplevel = Category(name=title)
        toplevel.parent = parent
        toplevel.save()
        for cell in column[1:]:
            if cell.value is None:
                break
            print "  ", cell.value
            cat = Category(name=cell.value)
            cat.parent = toplevel
            cat.save()
            
class Command(BaseCommand):
    help = "Import categories from xlsx"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("need exactly one argument for categories xlsx file")

        filename, = args

        import_categories(filename)


