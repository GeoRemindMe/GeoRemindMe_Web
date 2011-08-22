# coding=utf-8
from google.appengine.ext import db

from geoalert.signals import suggestion_new, suggestion_deleted
from geolist.signals import list_new, list_deleted
from geovote.signals import comment_new, comment_deleted, vote_new, vote_deleted
from geoauth.clients.facebook import FacebookClient
from django.conf import settings

def new_suggestion(sender, **kwargs):
    fb_client=FacebookClient(user=sender.user)
    params= {
                "name": "En %(sitio)s" % {'sitio':sender.poi.name.encode('utf-8')},
                "link": settings.WEB_APP+"suggestion/"+sender.slug.encode('utf-8'),
                "caption": "Foto de %(sitio)s" % {'sitio':sender.poi.name.encode('utf-8')},
                #"picture": "http://www.example.com/thumbnail.jpg",
            }
    if sender.description is not None:
        params["description"]=sender.description.encode('utf-8')
            
    if sender._is_public():
        params["privacy"]={'value':'EVERYONE'}
    else:
        params["privacy"]={'value':'CUSTOM','friends':'SELF'}
        
    post_id = fb_client.consumer.put_wall_post("%(sugerencia)s" % {'sugerencia':sender.name.encode('utf-8')}, params)
    from models import _FacebookPost
    fb_post = _FacebookPost(instance=str(sender.key()), post=post_id['id'])
    fb_post.put()
suggestion_new.connect(new_suggestion)


def new_list(sender, **kwargs):
    from geolist.models import ListSuggestion, ListRequested

    params= {
            "name": sender.name,
            "link": settings.WEB_APP+sender.get_absolute_url()
            }

    if sender.description is not None:                
            params["description"]= "This is a longer description of the attachment"
    
    if sender._is_public():
        params["privacy"]={'value':'EVERYONE'}
    else:
        params["privacy"]={'value':'CUSTOM','friends':'SELF'}
    if isinstance(sender, ListSuggestion):
        fb_client=FacebookClient(user=sender.user)
        post_id = fb_client.consumer.put_wall_post("He creado una lista de sugerencias ", params)
    elif isinstance(sender, ListRequested):        
        fb_client=FacebookClient(user=sender.user)
        post_id = fb_client.consumer.put_wall_post("Necesito sugerencias", params)
    else:
        return
    
    from models import _FacebookPost
    fb_post = _FacebookPost(instance=str(sender.key()), post=post_id['id'])
    fb_post.put()
list_new.connect(new_list)


def new_comment(sender, **kwargs):
    if hasattr(sender.instance, '_vis'):
        params= {
                    "name": sender.instance.name,
                    "link": settings.WEB_APP+"suggestion/"+sender.instance.slug,
                    "caption": "{*actor*} posted a new review",
                    "picture": "http://localhost:8080/user/picture/"+sender.instance.user.username,
                }
        if sender.instance._is_public():
            params["privacy"]= {'value':'EVERYONE'}
                
        else:
            params["privacy"]= {'value':'CUSTOM','friends':'SELF'}
                
        fb_client=FacebookClient(user=sender.user)
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
    if hasattr(sender.instance, '_vis'):
        if isinstance(sender.instance, Comment):
            params= {
                        "name": sender.instance.instance.name.encode('utf-8'),
                        "link": settings.WEB_APP+"suggestion/"+sender.instance.instance.slug.encode('utf-8'),
                        #"caption": "{*actor*} posted a new review",
                        #"picture": "http://www.example.com/thumbnail.jpg",
                    }
        else:
            params= {
                        "name": sender.instance.name.encode('utf-8'),
                        "link": settings.WEB_APP+"suggestion/"+sender.instance.slug.encode('utf-8'),
                        #"caption": "{*actor*} posted a new review",
                        #"picture": "http://www.example.com/thumbnail.jpg",
                    }
            
        if hasattr(sender.instance,"description"):
            params['description']=sender.instance.description.encode('utf-8')
            
        if sender.instance._is_public():
            params["privacy"]= {'value':'EVERYONE'}
        else:
            params["privacy"]= {'value':'CUSTOM','friends':'SELF'}
            
                
        fb_client=FacebookClient(user=sender.user)
        
        if isinstance(sender.instance, Comment):
            user_comment = sender.instance.msg.encode('utf-8')
            
            if isinstance(sender.instance.instance, Suggestion):
                post_id = fb_client.consumer.put_wall_post(u"Me ha gustado el comentario \"%(comentario)s\" de %(autor)s en la sugerencia" % {'comentario':user_comment,'autor':sender.instance.user.username}, params)
            else:
                post_id = fb_client.consumer.put_wall_post(u"Me ha gustado el comentario \"%(comentario)s\" de %(autor)s en la lista de sugerencias" % {'comentario':user_comment,'autor':sender.instance.user.username}, params)
        else:
            post_id = fb_client.consumer.put_wall_post("Me ha gustado la sugerencia de %(autor)s" % {'autor':sender.instance.user.username}, params)
        
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
    suggestion_deleted.disconnect(deleted_post)
    list_deleted.disconnect(deleted_post)
