# django-proclaim

Djando-proclaim is a django application that allows one to easily
release new features to a subset of users.

Still very much a work in progress, this just outlines what the goal is.

# Dependancies

* [django](http://djangoproject.com)
* [redis](http://redis.io)
* [proclaim](http://github.com/asenchi/proclaim)

**NOTE**: This application expects a Redis server running on localhost. Eventually
I'll make that configurable, but for now it makes the most sense.

# Usage

Basically one would use this app to split their Django project up into
features that you can roll out to individuals, groups or a percentage of
users.  Many sites implement a similar strategy to catch bugs or see how
new features are received.

Disclaimer: I am not really happy with the interface currently and am
having issues deciding the best course of action.  Here are the two
options I am looking at for templates:

Option 1:

    {% proclaim "feature1" %}
        ... handy new feature of your site ...
    {% endproclaim %}

Option 2:

    {% proclaim "feature1" "path/to/template.html" %}

I think the second one looks cleaner, but I am not sure about it. May be
nice to keep all "feature templates" in snippets until they are
implemented? Who knows... I am still on the fence.

From the command line, add a percentage of users to 'feature1':

This will allow every fifth user to see "feature1":
    $ python manage.py proclaim "feature1" --percentage="20" --activate

Add a group to feature2:
    $ python manage.py proclaim "feature2" --group=Admins --activate

See which target is active for "feature3":
    $ python manage.py proclaim "feature3"
    >>> Group: Admins

You can always just use the
[proclaim](http://github.com/asenchi/proclaim) in your views.py or
models.py to target specific users with new features.

# Copyright

Copyright @ 2010 Curt Micol, see LICENSE for details.
