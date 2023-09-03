from abc import ABC, abstractmethod

class AbstractedDataAnalyser(ABC):

    @abstractmethod
    def read_a_line(self, line: str):
        """ Reading a line of data and analysing it"""
        pass
    
    @abstractmethod
    def analyse(self):
        """ Analysing data after reading. """
        pass

    @abstractmethod
    def store(self):
        """ Storing a result of the analysis. """
        pass