from __future__ import print_function

from django.core.management.base import BaseCommand
from cronjob.custom_crontab import CustomCrontab
import os


class Command(BaseCommand):
    help = 'run this command to add, show or remove the jobs defined in CRONJOBS setting from/to crontab'

    def add_arguments(self, parser):
        parser.add_argument('subcommand', choices=['add', 'show', 'remove', 'run', 'add_one', 'remove_one'])
        parser.add_argument('jobhash', nargs='?')

    def handle(self, *args, **options):
        """
        Dispatches by given subcommand
        """
        if options['subcommand'] == 'add':
            with CustomCrontab(**options) as crontab:
                crontab.remove_jobs()
                crontab.add_jobs()
        elif options['subcommand'] == 'show':
            with CustomCrontab(readonly=True, **options) as crontab:
                crontab.show_jobs()
        elif options['subcommand'] == 'remove':
            with CustomCrontab(**options) as crontab:
                crontab.remove_jobs()
        elif options['subcommand'] == 'run':
            CustomCrontab().run_job(options['jobhash'])
        elif options['subcommand'] == 'add_one':
            with CustomCrontab(**options) as crontab:
                crontab.add_one_job(options['jobhash'])
        elif options['subcommand'] == 'remove_one':
            with CustomCrontab(**options) as crontab:
                crontab.remove_job_with_hash(options['jobhash'])
        else:
            print(self.help)
