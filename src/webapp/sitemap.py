# coding=utf-8


import datetime
from os import environ
from google.appengine.ext import deferred
from google.appengine.ext import db
from google.appengine.api import taskqueue
from django import template
from django.http import HttpResponseBadRequest, HttpResponse
from geoalert.models import Suggestion
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
        return HttpResponseBadRequest()
    

def _get_all_paths(cursor = None):
    """
        Obtiene las urls de las sugerencias
    """
    keys = []
    if cursor is None:
        suggs = Suggestion.all().filter('_vis =', 'public').fetch(500)
        keys.extend(suggs)
    while len(suggs) == 500:
        keys.extend(suggs)
        q = Suggestion.all().filter('_vis =', 'public').filter('__key__ >', suggs[-1])
        suggs = q.fetch(500)
        keys.extend(suggs)
    return [x.get_absolute_url() for x in keys]


def _regenerate_sitemap():
    """
        Crea un nuevo sitemap, ejecutar en defer
    """
    paths = _get_all_paths() # obtiene todas las sugerencias para el sitemap
    template_num=0
    # aqui pasar cada sublista de 500 elementos a render
    _render_sitemap('sitemap_partial.xml', 
                    {'paths': paths, 
                     'host':environ['HTTP_HOST'],
                     
                    },
                    template_num=template_num
                   )


@cron_required
def build_sitemap(request):
    # crear sitemap
    try:
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        eta = now.replace(second=0, microsecond=0) + datetime.timedelta(seconds=65)
        _regenerate_sitemap()
        #deferred.defer(
        #               _regenerate_sitemap,
        #               _name='sitemap-%s' % (now.strftime('%Y%m%d%H%M'),),
        #               _eta=eta)
    except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError), e:
        pass
    return HttpResponse()


def response_sitemap(request, id):
    s = Sitemap.get('%dsitemap.xml' % int(id))
    return HttpResponse(s.body, mimetype='application/xml')


def main_sitemap(request):
    ids = Sitemap.all().count()
    tpl = template.loader.get_template('sitemap.xml')
    rendered = tpl.render(template.Context({'host':environ['HTTP_HOST'],
                                            'path': 'sitemap/',
                                            'ids': range(ids)
                                            }))
    return HttpResponse(rendered, mimetype='application/xml')