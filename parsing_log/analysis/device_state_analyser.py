
import os
from abstract_data_analyser import AbstractedDataAnalyser

class DeviceStateAnalyser(AbstractedDataAnalyser):

    def __init__(self):
        pass

    def read_a_line(self, line: str):
        """ Parsing and analysing a line """
        pass

    def analyse(self):
        """ Nothing to do in this class """
        pass

    def store(self) -> str:
        """ Storing a result as a file and return the result file.
            Although it should be stored in DB, handling the data as a file for the test 
        """
        result_file_path = os.path.join(os.getcwd(), 'parsing_log', 'test_data', 'test.result')
        
        # Store analysis result to file

        return result_file_path