# coding=utf-8


import itertools
import datetime
from os import environ
from google.appengine.ext import deferred
from google.appengine.ext import db
from google.appengine.api import taskqueue
from django import template
from django.http import HttpResponseBadRequest, HttpResponse
from geoalert.models import Suggestion
from geoalert.models_poi import Place
from geouser.models import User
from georemindme.cron import cron_required


class Sitemap(db.Model):
    body = db.BlobProperty()
    content_type = db.StringProperty(required=True, default='application/xml')
    last_modified = db.DateTimeProperty(auto_now=True)
    
    @classmethod
    def get(self, path):
        return Sitemap.get_by_key_name(path)
    
    @classmethod
    def set(self, path, body, content_type='application/xml'):
        sitemap = Sitemap.get_by_key_name(path)
        if sitemap is not None:
            sitemap.body = str(body)
        else:
            sitemap = Sitemap(key_name=path, 
                          body=str(body), 
                          content_type=content_type
                          )
        sitemap.put()
        

def _render_sitemap(template_name, template_vals=None, template_num=0):
    """
        Renderiza una plantilla sitemap.xml
    """
    try:
        tpl = template.loader.get_template(template_name)
        rendered = tpl.render(template.Context(template_vals))
        Sitemap.set('%d%s' % (template_num, template_name), rendered, 'application/xml')
        return rendered
    except:
        return None
    
def chunker(iterable, chunksize):
    """
    Return elements from the iterable in `chunksize`-ed lists. The last returned
    chunk may be smaller (if length of collection is not divisible by `chunksize`).

    >>> print list(chunker(xrange(10), 3))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    i = iter(iterable)
    while True:
        wrapped_chunk = [list(itertools.islice(i, int(chunksize)))]
        if not wrapped_chunk[0]:
            break
        yield wrapped_chunk.pop()

    

def _get_all_suggs(cursor = None):
    """
        Obtiene las urls de las sugerencias
    """
    keys = []
    if cursor is None:
        suggs = Suggestion.all().filter('_vis =', 'public').fetch(500)
        keys.extend(suggs)
    else:
        suggs = Suggestion.all().filter('_vis =', 'public').with_cursor(cursor).fetch(500)
    while len(suggs) == 500:
        keys.extend(suggs)
        q = Suggestion.all().filter('_vis =', 'public').filter('__key__ >', suggs[-1].key())
        suggs = q.fetch(500)
        keys.extend(suggs)
    return [x.get_absolute_url() for x in keys]


def _get_all_places(cursor = None):
    """
        Obtiene las urls de las sugerencias
    """
    keys = []
    if cursor is None:
        places = Place.all().fetch(500)
        keys.extend(places)
    while len(places) == 500:
        keys.extend(places)
        q = Place.all().filter('__key__ >', places[-1].key())
        places = q.fetch(500)
        keys.extend(places)
    return [x.get_absolute_url() for x in keys]


def _get_all_users(cursor = None):
    """
        Obtiene las urls de las sugerencias
    """
    keys = []
    if cursor is None:
        users = User.all().filter('username !=', None).fetch(500)
        keys.extend(users)
    while len(users) == 500:
        keys.extend(users)
        q = User.all().filter('username !=', None).filter('__key__ >', users[-1].key())
        users = q.fetch(500)
        keys.extend(users)
    return [x.get_absolute_url() for x in keys]


def _regenerate_sitemap():
    """
        Crea un nuevo sitemap, ejecutar en defer
    """
    paths = _get_all_suggs() # obtiene todas las sugerencias para el sitemap
    paths.extend(_get_all_places())
    paths.extend(_get_all_users())
    template_num=0
    # aqui pasar cada sublista de 500 elementos a render
    for chunk in chunker(paths, chunksize=1000):
        _render_sitemap(template_name ='sitemap_partial.xml', 
                    template_vals = {'paths': paths, 
                                     'host':environ['HTTP_HOST'],
                                     },
                    template_num=template_num
                   )
        del chunk


@cron_required
def build_sitemap(request):
    # crear sitemap
    try:
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        eta = now.replace(second=0, microsecond=0) + datetime.timedelta(seconds=65)
        _regenerate_sitemap()
        deferred.defer(
                       _regenerate_sitemap)
#                       _queue='sitemap-%s' % (now.strftime('%Y%m%d%H%M')))
#                       _eta=eta)
    except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError), e:
        pass
    return HttpResponse()


def response_sitemap(request, id):
    s = Sitemap.get('%dsitemap_partial.xml' % int(id))
    if s is not None:
        return HttpResponse(s.body, mimetype='application/xml')
    else:
        response = _render_sitemap('sitemap_partial.xml', 
                        {'paths': [], 
                     'host':environ['HTTP_HOST'],
                     
                    },
                    template_num=int(id)
                   )
        return HttpResponse(response, mimetype='application/xml')


def main_sitemap(request):
    ids = Sitemap.all().count()
    if ids == 0:
        return HttpResponse()
    tpl = template.loader.get_template('sitemap.xml')
    rendered = tpl.render(template.Context({'host':environ['HTTP_HOST'],
                                            'path': 'sitemap/',
                                            'ids': range(ids)
                                            }))
    return HttpResponse(rendered, mimetype='application/xml')