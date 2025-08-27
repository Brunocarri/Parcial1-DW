from io import BytesIO
from app.models import Alumno
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class FichaAlumnoService:
    @staticmethod
    def generar_ficha_json(alumno: Alumno) -> dict:
        return {
            "nro_legajo": alumno.nro_legajo,
            "apellido": alumno.apellido,
            "nombre": alumno.nombre,
            "facultad": getattr(getattr(getattr(alumno, "especialidad", None), "facultad", None), "nombre", "Sin Facultad")
        }

    @staticmethod
    def generar_ficha_pdf(alumno: Alumno) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph(f"Ficha del Alumno", styles["Heading1"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Nro Legajo: {alumno.nro_legajo}", styles["Normal"]))
        story.append(Paragraph(f"Apellido: {alumno.apellido}", styles["Normal"]))
        story.append(Paragraph(f"Nombre: {alumno.nombre}", styles["Normal"]))
        facultad = getattr(getattr(getattr(alumno, "especialidad", None), "facultad", None), "nombre", "Sin Facultad")
        story.append(Paragraph(f"Facultad: {facultad}", styles["Normal"]))
        doc.build(story)
        buffer.seek(0)
        return buffer
