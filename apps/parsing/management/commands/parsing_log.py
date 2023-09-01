from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Command for parsing given log file """
    help = 'Command for parsing given log file'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Parsing command is executed successfully'))