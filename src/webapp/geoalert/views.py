# coding=utf-8

"""
.. module:: views
    :platform: appengine
    :synopsis: Views for GeoAlert
"""

from django.http import Http404, HttpResponseServerError
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from models import *
from geouser.decorators import login_required
import memcache


#===============================================================================
# PERFIL DE EVENTOS
#===============================================================================
def suggestion_profile(request, id):
    """
        Devuelve el perfil de una sugerencia, comprueba la
        visibilidad de una funcion
        
            :param id: identificador de la sugerencia
            :type id: :class:`ìnteger`
    """
    user = request.session.get('user', None)
    suggestion = Suggestion.objects.get_by_id(id)
    if suggestion is None:
        raise Http404
    if suggestion._is_private() and suggestion.user != user:
        # sugerencia privada, pero de otro usuario
        raise Http404
    elif suggestion._is_shared() and not suggestion.user_invited(user):
        raise Http404 
    
    return render_to_response('webapp/suggestionprofile.html', {'suggestion':suggestion},
                               context_instance=RequestContext(request))

    
#===============================================================================
# FUNCIONES PARA AÑADIR, EDITAR, OBTENER Y MODIFICAR ALERTAS
#===============================================================================
@login_required
def add_alert(request, form, address):
    """
        Añade una alerta
        
            :param form: formulario con los datos
            :type form: :class:`geoalert.forms.RemindForm`
            :param address: direccion obtenida de la posicion
            :type: :class:`string`
            
            :returns: :class:`geoalert.models.Alert`
    """
    alert = form.save(user = request.session['user'], address = address)
    return alert


@login_required
def edit_alert(request, id, form, address):
    """
        Edita una alerta
        
            :param form: formulario con los datos
            :type id: :class:`geoalert.forms.RemindForm`
            
            :returns: :class:`geoalert.models.Alert`
    """
    alert = form.save(user = request.session['user'], address = address, id = id)
    return alert


@login_required
def get_alert(request, id, done = None, page = 1, query_id = None):
    """
        Obtiene alertas
        
            :param id: identificador de la alerta
            :type id: :class:`integer`
            :param done: devolver solo las realizadas
            :type done: boolean
            :param page: pagina a devolver
            :type page: :class:`ìnteger`
            :param query_id: identificador de la busqueda
            :type query_id: :class:`integer`
            
            :returns: :class:`geoalert.models.Alert`
    """
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
    """
        Borra una alerta
        
            :param id: identificador de la alerta
            :type id: :class:`integer`
            
            :returns: True
            :raises: AttributeError
    """
    if id is None:
        raise AttributeError()
    alert = Alert.objects.get_by_id_user(int(id), request.session['user'])
    if not alert:
            raise AttributeError()
    alert.delete()    
    return True

#===============================================================================
# AÑADIR PLACES
#===============================================================================
def _get_city(components):
    for i in components:
        if 'locality' in i['types']:
            return i['short_name']
            
def search_place(pos, radius=500, types=None, language=None, name=None, sensor=False):
    """
        Busca lugares cercano a la posicion usando la API de Google Places
        
            :param pos: posicion a buscar
            :type pos: :class:`db.GeoPt`
            :param radius: radio a buscar
            :type radius: :class:`integer`
            :param types: lista de tipos de sitios (opcional)
            :type types: list
            :param language: idioma de los resultados (opcional)
            :type language: string
            :param name: Nombre que buscar (opcional)
            :type name: string
            :param sensor: indicar si la posicion se obtiene con GPS, etc.
            :type sensor: boolean
            
            :returns: dict
    """
    def _add_urls_to_results(search):
        gets = list()
        length = len(search['results'])
        for i in xrange(length):
            gets.append(Place.all().filter('google_places_id =', search['results'][i]['id']).run())    
        for i in xrange(length):
            place = gets[i]
            try:
                place = place.next()
                search['results'][i].update({'_url': place.get_absolute_url()})
            except StopIteration:
                # no existe, devolvemos una url 'generica'
                search['results'][i].update({'_url': '/place/gref/%s' % search['results'][i]['reference']})
        return search
    from mapsServices.places.GPRequest import GPRequest
    search = GPRequest().do_search(pos, radius, types, language, name, sensor)
    return _add_urls_to_results(search)

@login_required
def add_from_google_reference(request, reference):
    """
        Añade un lugar a partir de una referencia
        
            :param reference: clave de referencia
            :type reference: :class:`string`

    """
    place = Place.objects.get_by_google_reference(reference)
    if place is not None:  # ya existe, hacemos una redireccion permanente
        return redirect(place.get_absolute_url(), permanent=True)
    from mapsServices.places.GPRequest import *
    try:
        search = GPRequest().retrieve_reference(reference)
    except GPAPIError, e:
        return render_to_response('webapp/placeerror.html', {'error': e},
                                  context_instance=RequestContext(request))
    except:
        return HttpResponseServerError

    place = Place.insert_or_update(name=search['result']['name'],
                                address=search['result']['formatted_address'], 
                                city=_get_city(search['result']['address_components']),
                                location=db.GeoPt(search['result']['geometry']['location']['lat'], search['result']['geometry']['location']['lng']),
                                google_places_reference=search['result']['reference'],
                                google_places_id=search['result']['id'],
                                user = request.user
                                )
    
    return redirect(place.get_absolute_url(), permanent=True)


def view_place(request, slug):
    """
        Devuelve la vista con informacion de un lugar
       
           :param slug: slug identificativo del lugar
           :type slug: string
    """
    place = Place.objects.get_by_slug(slug)
    if place is None:
        raise Http404
    from mapsServices.places.GPRequest import *
    try:
        search = GPRequest().retrieve_reference(place.google_places_reference)
    except: 
        return render_to_response('webapp/place.html', {'place': place},
                                  context_instance=RequestContext(request)
                                  )
    place.update(name=search['result']['name'],
                        address=search['result']['formatted_address'], 
                        city=_get_city(search['result']['address_components']),
                        location=db.GeoPt(search['result']['geometry']['location']['lat'], search['result']['geometry']['location']['lng']),
                        google_places_reference=search['result']['reference'],
                        google_places_id=search['result']['id']
                        )
    return render_to_response('webapp/place.html',
                              {'place': place, 'google': search['result']},
                              context_instance=RequestContext(request)
                              )
        
    
    
    
    
        
    
    
        