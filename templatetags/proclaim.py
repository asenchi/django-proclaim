from django.template import Library, TemplateSyntaxError, Node

from redis import Redis
from proclaim import Proclaim

register = template.Library()

class ProclaimNode(Node):
    def __init__(self, feature_string, nodelist):
        self.feature_string = feature_string
        self.nodelist = nodelist

        # We expect Redis to be on localhost at the standard port.
        r = Redis()
        self.proclaim = Proclaim(r)

    def render(self, context):
        feature = self.feature_string
        user = resolve_variable('user', context)
        if not user.is_authenticated:
            return ''
        is_active = self.proclaim.is_active(feature, user)
        if is_active:
            return self.nodelist.render(context)
        return ''

def do_proclaim(parser, token):
    """
    Outputs the contents of the block if the currently authenticated user
    is activated to view the feature.

    Dependencies::
    * `redis`_
    * `redis.py`
    * `proclaim`_

    .. _redis: http://redis.io
    .. _redis.py: http://pypi.python.org/pypi/redis
    .. _proclaim: http://github.com/asenchi/proclaim

    Examples::

        {% proclaim "newfeature" %}
            ...
        {% endproclaim %}
    """
    try:
        tag_name, feature_string = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r takes one argument" % tag_name)
    if not (feature_string[0] == feature_string[-1]
            and feature_string[0] in ('"', '"')):
        raise TemplateSyntaxError("%r feature should be in quotes" % tag_name)
    end_tag = 'end' + tag_name
    nodelist = parser.parse((end_tag,))
    parser.delete_first_token()
    return ProclaimNode(feature_string[1:-1], nodelist)
proclaim = register.tag("proclaim", do_proclaim)
