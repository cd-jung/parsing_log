
import os
from enum import Enum
from datetime import datetime
from .abstract_data_analyser import AbstractedDataAnalyser

class DeviceState(Enum):
    ON = "ON"
    OFF = "OFF"
    ERR = "ERR"

    def get_state_by_val(val:str):
        for state in DeviceState: 
            if state.value == val:
                return state
        return None
    
class DeviceStateAnalyser(AbstractedDataAnalyser):
    # Extracted data. This shuld be a file or other data source when the input is expected huge.
    device_onoff_records = [] # {'start_time':timestamp, 'end_time':timestamp, 'duration':mill second}
    device_error_records = [] # timestamp
    total_of_on_time = 0 # mill second
    time_records = [] # timestamp
    start_time = 0
    end_time = 0

    def __init__(self):
        pass

    def read_a_line(self, line: str):
        """ Parsing and store a line data. """
        time = int(self._extract_time(line).timestamp() * 1000)
        state = self._extract_state(line)
        # print(f"time:{time}, state:{state}")

        self.time_records.append(time)

        if state == DeviceState.ERR:
            self.device_error_records.append(time)
        elif state == DeviceState.ON:
            self.device_onoff_records.append({"start_time":time})
        elif state == DeviceState.OFF:
            record = self.device_onoff_records[-1]
            record["end_time"] = time
            record["duration"] = record["end_time"] - record["start_time"]

    def analyse(self):
        """ Analysing the extracted data. """
        for record in self.device_onoff_records:
            if 'duration' in record:
                self.total_of_on_time += record["duration"]
        self.time_records.sort()
        self.start_time = self.time_records[0]
        self.end_time = self.time_records[-1]
        
        # print('total_of_on_time :', str(self.total_of_on_time))
        # print('device_onoff_records :', str(self.device_onoff_records))
        # print('device_error_records :', str(self.device_error_records))

    def store(self) -> str:
        """ Storing a result as a file and return the result file.
            Although it should be stored in DB, handling the data as a file for the test 
        """
        result_file_path = os.path.join(os.getcwd(), 'parsing_log', 'test_data', 'test.result')
        
        analysis = {"total_of_on_time":self.total_of_on_time,
                    "start_time": self.start_time,
                    "end_time": self.end_time,
                    "device_onoff_records":self.device_onoff_records,
                    "device_error_records":self.device_error_records}
        analysis = str(analysis)
        with open(result_file_path, 'w') as file:
            file.write(analysis)

        return result_file_path
    
    def _extract_time(self, line):
        time_str = line.split("[")[0]
        if time_str == None or time_str == "":
            raise ValueError("Format of data is wrong.")
        time_str = time_str.strip()

        return self._convert_time(time_str)


    def _convert_time(self, time_str):
        date_format = "%b %d %H:%M:%S:%f"
        try:
            time = datetime.strptime(time_str, date_format)
            time = time.replace(year=2023)
            return time
        except Exception as e:
            raise ValueError("Format of data is wrong.", e)
        
    def _extract_state(self, line):
        state_str = line.split(":")[-1]
        if state_str == None or state_str == "":
            raise ValueError("Format of data is wrong.")
        state = DeviceState.get_state_by_val(state_str.strip())
        if state == None:
            raise ValueError("Format of data is wrong.")
        return state
