from app import db
from app.models import Alumno
from app.repositories.interfaces.alumno_repository_interface import AlumnoRepositoryInterface

class AlumnoRepository(AlumnoRepositoryInterface):
    def crear(self, alumno):
        """
        Crea un nuevo alumno en la base de datos.
        """
        db.session.add(alumno)
        db.session.commit()

    def get_by_id(self, alumno_id):
        """
        Busca un alumno por su id.
        """
        return db.session.query(Alumno).filter_by(id=alumno_id).first()

    def buscar_todos(self):
        """
        Busca todos los alumnos.
        """
        return db.session.query(Alumno).all()

    def actualizar(self, alumno):
        """
        Actualiza un alumno en la base de datos.
        """
        alumno_existente = db.session.merge(alumno)
        if not alumno_existente:
            return None
        db.session.commit()
        return alumno_existente

    def borrar_por_id(self, id):
        """
        Borra un alumno por su id.
        """
        alumno = db.session.query(Alumno).filter_by(id=id).first()
        if not alumno:
            return None
        db.session.delete(alumno)
        db.session.commit()
        return alumno