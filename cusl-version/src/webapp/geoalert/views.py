# coding=utf-8

from models import Alert
from geouser.decorators import login_required

#===============================================================================
# FUNCIONES PARA AÑADIR, EDITAR, OBTENER Y MODIFICAR ALERTAS
#===============================================================================
@login_required
def add_alert(request, form, address):
    alert = form.save(user = request.session['user'], address = address)
    return alert

@login_required
def edit_alert(request, id, form, address):
    alert = form.save(user = request.session['user'], address = address, id = id)
    return alert

@login_required
def get_alert(request, id, done = None, page = 1, query_id = None):
    if id:
        return [Alert.objects.get_by_id_user(id, request.session['user'])]
    if done is None:
        return Alert.objects.get_by_user(request.session['user'], page, query_id)
    if done:
        return Alert.objects.get_by_user_done(request.session['user'], page, query_id)
    else:
        return Alert.objects.get_by_user_undone(request.session['user'], page, query_id)

@login_required    
def del_alert(request, id = None):
    if id is None:
        raise AttributeError()
    alert = Alert.objects.get_by_id_user(int(id), request.session['user'])
    if not alert:
            raise AttributeError()
    alert.delete()    
    return True