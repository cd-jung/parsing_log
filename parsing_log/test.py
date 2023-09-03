from django.test import TestCase
from parsing_log.management.commands.log_analysis import Command
from parsing_log.analysis.device_state_analyser import DeviceStateAnalyser, DeviceState
import os

# Create your tests here.
class DeviceStateAnalyserTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_time_str = "Jul 23 15:12:39:599"
        cls.test_timestamp = 1690125159599
        cls.test_line_on = "Jul 23 15:12:39:599 [139681125603140] dut: Device State: ON"
        cls.test_line_off = "Jul 23 15:12:40:599 [139681125603141] dut: Device State: OFF"
        cls.test_off_timestamp = 1690125160599
        cls.test_duration = cls.test_off_timestamp - cls.test_timestamp
        cls.test_line_err = "Jul 23 15:12:41:599 [139681125603142] dut: Device State: ERR"
        cls.test_err_timestamp = 1690125161599
        
        return super().setUpClass()
    def setUp(self):
        self.analyser = DeviceStateAnalyser()
        print('called')

    def test_convert_time(self):
        self.assertEqual(int(self.analyser._convert_time(self.test_time_str).timestamp()*1000), self.test_timestamp)

    def test_extract_time(self):
        self.assertEqual(int(self.analyser._extract_time(self.test_line_on).timestamp()*1000), self.test_timestamp)

    def test_extract_state(self):
        self.assertEqual(self.analyser._extract_state(self.test_line_on), DeviceState.ON)
        self.assertEqual(self.analyser._extract_state(self.test_line_off), DeviceState.OFF)
        self.assertEqual(self.analyser._extract_state(self.test_line_err), DeviceState.ERR)

    def test_read_a_line(self):
        original_len = len(self.analyser.device_onoff_records)
        self.analyser.read_a_line(self.test_line_on)
        self.assertEqual(len(self.analyser.device_onoff_records), original_len+1)
        self.assertTrue('start_time' in self.analyser.device_onoff_records[-1])
        self.assertEqual(self.analyser.device_onoff_records[-1]['start_time'], self.test_timestamp)
        
        original_len = len(self.analyser.device_onoff_records)
        self.analyser.read_a_line(self.test_line_off)
        self.assertEqual(len(self.analyser.device_onoff_records), original_len)
        self.assertTrue('end_time' in self.analyser.device_onoff_records[-1])
        self.assertEqual(self.analyser.device_onoff_records[-1]['end_time'], self.test_off_timestamp)
        self.assertTrue('duration' in self.analyser.device_onoff_records[-1])
        self.assertEqual(self.analyser.device_onoff_records[-1]['duration'], self.test_duration)
        
        original_len = len(self.analyser.device_error_records)
        self.analyser.read_a_line(self.test_line_err)
        self.assertEqual(len(self.analyser.device_error_records), original_len+1)
        self.assertEqual(self.analyser.device_error_records[-1], self.test_err_timestamp)

    def test_analyse(self):
        self.analyser.read_a_line(self.test_line_on)
        self.analyser.read_a_line(self.test_line_off)
        self.analyser.read_a_line(self.test_line_err)

        self.analyser.analyse()
        self.assertEqual(self.analyser.start_time, self.test_timestamp)
        self.assertEqual(self.analyser.end_time, self.test_err_timestamp)
        self.assertEqual(self.analyser.total_of_on_time, self.test_duration)

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