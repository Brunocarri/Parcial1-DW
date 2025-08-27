from abc import ABC, abstractmethod

class AlumnoRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, alumno_id):
        pass

    @abstractmethod
    def save(self, alumno):
        pass

    # ...otros métodos necesarios...