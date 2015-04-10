======
README
======

Summary
=======

Denise is Dennis-as-a-Service.

.. Note::

   This is a copy-and-paste hacked-together monstrosity that
   does what I wanted it to do.

   It's a prototype.

   It's pre-alpha.

   Its future is unknown. I may never work on this again.


Install and configure
=====================

1. Create a virtual environment.

2. Install the dependencies::

     $ pip install -r requirements.txt

3. Copy ``denise/settings_local.py-dist`` to ``denise/settings_local.py``.
   Read through it and fill in appropriate values.

4. Run the migrations::

     $ ./manage.py migrate

5. FIXME: More?


Run server
==========

Run::

    $ python manage.py runserver


Locations of things
===================

:Project settings: ``denise/settings.py`` and ``denise/settings_local.py-dist``
:View code:        ``denise/view.py``
:Templates:        ``denise/templates/``
:Static assets:    ``denise/static/``
