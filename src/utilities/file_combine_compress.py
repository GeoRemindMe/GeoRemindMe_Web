#!/usr/bin/python
import os, os.path, shutil

YUI_COMPRESSOR = 'yuicompressor-2.4.6.jar'

def compress(in_files, out_file, in_type='js', verbose=False,
             temp_file='.temp'):
    temp = open(temp_file, 'w')
    for f in in_files:
        fh = open(f)
        data = fh.read() + '\n'
        fh.close()

        temp.write(data)

        print ' + %s' % f
    temp.close()

    options = ['-o "%s"' % out_file,
               '--type %s' % in_type]

    if verbose:
        options.append('-v')

    os.system('java -jar "%s" %s "%s"' % (YUI_COMPRESSOR,
                                          ' '.join(options),
                                          temp_file))

    org_size = os.path.getsize(temp_file)
    new_size = os.path.getsize(out_file)

    print '=> %s' % out_file
    print 'Original: %.2f kB' % (org_size / 1024.0)
    print 'Compressed: %.2f kB' % (new_size / 1024.0)
    print 'Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100)
    print ''

    #os.remove(temp_file)

COMMON_WEBAPP = [
    '../webapp/static/webapp/js/jquery.min.js',
    '../webapp/static/webapp/js/jquery.tmpl.js', 
    '../webapp/static/webapp/js/jquery-ui.min.js',
    '../webapp/static/common/js/grm.js',       
    '../webapp/static/webapp/js/common.js',
    '../webapp/static/facebookApp/js/jquery.hoverIntent.minified.js',
    '../webapp/static/webapp/js/jquery.lavalamp.js',
    '../webapp/static/webapp/js/jquery.reversegeocode.min.js',
    '../webapp/static/common/js/raw/jquery.cookies.2.2.0.min.js',
    '../webapp/static/webapp/js/jquery.placeholder.js',
    '../webapp/static/common/js/chronology.js',
]
COMMON_WEBAPP_OUT_DEBUG = '../webapp/static/common/js/common_webapp.js'
COMMON_WEBAPP_OUT = '../webapp/static/common/js/common_webapp.min.js'

LOGIN = [
    '../webapp/static/common/js/raw/login.js',
]
LOGIN_OUT_DEBUG = '../webapp/static/common/js/login.js'
LOGIN_OUT = '../webapp/static/common/js/login.min.js'

COMMON_FACEBOOKAPP = [
    '../webapp/static/webapp/js/jquery.min.js',
    '../webapp/static/webapp/js/jquery.tmpl.js',
    '../webapp/static/webapp/js/jquery-ui.min.js',
    '../webapp/static/webapp/js/jquery.placeholder.js',
    '../webapp/static/webapp/js/common.js',
    '../webapp/static/facebookApp/js/jquery.ba-resize.min.js',
    '../webapp/static/facebookApp/js/jquery.hoverIntent.minified.js',
    '../webapp/static/common/js/grm.js',
    '../webapp/static/facebookApp/js/main.js',
    '../webapp/static/facebookApp/js/chronology.js',
]

COMMON_FACEBOOKAPP_OUT_DEBUG = '../webapp/static/common/js/common_facebookApp.js'
COMMON_FACEBOOKAPP_OUT = '../webapp/static/common/js/common_facebookApp.min.js'

CHRONOLOGY = [
    '../webapp/static/facebookApp/js/social.js',    #
    '../webapp/static/facebookApp/js/chronology.js',#
]
CHRONOLOGY_OUT_DEBUG = '../webapp/static/common/js/chronology.js'
CHRONOLOGY_OUT = '../webapp/static/common/js/chronology.min.js'

# MOCHILA
BAG = [
    '../webapp/static/webapp/js/jquery.jeditable.js',
    '../webapp/static/common/js/raw/bag.js'
]
BAG_OUT_DEBUG = '../webapp/static/common/js/bag.js'
BAG_OUT = '../webapp/static/common/js/bag.min.js'

# VIEW_SUGGESTION
VIEW_SUGGESTION = [
    '../webapp/static/common/js/raw/load_panoramio.js',
    '../webapp/static/common/js/raw/view_suggestion.js',
    '../webapp/static/common/js/raw/wapi_panoramio.js'
]
VIEW_SUGGESTION_OUT_DEBUG = '../webapp/static/common/js/view_suggestion.js'
VIEW_SUGGESTION_OUT = '../webapp/static/common/js/view_suggestion.min.js'

# VIEW_PLACE
VIEW_PLACE = [
    '../webapp/static/common/js/raw/load_panoramio.js',
    '../webapp/static/common/js/raw/view_place.js',
    '../webapp/static/common/js/raw/wapi_panoramio.js'
]
VIEW_PLACE_OUT_DEBUG = '../webapp/static/common/js/view_place.js'
VIEW_PLACE_OUT = '../webapp/static/common/js/view_place.min.js'

# ADD_SUGGESTION
ADD_SUGGESTION = [

    '../webapp/static/common/js/raw/add_suggestion.js',
    '../webapp/static/facebookApp/js/geo-autocomplete/lib/jquery.autocomplete_geomod.js',
    '../webapp/static/facebookApp/js/geo-autocomplete/geo_autocomplete.js',
]
ADD_SUGGESTION_OUT_DEBUG = '../webapp/static/common/js/add_suggestion.js'
ADD_SUGGESTION_OUT = '../webapp/static/common/js/add_suggestion.min.js'


STYLESHEETS = [
    '../webapp/static/facebookApp/css/main.css',
    '../webapp/static/webapp/style/main.css',
    '../webapp/static/common/css/browser_error.css',
    #'../webapp/static/common/css/jquery-ui.css'
    ]
STYLESHEETS_OUT = '../webapp/static/common/css/style.min.css'

FB_STYLESHEETS = [
    '../webapp/static/facebookApp/css/main.css',
    '../webapp/static/common/css/browser_error.css',
    ]
FB_STYLESHEETS_OUT = '../webapp/static/common/css/fb_style.min.css'

def main():
    
    print 'Compressing JavaScript COMMON_WEBAPP...'
    compress(COMMON_WEBAPP, COMMON_WEBAPP_OUT, 'js', False, COMMON_WEBAPP_OUT_DEBUG)
    
    print 'Compressing JavaScript LOGIN...'
    compress(LOGIN, LOGIN_OUT, 'js', False, LOGIN_OUT_DEBUG)
    
    print 'Compressing JavaScript COMMON_FACEBOOKAPP...'
    compress(COMMON_FACEBOOKAPP, COMMON_FACEBOOKAPP_OUT, 'js', False, COMMON_FACEBOOKAPP_OUT_DEBUG)
    
    print 'Compressing JavaScript CHRONOLOGY...'
    compress(CHRONOLOGY, CHRONOLOGY_OUT, 'js', False, CHRONOLOGY_OUT_DEBUG)
    
    print 'Compressing JavaScript BAG...'
    compress(BAG, BAG_OUT, 'js', False, BAG_OUT_DEBUG)
    
    print 'Compressing JavaScript VIEW_SUGGESTION...'
    compress(VIEW_SUGGESTION, VIEW_SUGGESTION_OUT, 'js', False, VIEW_SUGGESTION_OUT_DEBUG)
    
    print 'Compressing JavaScript VIEW_PLACE...'
    compress(VIEW_PLACE, VIEW_PLACE_OUT, 'js', False, VIEW_PLACE_OUT_DEBUG)
    
    print 'Compressing JavaScript ADD_SUGGESTION...'
    compress(ADD_SUGGESTION, ADD_SUGGESTION_OUT, 'js', False, ADD_SUGGESTION_OUT_DEBUG)

    #~ print 'Compressing JavaScript VIEW_PLACE...'
    #~ compress(VIEW_PLACE, VIEW_PLACE_OUT, 'js', False, VIEW_PLACE_OUT_DEBUG)
    #~ 
    #~ print 'Compressing JavaScript VIEW_LIST...'
    #~ compress(VIEW_LIST, VIEW_LIST_OUT, 'js', False, VIEW_LIST_OUT_DEBUG)
    
    print 'Compressing CSS...'
    compress(STYLESHEETS, STYLESHEETS_OUT, 'css')
    
    print 'Compressing FACEBOOK CSS...'
    compress(FB_STYLESHEETS, FB_STYLESHEETS_OUT, 'css')

if __name__ == '__main__':
    main()





    
    


#~ DASHBOARD = [
    #~ '../webapp/static/webapp/js/jquery.min.js',
    #~ '../webapp/static/webapp/js/jquery-ui.min.js',
    #~ '../webapp/static/facebookApp/js/grm.js',
    #~ '../webapp/static/facebookApp/js/vault.js',
    #~ '../webapp/static/facebookApp/js/main.js',
    #~ '../webapp/static/facebookApp/js/social.js',
    #~ '../webapp/static/facebookApp/js/chronology.js',
    #~ '../webapp/static/webapp/js/jquery.tmpl.js',
    #~ '../webapp/static/webapp/js/common.js',
    #~ '../webapp/static/facebookApp/js/geo-autocomplete/lib/jquery.autocomplete_geomod.js',
    #~ '../webapp/static/facebookApp/js/geo-autocomplete/geo_autocomplete.js',
    #~ #'../webapp/static/facebookApp/js/suggestion.js', <-- Solo se usa en ADD SUGGESTION
    #~ '../webapp/static/common/js/jquery.ui/jquery.ui.core.js',
    #~ '../webapp/static/common/js/jquery.ui/jquery.ui.widget.js',
    #~ '../webapp/static/common/js/jquery.ui/jquery.ui.mouse.js',
    #~ '../webapp/static/common/js/jquery.ui/jquery.ui.resizable.js',
    #~ '../webapp/static/webapp/js/jquery.jeditable.js',
    #~ '../webapp/static/webapp/js/static.js',
    #~ '../webapp/static/facebookApp/js/jquery.ba-resize.min.js',
    #~ '../webapp/static/facebookApp/js/jquery.hoverIntent.minified.js',
    #~ '../webapp/static/webapp/js/jquery.lavalamp.js',
    #~ '../webapp/static/webapp/js/jquery.reversegeocode.min.js',
    #~ '../webapp/static/common/js/raw/jquery.cookies.2.2.0.min.js',
    #~ '../webapp/static/webapp/js/jquery.placeholder.js',
    #~ #'../webapp/static/facebookApp/js/geo-autocomplete/lib/jquery-ui/js/jquery-ui-1.8.5.custom.min.js',
    #~ #'../webapp/static/facebookApp/js/geo-autocomplete/ui.geo_autocomplete.js',
    #~ ]
