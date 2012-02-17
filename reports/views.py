from models import Report
from django.db import connections
from django.shortcuts import render
from django.conf import settings


def view_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    cursor = connections[settings.RO_DATABASE].cursor()
    cursor.execute(report.raw_sql)
    desc = cursor.description
    results = cursor.fetchall()

    return render(request, "reports/basic.html",
            {"report": report, "desc": desc, "results": results})
