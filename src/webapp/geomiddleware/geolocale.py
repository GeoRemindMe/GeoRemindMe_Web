from django.utils.cache import patch_vary_headers
from django.utils import translation
from django.http import HttpResponsePermanentRedirect

class geolocale(object):
    def process_request(self, request):
        """
            process the request to load the language from user
        """
        app_host = 'georemindme.appspot.com'
        dom_host = 'georemindme.com'
        if dom_host in request.get_host():
            if request.is_secure():
                return HttpResponsePermanentRedirect('https://%s%s' % (app_host,request.path))
            return HttpResponsePermanentRedirect('http://%s%s' % (app_host,request.path))
        
        language = self._get_language_from_request(request)
        from django.utils import translation
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
   
    def _get_language_from_request(self, request):
        """
            search if the language is saved in session
            if not load it from HTTP_ACCEPT_LANGUAGE header
        """
        from django.conf import settings
        available = dict(settings.LANGUAGES)
        
        #first, we try to load the language from the session
        if 'LANGUAGE_CODE' in request.session:
            if request.session['LANGUAGE_CODE'] in available:
                return request.session['LANGUAGE_CODE']
        '''
            If not, try to load the language from the HTTP header,
            and save it to the session
        '''
        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            lang_code = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')
            for lang in lang_code:
                if lang in available: #we have the lang_code
                    request.session['LANGUAGE_CODE'] = lang
                    return lang
                lang = lang.split('-', )[0] #split language code, ex: 'es-ES', return 'es'
                if lang in available:
                    request.session['LANGUAGE_CODE'] = lang
                    return lang
                    
        return settings.LANGUAGE_CODE
    
    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
                
            
