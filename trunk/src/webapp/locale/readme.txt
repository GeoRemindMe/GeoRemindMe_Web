how to create .po and .mo files:
http://docs.djangoproject.com/en/dev/topics/i18n/localization/

You need to have installed this:
sudo apt-get install gettext

django-admin.py makemessages -l de #creates german (de) .po
django-admin.py compilemessages # compiles and create .mo

or
django-admin makemessages -l es #creates spanish (es) .po
django-admin compilemessages # compiles and create .mo

how to create translation strings:
http://docs.djangoproject.com/en/dev/topics/i18n/internationalization/#

http://docs.djangoproject.com/en/dev/howto/i18n/#using-translations-in-your-own-projects
