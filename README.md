Django-rest-forum
------------------

is a minimalistic discussion form entirely rest API based. 



Installation
------------

install using ``pip``:

    pip install -e git+git://github.com/Diwaniya-Labs/django-rest-forum/#egg=discussion

Configuration
-------------

Modify your ``settings.py``. Add ``'discussion'`` to your ``INSTALLED_APPS`` like this::

    INSTALLED_APPS = (
        ...
        'discussion',
    )

Specify your authentication user model in your settings file, for example :

    AUTH_USER_MODEL = 'account.User'

Include discussion urls in your root api urls:

    urlpatterns = patterns('',
                           ...
                           url(r'^api/discussion/', include('discussion.api_urls')),
                           ...

    )

Run the database migration:

    python manage.py migrate discussion