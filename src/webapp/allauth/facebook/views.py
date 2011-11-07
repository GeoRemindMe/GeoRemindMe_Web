from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from allauth.utils import get_login_redirect_url
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.oauth import OAuthClient

from facebook import GraphAPI, GraphAPIError

from models import FacebookApp, FacebookAccount
from forms import FacebookConnectForm

from allauth.utils import valid_email_or_none

def login(request):
    ret = None
    if request.method == 'POST':
        form = FacebookConnectForm(request.POST)
        if form.is_valid():
            try:
                token = form.cleaned_data['access_token']
                g = GraphAPI(token)
                facebook_me = g.get_object("me")
                email = valid_email_or_none(facebook_me.get('email'))
                social_id = facebook_me['id']
                try:
                    account = FacebookAccount.objects.get(social_id=social_id)
                except FacebookAccount.DoesNotExist:
                    account = FacebookAccount(social_id=social_id)
                account.link = facebook_me['link']
                account.name = facebook_me['name']
                if account.pk:
                    account.save()
                data = dict(email=email,
                            facebook_me=facebook_me)
                # some facebook accounts don't have this data
                data.update((k,v) for (k,v) in facebook_me.items() 
                            if k in ['username', 'first_name', 'last_name'])
                ret = complete_social_login(request, data, account)
            except GraphAPIError, e:
                pass
    if not ret:
        ret = render_authentication_error(request)
    return ret

    
