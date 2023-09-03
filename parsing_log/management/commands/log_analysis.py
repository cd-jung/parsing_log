import os
from django.core.management.base import BaseCommand
from parsing_log.analysis.analysis_excutor import excute_analysis

class Command(BaseCommand):
    """ Command for analysing a given log file """
    help = 'Command for analysing a given log file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='File path that is analised.')

    def handle(self, *args, **options):
        file_path = options['file_path']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"This file path{file_path} does not exist."))
            raise FileNotFoundError()
        self.stdout.write(self.style.NOTICE(f"Starts to analyse a log file '{file_path}'."))

        try:
            excute_analysis(file_path)
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"An eception occured while analysing data."))
            self.stdout.write(self.style.ERROR(exc))
            raise Exception(exc)
