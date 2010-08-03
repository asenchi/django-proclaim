from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import os
import sys

class Command(BaseCommand):

    # Callback
    def findtarget(option, opt_str, value, parser, *args, **kwargs):
        "We only want to specify one target per feature at a time."
        if type(value) == "int":
            delattr(parser.values, 'proclaim_group')
            delattr(parser.values, 'proclaim_user')
        else:
            delattr(parser.values, 'proclaim_percentage')
            if "proclaim_group" in parser.values:
                delattr(parser.values, 'proclaim_user')

    option_list = Basecommand.option_list + (
        make_option('--activate',
            action='store_true',
            dest='proclaim_activate',
            help="Activate given target for feature."
        ),
        make_option('--deactivate',
            action='store_false',
            dest='proclaim_activate',
            help="Deactivate given target for feature."
        ),
        make_option('-g', '--group',
            type='string',
            action='callback', callback=findtarget,
            dest='proclaim_group', default='',
            help="Activate given group."
        ),
        make_option('-p', '--percentage',
            type='int',
            action='callback', callback=findtarget,
            dest='proclaim_percentage', default='',
            help="Activate given percentage of users."
        ),
        make_option('-u', '--user',
            type='string',
            action='callback', callback=findtarget,
            dest='proclaim_user', default='',
            help="Activate given user."
        ),
    )

    help = "Proclaim a feature and activate/deactivate a subset of users to use."
    args = 'feature'

    def handle(self, feature='', *args, **options):
        try:
            import redis
            from proclaim import Proclaim
        except ImportError:
            raise CommandError("Depends on Proclaim and Redis.")

        if args:
            raise CommandError('Usage is proclaim %s' % self.args)
        if not feature:
            raise CommandError('Usage is proclaim %s' % self.args)

#        redis = redis.Redis()
#        proclaim = Proclaim(redis)
#
#        if getattr(options, 'proclaim_deactivate'):
