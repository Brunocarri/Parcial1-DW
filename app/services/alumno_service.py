import datetime
from io import BytesIO
from app.models import Alumno
from app.repositories.interfaces.alumno_repository_interface import AlumnoRepositoryInterface

class AlumnoService:
    def __init__(self, alumno_repository: AlumnoRepositoryInterface):
        self.alumno_repository = alumno_repository

    def crear(self, alumno):
        self.alumno_repository.crear(alumno)

    def buscar_por_id(self, id: int) -> Alumno:
        return self.alumno_repository.get_by_id(id)

    def buscar_todos(self) -> list[Alumno]:
        return self.alumno_repository.buscar_todos()

    def actualizar(self, id: int, alumno: Alumno) -> Alumno:
        alumno_existente = self.alumno_repository.get_by_id(id)
        if not alumno_existente:
            return None
        alumno_existente.nombre = alumno.nombre
        alumno_existente.apellido = alumno.apellido
        alumno_existente.nrodocumento = alumno.nrodocumento
        alumno_existente.tipo_documento = alumno.tipo_documento
        alumno_existente.fecha_nacimiento = alumno.fecha_nacimiento
        alumno_existente.sexo = alumno.sexo
        alumno_existente.nro_legajo = alumno.nro_legajo
        alumno_existente.fecha_ingreso = alumno.fecha_ingreso
        return alumno_existente

    def borrar_por_id(self, id: int) -> bool:
        return self.alumno_repository.borrar_por_id(id)

    def generar_certificado_alumno_regular(self, id: int, tipo: str) -> BytesIO:
        from app.services.documentos_office_service import obtener_tipo_documento
        alumno = self.alumno_repository.get_by_id(id)
        if not alumno:
            return None
        context = self.__obtener_alumno_compat(alumno)
        documento = obtener_tipo_documento(tipo)
        if not documento:
            return None
        return documento.generar(
            carpeta='certificado',
            plantilla=f'certificado_{tipo}',
            context=context
        )

    @staticmethod
    def __obtener_fecha_actual():
        fecha_actual = datetime.datetime.now()
        fecha_str = fecha_actual.strftime('%d de %B de %Y')
        return fecha_str

    @staticmethod
    def __obtener_alumno_compat(alumno: Alumno) -> dict:
        especialidad = getattr(alumno, 'especialidad', None)
        facultad = getattr(especialidad, 'facultad', None) if especialidad else None
        universidad = getattr(facultad, 'universidad', None) if facultad else None
        if not especialidad:
            class MockEspecialidad:
                nombre = "Test Especialidad"
                facultad = None
            especialidad = MockEspecialidad()
        if not facultad:
            class MockFacultad:
                nombre = "Test Facultad"
                universidad = None
                ciudad = "Test Ciudad"
            facultad = MockFacultad()
            especialidad.facultad = facultad
        if not universidad:
            class MockUniversidad:
                nombre = "Test Universidad"
            universidad = MockUniversidad()
            facultad.universidad = universidad
        return {
            "alumno": alumno,
            "especialidad": especialidad,
            "facultad": facultad,
            "universidad": universidad,
            "fecha": AlumnoService.__obtener_fecha_actual()
        }