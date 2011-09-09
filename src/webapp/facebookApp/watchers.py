# coding=utf-8


from google.appengine.ext import db

from geoalert.signals import suggestion_new, suggestion_deleted
from geolist.signals import list_new, list_deleted
from geovote.signals import comment_new, comment_deleted, vote_new, vote_deleted
from geoauth.clients.facebook import FacebookClient
from django.conf import settings as __web_settings # parche hasta conseguir que se cachee variable global


def new_suggestion(sender, **kwargs):
    try:
        fb_client=FacebookClient(user=sender.user)
    except:
        return
    params= {
                "name": "Ver detalles de la sugerencia",
                "link": __web_settings.WEB_APP+"suggestion/"+sender.slug,
                "caption": "Destalles del sitio (%(sitio)s), comentarios, etc." % {'sitio':sender.poi.name},
                #"caption": "Foto de %(sitio)s" % {'sitio':sender.poi.name},
                #"picture": environ['HTTP_HOST'] +"/user/"+sender.user.username+"/picture",
            }
    if sender.description is not None:
        params["description"]=sender.description
    #Pasamos todos los valores a UTF-8
    params = dict([k, v.encode('utf-8')] for k, v in params.items())        
    if sender._is_public():
        params["privacy"]={'value':'EVERYONE'}
    else:
        params["privacy"]={'value':'CUSTOM','friends':'SELF'}
    try:
        post_id = fb_client.consumer.put_wall_post("%(sugerencia)s" % {'sugerencia':sender.name.encode('utf-8')}, params)
        from models import _FacebookPost
        fb_post = _FacebookPost(instance=str(sender.key()), post=post_id['id'])
        fb_post.put()
    except:
        pass
#suggestion_new.connect(new_suggestion)


def new_list(sender, **kwargs):
    from geolist.models import ListSuggestion, ListRequested
    try:
        fb_client=FacebookClient(user=sender.user)
    except:
        return
    params= {
            "name": sender.name,
            "link": __web_settings.WEB_APP+sender.get_absolute_url()
            }
    if sender.description is not None:                
            params["description"]= "This is a longer description of the attachment"
    params = dict([k, v.encode('utf-8')] for k, v in params.items())
    if sender._is_public():
        params["privacy"]={'value':'EVERYONE'}
    else:
        params["privacy"]={'value':'CUSTOM','friends':'SELF'}
    if isinstance(sender, ListSuggestion):
        post_id = fb_client.consumer.put_wall_post("He creado una lista de sugerencias ", params)
    elif isinstance(sender, ListRequested):        
        post_id = fb_client.consumer.put_wall_post("Necesito sugerencias, ¿me podéis ayudar?", params)
    else:
        return
    from models import _FacebookPost
    fb_post = _FacebookPost(instance=str(sender.key()), post=post_id['id'])
    fb_post.put()
list_new.connect(new_list)


def new_comment(sender, **kwargs):
    if hasattr(sender.instance, '_vis'):
        try:
            fb_client=FacebookClient(user=sender.user)
        except:
            return
        from os import environ
        params= {
                    "name": sender.instance.name,
                    "link": environ['HTTP_HOST'] + sender.instance.get_absolute_url(),
                    "caption": "Sugerencia de "+sender.instance.user.username,
                    "picture": environ['HTTP_HOST'] +"/user/"+sender.instance.user.username+"/picture/",
                }
        params = dict([k, v.encode('utf-8')] for k, v in params.items())
        if sender.instance._is_public():
            params["privacy"]= {'value':'EVERYONE'}
                
        else:
            params["privacy"]= {'value':'CUSTOM','friends':'SELF'}
        post_id = fb_client.consumer.put_wall_post(sender.msg, params)
        from models import _FacebookPost
        fb_post = _FacebookPost(instance=str(sender.key()), post=post_id['id'])
        fb_post.put()
    else:
        return
comment_new.connect(new_comment)


def new_vote(sender, **kwargs):
    from geovote.models import Comment
    from geoalert.models import Suggestion
    from os import environ
    if hasattr(sender.instance, '_vis'):
        try:
            fb_client=FacebookClient(user=sender.user)
        except:
            return
        if isinstance(sender.instance, Comment):
            params= {
                        "link": environ['HTTP_HOST'] + sender.instance.instance.get_absolute_url(),
                        "caption": sender.instance.user.username,
                        #"picture": "http://georemindme.com/media/img/whatsup.png"
                        "picture": environ['HTTP_HOST'] +"/user/"+sender.instance.instance.user.username+"/picture",
                    }
            if isinstance(sender.instance.instance, Suggestion):
                params["name"]= sender.instance.instance.name
                message = "Me gusta el comentario: \"%(comentario)s\" de %(autor)s en la sugerencia:" % {'comentario': sender.instance.msg,
                                                                                                           'autor':sender.instance.user.username
                                                                                                           }
            else:
                params["name"]="Ver lista de sugerencias: "+ sender.instance.instance.name
                message = "Me gusta el comentario: \"%(comentario)s\" de %(autor)s" % {'comentario': sender.instance.msg,
                                                                                                                      'autor': sender.instance.user.username
                                                                                                                      }
                
        elif isinstance(sender.instance, Suggestion):
            message = "Me gusta la sugerencia de %(autor)s:" % {
                                                                   'autor':sender.instance.user.username
                                                                   }
            params= {
                        "name": sender.instance.name,
                        "link": environ['HTTP_HOST'] + sender.instance.get_absolute_url(),
                        "caption": sender.instance.user.username,
                        #"picture": "http://georemindme.com/media/img/whatsup.png"
                        "picture": environ['HTTP_HOST'] +"/user/"+sender.instance.user.username+"/picture",
                    }
        if hasattr(sender.instance,"description"):
            params['description']=sender.instance.description
        # codificamos todo el diccionario de parametros, antes de añadir el parametro privacy
        params = dict([k, v.encode('utf-8')] for k, v in params.items())
        if sender.instance._is_public():
            params["privacy"]= {'value':'EVERYONE'}
        else:
            params["privacy"]= {'value':'CUSTOM','friends':'SELF'}
        
        #~ raise Exception(params["picture"])
        post_id = fb_client.consumer.put_wall_post(message.encode('utf-8'), params)
        from models import _FacebookPost
        fb_post = _FacebookPost(instance=str(sender.key()), post=post_id['id'])
        fb_post.put()
    else:
        return
vote_new.connect(new_vote)


def deleted_post(sender, **kwargs):
    from models import _FacebookPost
    fb_post = _FacebookPost.all().filter('instance =', str(sender.key())).get()
    if fb_post is not None:
        fb_client=FacebookClient(user=sender.user)
        try:
            fb_client.consumer.delete_object(fb_post.post)
            fb_post.delete()
        except:
            pass
suggestion_deleted.connect(deleted_post)
list_deleted.connect(deleted_post)
comment_deleted.connect(deleted_post)


def disconnect_all():
    suggestion_new.disconnect(new_suggestion)
    list_new.disconnect(new_list)
    comment_new.disconnect(new_comment)
    vote_new.disconnect(new_vote)
    suggestion_deleted.disconnect(deleted_post)
    list_deleted.disconnect(deleted_post)
    comment_deleted.disconnect(deleted_post)
