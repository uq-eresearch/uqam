from django.db import models


class Report(models.Model):
    name = models.CharField("Report Name", max_length=40, unique=True)
    description = models.TextField(blank=True)
    raw_sql = models.TextField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('view_report', [str(self.id)])
