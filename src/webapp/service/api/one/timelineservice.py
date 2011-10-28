# coding:utf-8
"""
This file is part of GeoRemindMe.

GeoRemindMe is free software: you can redistribute it and/or modify
it under the terms of the Affero General Public License (AGPL) as published 
by Affero, as published by the Free Software Foundation, either version 3 
of the License, or (at your option) any later version.

GeoRemindMe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

You should have received a copy of the GNU Affero General Public License
along with GeoRemindMe.  If not, see <http://www.gnu.org/licenses/>.

"""

"""
.. module:: api/timelineservice
    :platform: google-appengine (GAE)
    :synopsis: Funciones para obtener timelines del usuario (actividad, notificaciones, etc.)
.. moduleauthor:: Javier Cordero <javier@georemindme.com>
"""

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Timelines, Timeline
from mainservice import MainService

class GetActivityRequest(messages.Message):
    """
    Datos recibidos para poder procesar la peticion del timeline
        
        :param limit: (NO USABLE) limite de timeline a obtener (por defecto 10) 
        :type limit: :class:`Integer`
        :param query_id: identificador para continuar una peticion anterior, 
            si no existe, se devuelve el timeline mas nuevo
        :type query_id: :class`String`
    """
    limit = messages.IntegerField(1, default=10)
    query_id = messages.StringField(2, default=None)
  

class TimelineService(MainService):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetActivityRequest, Timelines)
    def get_activity(self, request):
        """
        Obtiene el timeline de actividad completo del usuario.
            
            :param request: datos necesarios para realizar la peticion
            :type request: :class:`GetActivityRequest`
            :returns: :class:`Timelines`
            :raises: :class:`ApplicationError`
        """ 
        self._login_required()
        
        activity = self.user.get_activity_timeline(request.query_id)
        timelines = []
        from time import mktime
        from geovote.models import Comment, Vote
        for a in activity[1]:
            t = Timeline(msg=a['msg'],
                         msg_id = a['msg_id'],
                         user=a['username'],
                         created=int(mktime(a['modified'].utctimetuple()))
                         )
            if a['instance'] is not None:
                if isinstance(a['instance'], Comment) or isinstance(a['instance'], Vote): 
                    t.instance_id=a['instance'].instance.id
                    t.instance_name=unicode(a['instance'].instance)
                    if hasattr(a['instance'].instance,"get_absolute_url"):
                        t.url = a['instance'].instance.get_absolute_url().encode("utf8")
                else:
                    t.instance_id=a['instance'].id
                    t.instance_name=unicode(a['instance'])
                    t.url = a['instance'].get_absolute_url().encode("utf8")
            timelines.append(t)
        return Timelines(timelines=timelines, query_id = '-'.join(activity[0]))
