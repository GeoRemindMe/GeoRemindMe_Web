# coding=utf-8

"""
.. module:: helpers
    :platform: appengine
    :synopsis: Helpers de models
"""


class UserHelper(object):
    """Do the queries needed to get a object
        Use ->  User.objects.method()
    """
    def get_by_key(self, key):
        from models import User
        try:
            return User.get(key)
        except:
            return None
    
    def get_by_username(self, username, keys_only=False):
        if username == '' or username is None:
            return None
        username = username.lower()
        if keys_only:
            from google.appengine.ext import db
            return db.GqlQuery('SELECT __key__ FROM User WHERE username = :1', username).get()
        from models import User
        return User.gql('WHERE username = :1', username).get()
    
    def get_by_id(self, userid, keys_only=False):
        try:
            userid = long(userid)
        except:
            return None
        from models import User
        if keys_only:
            from google.appengine.ext import db
            return db.Key.from_path(User.kind(), userid)
        return User.get_by_id(userid)
    
    def get_by_email(self, email, keys_only=False):
        """
         Search and returns a User object with that email
        """
        if email is None or not isinstance(email, basestring):
            return None
        email = email.lower()
        if keys_only:
            from google.appengine.ext import db
            return db.GqlQuery('SELECT __key__ FROM User WHERE email = :1', email).get()
        return self._get().filter('email =', email).get()       
    
    def get_by_email_not_confirm(self, email, keys_only=False):
        """Search and returns a User object with that email.
         Search users with confirm True or False
        """
        if email is None or not isinstance(email, basestring):
            return None
        email = email.lower()
        if keys_only:
            from google.appengine.ext import db
            return db.GqlQuery('SELECT __key__ FROM User WHERE email = :1 AND has=\'confirmed:F\'', email).get()
        return self._get().filter('email =', email).filter('has =', 'confirmed:F').get()
        
    def get_followers(self, userid = None, username=None, page=1, query_id=None):
        """Obtiene la lista de followers de un usuario
            
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
            
            :raises: AttributeError
        """
        from google.appengine.ext import db
        if username is not None:
            userkey = self.get_by_username(username, keys_only=True)
        elif userid is not None:
            from models import User
            userkey = db.Key.from_path(User.kind(), userid)
        else:
            raise AttributeError()
        from georemindme.paging import PagedQuery
        from models_acc import UserFollowingIndex
        followers = UserFollowingIndex.gql('WHERE following = :1 ORDER BY created DESC', userkey)
        p = PagedQuery(followers, id = query_id)
        from georemindme.funcs import fetch_parents
        users = fetch_parents(p.fetch_page(page))
        return [p.id, [{'id':u.id, 
                        'username':u.username, 
                        'is_following': u.has_follower(userkey=userkey),
                        'profile':u.profile } 
                       for u in users]]
    
    def get_followings(self, userid = None, username=None, page=1, query_id=None):
        """Obtiene la lista de personas a las que sigue el usuario
        
            :param userid: id del usuario (user.id)
            :type userid: :class:`string`
            :param username: nombre del usuario (user.username)
            :type username: :class:`string`
            :param page: numero de pagina a mostrar
            :type param: int
            :param query_id: identificador de busqueda
            :type query_id: int
            :returns: lista de tuplas de la forma [query_id, [(id, username, avatar)]]
            
            :raises: AttributeError
        """
        from google.appengine.ext import db
        if username is not None:
            userkey = self.get_by_username(username, keys_only=True)
        elif userid is not None:
            from models import User
            userkey = db.Key.from_path(User.kind(), userid)
        else: 
            raise AttributeError()
        from georemindme.paging import PagedQuery
        from models_acc import UserFollowingIndex
        followings = UserFollowingIndex.all().ancestor(userkey).order('-created')
        p = PagedQuery(followings, id = query_id)
        users = [index.following for index in p.fetch_page(page)]  # devuelve una lista anidada con otra
        users = db.get([item for sublist in users for item in sublist])
        return [p.id, [{'id':u.id, 
                        'username':u.username, 
                        'profile':u.profile 
                        } for u in users]
                ]
        
    def get_top_users(self, limit=5):
        from geouser.models_acc import UserCounter
        from georemindme.funcs import fetch_parentsKeys
        top_users = UserCounter.all(keys_only=True).order('-suggested').fetch(limit)
        top_users = fetch_parentsKeys(top_users)
        top_users = filter(None, top_users)
        return top_users

    def _get(self, string=None):
        from models import User
        return User.all().filter('has =', 'active:T')
