from abc import ABC, abstractmethod

class AbstractedDataAnalyser(ABC):

    @abstractmethod
    def analise_a_line(self, line):
        pass