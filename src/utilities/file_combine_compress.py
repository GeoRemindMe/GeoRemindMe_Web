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



SCRIPTS = [
    '../webapp/static/webapp/js/jquery.min.js',
    '../webapp/static/webapp/js/jquery-ui.min.js',
    '../webapp/static/facebookApp/js/grm.js',
    '../webapp/static/facebookApp/js/vault.js',
    
    '../webapp/static/facebookApp/js/main.js',
    '../webapp/static/facebookApp/js/social.js',
    '../webapp/static/facebookApp/js/chronology.js',
    
    '../webapp/static/webapp/js/jquery.tmpl.min.js',
    '../webapp/static/webapp/js/common.js',
    
    '../webapp/static/facebookApp/js/geo-autocomplete/lib/jquery.autocomplete_geomod.js',
    '../webapp/static/facebookApp/js/geo-autocomplete/geo_autocomplete.js',
    
    #'../webapp/static/facebookApp/js/suggestion.js', <-- Solo se usa en ADD SUGGESTION
    '../webapp/static/common/js/jquery.ui/jquery.ui.core.js',
    '../webapp/static/common/js/jquery.ui/jquery.ui.widget.js',
    '../webapp/static/common/js/jquery.ui/jquery.ui.mouse.js',
    '../webapp/static/common/js/jquery.ui/jquery.ui.resizable.js',
    '../webapp/static/webapp/js/jquery.jeditable.js',
    '../webapp/static/webapp/js/static.js',
    '../webapp/static/facebookApp/js/jquery.ba-resize.min.js',
    '../webapp/static/facebookApp/js/jquery.hoverIntent.minified.js',
    '../webapp/static/webapp/js/jquery.lavalamp.js',
    '../webapp/static/webapp/js/jquery.reversegeocode.min.js',
    '../webapp/static/common/js/jquery.cookies.2.2.0.min.js',
    '../webapp/static/webapp/js/jquery.placeholder.js',
    
    
    #'../webapp/static/facebookApp/js/geo-autocomplete/lib/jquery-ui/js/jquery-ui-1.8.5.custom.min.js',
    #'../webapp/static/facebookApp/js/geo-autocomplete/ui.geo_autocomplete.js',

    ]
SCRIPTS_OUT_DEBUG = '../webapp/static/common/js/multifarce.js'
SCRIPTS_OUT = '../webapp/static/common/js/multifarce.min.js'

STYLESHEETS = [
    '../webapp/static/facebookApp/css/main.css',
    '../webapp/static/webapp/style/main.css',
    #'../webapp/static/common/css/jquery-ui.css'
    ]
STYLESHEETS_OUT = '../webapp/static/common/css/style.min.css'

def main():
    print 'Compressing JavaScript...'
    compress(SCRIPTS, SCRIPTS_OUT, 'js', False, SCRIPTS_OUT_DEBUG)

    print 'Compressing CSS...'
    compress(STYLESHEETS, STYLESHEETS_OUT, 'css')

if __name__ == '__main__':
    main()
