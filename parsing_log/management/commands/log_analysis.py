from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Command for analysing a given log file """
    help = 'Command for analysing a given log file'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help='File name that is analised.')

    def handle(self, *args, **options):
        file_name = options['file_name']
        self.stdout.write(self.style.NOTICE(f"Starts to analyse a log file '{file_name}'."))