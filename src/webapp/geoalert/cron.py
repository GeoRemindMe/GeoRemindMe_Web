#coding=utf-8


from georemindme.cron import cron_required

from models import Suggestion


@cron_required
def cron_suggestions(request, cursor):
   pass