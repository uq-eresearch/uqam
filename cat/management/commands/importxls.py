from django.core.management.base import BaseCommand, CommandError
from cat.models import MuseumObject, FunctionalCategory, ArtefactType, CulturalBloc
from cat.models import Person, Place
from django.core import management
from django.db import transaction
from django import db

import csv
import sys
import os
import string

from openpyxl.reader.excel import load_workbook

def import_xlsx(filename):
    wb = load_workbook(filename = filename)
    sheet = wb.get_sheet_by_name(name = 'Sheet1')
    sheet.get_highest_column()
    sheet.get_highest_row()
    sheet.cell(row=1, column=1)
    data = sheet.range(sheet.calculate_dimension())
    headers = [v.value for v in data[0]]
    for row in data[1:]:
        vals = [str(v.value).strip() for v in row]
        m = MuseumObject()
        m.id = vals[0]
        m.old_registration_number = vals[1]
        m.other_number = vals[2]
        m.functional_category = vals[3] ####
        m.Artefact_type = vals[4] ####
        m.storage_section = vals[5]
        m.storage_unit = vals[6]
        m.storage_bay = vals[7]
        m.storage_shelf_box_drawer = vals[8]
        m.acquisition_date = vals[9] ####
        m.access_status = vals[10]
        m.description = vals[11]
        m.comment = vals[12]
        region = vals[13]
        state = vals[14]
        m.acquisition_method = vals[15]
        m.loan_status = vals[16]
        country = vals[17]
        place = vals[18]
        cultural_bloc = vals[19]
        photographic_record = vals[20]
        collector = vals[21]
        when_obtained = vals[22]
        how_obtained = vals[23]
        source = vals[24]
        when_obtained = vals[25]
# All empty       how_obtained = vals[26]
# All empty       category_illustration = vals[27]
# All empty       artefaction_illustration = vals[28]
        raw_material = vals[29]
        indigenous_name = vals[30]
        associated_group = vals[31]
        recorded_use = vals[32]
        maker_artist = vals[33]
        m.length = vals[34]
        m.width = vals[35]
        m.depth = vals[36]
        m.circumference = vals[37]
        m.weight = vals[38]




class Command(BaseCommand):
    help = "Import artefact records from xlsx"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("need exactly one argument for xlsx file")

        filename, = args

        import_xlsx(filename)


