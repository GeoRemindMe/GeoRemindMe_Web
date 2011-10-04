#!/usr/bin/python
# coding=utf-8

import os,sys,fileinput,re,urllib

ROOT_DIR = "georemindme"
CWD = os.getcwd()

def main():
    
    if len(sys.argv) <> 3:
        print "Uso: %s <google appengine sdk path> <version>" % sys.argv[0]
        exit(-1)
    
    if not confirm("Vas a subir la aplicación a la versión %s. ¿Estás seguro?" % sys.argv[2]):
        exit(-1)
    
    find_root()
    debug(False)
    
    #resp = unit() and make_doc() and compress() and lang() and upload()
    resp = unit() and compress() and lang() and upload()
    
    find_root()
    debug(True)
    
    if resp:
        print "-> Todo correcto. Aplicación subida a la versión %s" % sys.argv[2]
    
    os.chdir( CWD )


# finds root repo dir
def find_root():
    cwd = os.path.basename(os.getcwd())
    while cwd <> ROOT_DIR:
        os.chdir( os.pardir )
        cwd = os.path.basename(os.getcwd())
        
        if cwd == '/':
            raise Exception("Path not found")
        

def make_doc():
    print "-> Generando documentación..."
    os.chdir( "doc/sphinx-doc" )
    if os.system("export PYTHONPATH=$PYTHONPATH:%s;make html" % sys.argv[1]):
        print "-> Error generando documentación"
        print "-> Compruebe que tiene instalados los paquetes: python-sphinx, python-yaml y que ha puesto la ruta correcta del SDK de appengine"
        return False
    find_root()
    return True
    

def compress():
    os.chdir( "src/utilities" )
    print "-> Comprimiendo estáticos..."
    if os.system("python2 file_combine_compress.py"):
        print "-> Error comprimiendo estáticos"
        return False
    find_root()
    return True

def debug(true_or_false):
    for line in fileinput.input( "src/webapp/settings.py", inplace=1):
        line = re.sub(r'^DEBUG\s*=\s*%s' % str(not true_or_false),'DEBUG = %s' % str(true_or_false), line)
        sys.stdout.write(line)

def unit():
    print "Consulte la dirección http://localhost:8080/test y asegurese de que están todos los tests correctos"
    if not confirm("¿Todo correcto?"):
        print "-> Han fallado los tests unitarios. Corríja los fallos antes de continuar"
        return False
    return True

def lang():
    os.chdir( "src/webapp" )
    print "-> Compilando ficheros de idiomas..."
    if os.system("python2 manage.py compilemessages"):
        print "-> Error compilando idiomas"
        return False
    find_root()
    return True
    

def upload():
    os.chdir( "src/webapp" )
    if os.system("python2 %s --version=%s update ." % (os.path.join(sys.argv[1],"appcfg.py"),sys.argv[2], ) ):
        print "-> Error subiendo la aplicación. Compruebe que ha puesto bien la ruta del SDK de AppEngine"
        return False
    find_root()
    return True
    

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

if __name__ == "__main__":
    main()
