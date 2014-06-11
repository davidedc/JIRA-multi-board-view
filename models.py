from django.db import models

class BoardDefinition(models.Model):
    name = models.CharField('board name', max_length=128)
    jql = models.CharField("JQL for board", max_length=1024,
        help_text="")
    statuses = models.CharField('Statuses', max_length=2048,
        help_text='Comma separated names of statuses')

    def __unicode__(self):
        return unicode(self.name) + " (" + self.statuses + ")"

class EpicDefinition(models.Model):
    name = models.CharField('epic name', max_length=128)
    jql = models.CharField("JQL for Epic", max_length=2048,
        help_text="Simplest form can look like 'Epic Link' = XXX-001")

    def __unicode__(self):
        return unicode(self.name) + " (" + self.jql + ")"
