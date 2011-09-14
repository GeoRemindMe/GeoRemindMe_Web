# coding=utf-8

from protorpc import message_types
from protorpc import remote
from protorpc import messages

from messages import Timelines, Timeline

class GetActivityRequest(messages.Message):
    limit = messages.IntegerField(1, default=10)
    query_id = messages.StringField(2, default=None)

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
        from geouser.models import User
        user = User.objects.get_by_id(int(environ['user']))
        if user is None:
            from protorpc.remote import ApplicationError
            raise ApplicationError("Unknow user")
        activity = user.get_activity_timeline(request.query_id)
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
        return Timelines(timelines=timelines, query_id = activity[0])

    
