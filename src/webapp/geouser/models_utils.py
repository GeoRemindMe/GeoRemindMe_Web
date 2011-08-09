# coding=utf-8

"""
.. module:: models_utils
    :platform: appengine
    :synopsis: Modelos auxiliares
"""

from django.utils.translation import gettext_lazy as _

from google.appengine.ext import db
from models import User


class _Notification(db.Model):
    from models_acc import UserTimelineBase
    owner = db.ReferenceProperty(User, required=True)
    timeline = db.ReferenceProperty(UserTimelineBase, required=True)
    _created = db.DateTimeProperty(auto_now_add=True)
    
    @property
    def user(self):
        return self.timeline.user
    
    @property
    def msg_id(self):
        return self.timeline.msg_id
    
    @property
    def msg(self):
        return self.timeline.msg
    
    @property
    def instance(self):
        return self.timeline.instance
    
    @property
    def modified(self):
        return self.timeline.modified
    
    @property
    def created(self):
        return self.timeline.created
    
    @property
    def id(self):
        return self.timeline.id
    
    def put(self):
        if not self.is_saved():
            self.owner.counters.set_notifications()
        super(_Notification, self).put()

class _Report_Account_follower(db.Model):
    """
        Guarda la lista de nuevos followers para posteriormente ser
        notificada a los usuarios que no quieren email instantaneos
    """
    keys = db.StringListProperty(db.Key)
    created = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def insert_or_update(cls, userkey, add=None, delete=None):
        from google.appengine.ext import deferred
        if not isinstance(userkey, db.Key):
            raise deferred.PermanentTaskFailure
        report = cls.get_by_key_name('report_account_follower_%d' % userkey.id())
        if report is not None:
            if add is not None:
                report.keys.append(str(add))
            if delete is not None:
                try:
                    report.keys.remove(str(delete))
                except:
                    raise deferred.PermanentTaskFailure
        else:
            if add is not None:
                if type(add) != type(list):
                    add = [str(add)]
                report = cls(key_name='report_account_follower_%d' % userkey.id(), keys=add)
            else:
                return None
        try:
            report.put()
        except:
            raise deferred.PermanentTaskFailure 
        return report
    
    
    def clear(self):
        del self.keys[:]
        self.put()
        
    def send_notification(self, user):
        from geouser.mails import send_notification_account_summary
        followers = db.get(self.keys)
        send_notification_account_summary(user.email,
                                          user=user,
                                          followers=followers,
                                          language=user.get_language()
                                          )
        
    @property
    def id(self):
        return self.key().name().split('report_account_follower_')[1]


class _Report_Suggestion_changed(db.Model):
    from properties import JSONProperty
    user = db.ReferenceProperty(User)
    counters = JSONProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def insert_or_update(cls, userkey, suggestionkey):
        from google.appengine.ext import deferred
        if not isinstance(suggestionkey, db.Key) or not isinstance(userkey, db.Key):
            raise deferred.PermanentTaskFailure
        report = cls.get_by_key_name('report_suggestion_changed_%d' % suggestionkey.id())
        if report is None:
            from geoalert.models_indexes import SuggestionCounter
            report = cls(key_name='report_suggestion_changed_%d' % suggestionkey.id(),
                         user = db.get(userkey),
                         counters = SuggestionCounter.all().ancestor(suggestionkey).get().to_dict()
                         )
            try:
                report.put()
            except:
                raise
                raise deferred.PermanentTaskFailure
        return report
    
    @property
    def id(self):
        return self.key().name().split('report_suggestion_changed_')[1]
    
    def to_dict(self):
        from geoalert.models import Suggestion
        sug = Suggestion.objects.get_by_id_user(self.id, self.user)
        return {self.id: {
                          'name': sug.name,
                          'counters': sug.counters,
                          'old_counters': self.counters
                          }
                }


class _Report_Suggestion_commented(db.Model):
    user = db.ReferenceProperty(User)
    time_first_comment = db.DateTimeProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def insert_or_update(cls, userkey, suggestionkey, time):
        from google.appengine.ext import deferred
        report = cls.get_by_key_name('report_suggestion_commented_%d' % suggestionkey.id())
        if report is None:
            report = cls(key_name='report_suggestion_commented_%d' % suggestionkey.id(),
                         user = db.get(userkey),
                         time_first_comment=time
                         )
            try:
                report.put()
            except:
                raise deferred.PermanentTaskFailure
        return report
    
    @property
    def id(self):
        return self.key().name().split('report_suggestion_commented_')[1]
    
    def to_dict(self):
        from geoalert.models import Suggestion
        sug = Suggestion.objects.get_by_id_user(self.id, self.user)
        return {self.id: {
                          'name': sug.name,
                          'time': self.time_first_comment
                          }
                }
    
