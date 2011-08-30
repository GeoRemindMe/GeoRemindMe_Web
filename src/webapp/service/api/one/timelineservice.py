# coding=utf-8

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Timelines, Timeline

class GetActivityRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    on_or_before = messages.IntegerField(2)

    class Order(messages.Enum):
        MODIFIED = 1
        TEXT = 2
    order = messages.EnumField(Order, 3, default=Order.MODIFIED)
  

class TimelineService(remote.Service):
    """
        Define el servicio para obtener timelines de usuarios
    """
    
    #decorador para indicar los metodos del servicio
    @remote.method(GetActivityRequest, Timelines)
    def get_activity(self, request):
        from os import environ
        activity = environ['user'].get_activity_timeline()
        timelines = []
        from time import mktime
        from geovote.models import Comment, Vote
        for a in activity[1]:
            t = Timeline(msg=a['msg'], 
                         user=a['username'],
                         created=int(mktime(a['modified'].utctimetuple()))
                         )
            if a['instance'] is not None:
                if isinstance(a['instance'], Comment) or isinstance(a['instance'], Vote): 
                    t.instance_id=a['instance'].instance.id
                    t.instance_name=unicode(a['instance'].instance)
                else:
                    t.instance_id=a['instance'].id
                    t.instance_name=unicode(a['instance'])
            timelines.append(t)
        return Timelines(timelines=timelines)

    