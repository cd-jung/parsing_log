from django.test import TestCase
from parsing_log.management.commands.log_analysis import Command
import os

# Create your tests here.
class DeviceStateAnalyserTestCase(TestCase):
    def setUp(self):
        pass

    def test_analise_a_line(self):
        self.assertTrue(True)

class LogAnalysisCommandTestCase(TestCase):
    def setUp(self):
        self.command = Command()

    def test_log_analysis_command_success(self):
        try:
            self.command.handle(file_path=os.path.join(os.getcwd(), 'parsing_log', 'test_data', 'test.log'))
        except Exception as e:
            self.fail("test_log_analysis_command failed.")
        
    def test_log_analysis_command_failure_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            self.command.handle(file_path=os.path.join(os.getcwd(), 'parsing_log', 'test_data', 'test.log2'))