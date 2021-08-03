from abc import ABC, abstractmethod

class WordInformationGetter(ABC):
    
    @abstractmethod
    def get_translation(self):
        pass
    
    @abstractmethod
    def get_definition(self):
        pass

    @abstractmethod
    def get_synonym(self):
        pass

    @abstractmethod
    def get_antonym(self):
        pass