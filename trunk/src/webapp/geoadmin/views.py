# coding=utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.


"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from utils import *
from decorators import admin_required
import modelsAdmin

@admin_required
def index(request):
    models = {}
    try:
        for k,v in modelsAdmin._models.iteritems():
            models[str(k)] = v.description
    except NameError:
        pass
    
    return render_to_response('admin/index.html', {'models': models, 'stats': datastore_stats()}, context_instance=RequestContext(request))

@admin_required
def list(request, model):
    amodel = modelsAdmin.getAdminModel(model)
    list = amodel.list()
    
    return render_to_response('admin/list.html', {'adminmodel' : amodel.model.__name__, 'models': list, 'header':amodel.header_list, 'stats': datastore_stats(model=amodel.model.__name__)}, context_instance=RequestContext(request))
 
@admin_required
def edit(request, model, key):
    amodel = modelsAdmin.getAdminModel(model)
    instance = amodel.get(key=key)
    if request.method == 'POST':
        f = amodel.form(request.POST, prefix='admin_form')
        if f.is_valid():
            f.save()
            return HttpResponseRedirect('/admin/list/%s' % amodel.model.__name__)
    else:
        f = amodel.form(initial=instance, prefix='admin_form')
        
    return render_to_response('admin/edit.html', {'adminmodel': amodel.model.__name__, 'form':f, }, context_instance=RequestContext(request))
    
    