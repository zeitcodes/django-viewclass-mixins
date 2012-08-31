Django ViewClass Mixins
=======================

Provides some common mixin patterns for Django's View classes.

Installation
------------

Run `pip install hg+https://bitbucket.org/nextscreenlabs/django-viewclass-mixins`

View Mixins
-----------

###LoginMixin
Ensures the view is being requested by an authenticated user or redirects to the login page. It behaves the same as the function decorator `login_required`.

###DeactivateMixin
A mixin to the DeleteView. Instead of deleting an object it will mark it as inactive instead.

###FilterListMixin
A mixin to the ListView. It will apply filters from the URL querystring to the underlying QuerySet before the list is returned.