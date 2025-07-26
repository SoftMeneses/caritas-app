from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import flet as ft
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

# Abrevia días de la semana
def abreviar_dias(texto):
    if not isinstance(texto, str):
        return texto
    dias_completos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_abrev = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    partes = [p.strip() for p in texto.split(',') if p.strip() in dias_completos]
    if set(partes) == set(dias_completos[:5]):
        return "Lun-Vie"
    elif set(partes) == set(dias_completos[5:]):
        return "Fines de semana"
    elif set(partes) == set(dias_completos):
        return "Todos los días"
    abreviados = []
    for dia in partes:
        if dia in dias_completos:
            i = dias_completos.index(dia)
            abreviados.append(dias_abrev[i])
    return ", ".join(abreviados)

# Menbrete con logo y título institucional
def dibujar_menbrete(c):
    try:
        # Ruta absoluta al logo, relativa a la carpeta del archivo actual
        ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'views', 'assets', 'logo_main_caritas.png')
        ruta_logo = os.path.abspath(ruta_logo)
        imagen = ImageReader(ruta_logo)
        c.drawImage(imagen, 40, 740, width=120, height=50, mask='auto')  # 'mask=auto' trata transparencias
    except Exception as e:
        print(f"No se pudo insertar el logo: {e}")

    c.setFont("Helvetica-Bold", 14)
    texto = "CÁRITAS PARROQUIAL"
    ancho_texto = c.stringWidth(texto, "Helvetica-Bold", 14)
    pagina_ancho, _ = letter
    posicion_x = (pagina_ancho - ancho_texto) / 2
    c.drawString(posicion_x, 745, texto)

    c.setLineWidth(1)
    c.line(40, 715, 550, 715)

def poner_fecha_creacion(c):
    fecha_hora = datetime.now().strftime("Creado el %d/%m/%Y a las %H:%M:%S")
    pagina_ancho, pagina_alto = letter
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(pagina_ancho - 40, 30, fecha_hora)

def mostrar_confirmacion_impresion(page, mensaje, funcion_imprimir):
    dialog = ft.AlertDialog(
        title=ft.Text("Confirmar impresión"),
        content=ft.Text(mensaje),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.TextButton("Imprimir", on_click=lambda e: funcion_imprimir())
        ]
    )
    page.dialog = dialog
    page.open(dialog)
    page.update()

def mostrar_exito_impresion(page, ruta_pdf):
    exito_dialog = ft.AlertDialog(
        title=ft.Text("Éxito"),
        content=ft.Text(f"Archivo guardado exitosamente en:\n{ruta_pdf}"),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page))]
    )
    page.success_dialog = exito_dialog
    page.open(exito_dialog)
    page.update()

def cerrar_dialogo(page, e=None):
    for attr in ['dialog', 'dgElim', 'success_dialog', 'error_dialog']:
        if hasattr(page, attr):
            dialog = getattr(page, attr)
            if hasattr(dialog, 'open') and dialog.open:
                dialog.open = False
    page.update()

# =============================
# Funciones de creación de PDF
# =============================

def crear_pdf_blanco(nombre_archivo="salida.pdf"):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    poner_fecha_creacion(c)
    c.showPage()
    c.save()

def crear_pdf_listado_donantes(nombre_archivo, donantes):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Listado General de Donantes")
    c.setFont("Helvetica-Bold", 12)
    y = 690
    c.drawString(50, y, "Nombre")
    c.drawString(160, y, "Teléfono")
    c.drawString(270, y, "Email")
    c.drawString(420, y, "Cédula")
    y -= 25
    c.setFont("Helvetica", 11)
    for d in donantes:
        c.drawString(50, y, str(d[1])[:18])
        c.drawString(160, y, str(d[2]))
        c.drawString(270, y, str(d[3])[:30])
        c.drawString(420, y, str(d[4]))
        y -= 18
        if y < 50:
            poner_fecha_creacion(c)
            c.showPage()
            dibujar_menbrete(c)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 720, "Listado General de Donantes")
            y = 690
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_detalle_donante(nombre_archivo, donante):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Detalle del Donante")
    c.setFont("Helvetica", 12)
    y = 690
    campos = ["ID", "Nombre", "Teléfono", "Email", "Cédula", "Dirección", "Última Donación"]
    for i, campo in enumerate(campos):
        c.drawString(50, y, f"{campo}: {donante[i]}")
        y -= 25
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_listado_donaciones(nombre_archivo, donaciones):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Listado General de Donaciones")
    c.setFont("Helvetica-Bold", 12)
    y = 690
    c.drawString(50, y, "Fecha")
    c.drawString(110, y, "Donante")
    c.drawString(230, y, "Tipo")
    c.drawString(330, y, "Descripción")
    y -= 25
    c.setFont("Helvetica", 11)
    for d in donaciones:
        c.drawString(50, y, str(d['FECHA']))
        c.drawString(110, y, str(d['NOMBRE'])[:18])
        tipos = ", ".join([detalle.get("TIPO", "") for detalle in d.get("detalles", [])])
        c.drawString(230, y, tipos[:20])
        c.drawString(330, y, str(d['DESCRI'])[:40])
        y -= 18
        if y < 50:
            poner_fecha_creacion(c)
            c.showPage()
            dibujar_menbrete(c)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 720, "Listado General de Donaciones")
            y = 690
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_detalle_donacion(nombre_archivo, donacion):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Detalle de Donación")
    c.setFont("Helvetica", 12)
    y = 690
    campos = [
        ("Fecha", donacion['FECHA']),
        ("Donante", donacion['NOMBRE']),
        ("Descripción", donacion['DESCRI']),
        ("Cédula", donacion.get('CEDULA', '')),
        ("Teléfono", donacion.get('TELEFONO', '')),
        ("Email", donacion.get('CORREO', '')),
        ("Dirección", donacion.get('DIRECCION', '')),
    ]
    for campo, valor in campos:
        c.drawString(50, y, f"{campo}: {valor}")
        y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detalles:")
    y -= 18
    c.setFont("Helvetica", 11)
    for detalle in donacion.get('detalles', []):
        linea = f"- {detalle.get('TIPO', '')}: "
        if detalle.get('TIPO') == "Monetaria":
            linea += f"Monto: {detalle.get('MONTO', '')}, Método: {detalle.get('METODO_PAGO', '')}"
        elif detalle.get('TIPO') in ["Alimentos", "Medicamentos"]:
            linea += f"{detalle.get('DESCRIPCION', '')}, Cantidad: {detalle.get('CANTIDAD', '')}"
        c.drawString(60, y, linea[:90])
        y -= 16
        if y < 50:
            poner_fecha_creacion(c)
            c.showPage()
            dibujar_menbrete(c)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 720, "Detalle de Donación")
            y = 690
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_listado_voluntarios(nombre_archivo, voluntarios):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Listado General de Voluntarios")
    c.setFont("Helvetica-Bold", 12)
    y = 690
    c.drawString(50, y, "Nombre")
    c.drawString(160, y, "Cédula")
    c.drawString(250, y, "Teléfono")
    c.drawString(350, y, "Email")
    c.drawString(490, y, "Disp.")
    y -= 25
    c.setFont("Helvetica", 11)
    for v in voluntarios:
        c.drawString(50, y, str(v[1])[:18])
        c.drawString(160, y, str(v[2]))
        c.drawString(250, y, str(v[3]))
        c.drawString(350, y, str(v[4])[:25])
        disponibilidad = abreviar_dias(str(v[5]))
        c.drawString(490, y, disponibilidad[:20])
        y -= 18
        if y < 50:
            poner_fecha_creacion(c)
            c.showPage()
            dibujar_menbrete(c)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 720, "Listado General de Voluntarios")
            y = 690
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_detalle_voluntario(nombre_archivo, voluntario):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Detalle del Voluntario")
    c.setFont("Helvetica", 12)
    y = 690
    campos = ["ID", "Nombre", "Cédula", "Teléfono", "Email", "Disponibilidad"]
    for i, campo in enumerate(campos):
        valor = abreviar_dias(voluntario[i]) if campo == "Disponibilidad" else voluntario[i]
        c.drawString(50, y, f"{campo}: {valor}")
        y -= 22
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_listado_jornadas(nombre_archivo, jornadas):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Listado General de Jornadas")
    c.setFont("Helvetica-Bold", 12)
    y = 690
    c.drawString(50, y, "Fecha")
    c.drawString(130, y, "Descripción")
    c.drawString(330, y, "Ubicación")
    c.drawString(490, y, "Estatus")
    y -= 25
    c.setFont("Helvetica", 11)
    for j in jornadas:
        fecha = abreviar_dias(str(j[1]))
        c.drawString(50, y, fecha)
        c.drawString(130, y, str(j[2])[:25])
        c.drawString(330, y, str(j[3])[:25])
        c.drawString(490, y, str(j[4]))
        y -= 18
        if y < 50:
            poner_fecha_creacion(c)
            c.showPage()
            dibujar_menbrete(c)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 720, "Listado General de Jornadas")
            y = 690
    poner_fecha_creacion(c)
    c.save()

def crear_pdf_detalle_jornada(nombre_archivo, jornada, voluntarios=None, recursos=None, observacion=None):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    dibujar_menbrete(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 720, "Detalle de Jornada")
    c.setFont("Helvetica", 12)
    y = 690
    campos = [
        ("ID", jornada[0]),
        ("Fecha", abreviar_dias(jornada[1])),
        ("Descripción", jornada[2]),
        ("Ubicación", jornada[3]),
        ("Estatus", jornada[4])
    ]
    for campo, valor in campos:
        c.drawString(50, y, f"{campo}: {valor}")
        y -= 22
    if voluntarios:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Voluntarios:")
        y -= 18
        c.setFont("Helvetica", 11)
        for v in voluntarios:
            c.drawString(60, y, f"- {v[1][:18]} ({abreviar_dias(v[2])})")
            y -= 16
            if y < 50:
                poner_fecha_creacion(c)
                c.showPage()
                dibujar_menbrete(c)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 720, "Detalle de Jornada")
                y = 690
    if recursos:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Recursos Utilizados:")
        y -= 18
        c.setFont("Helvetica", 11)
        for r in recursos:
            c.drawString(60, y, f"- {r['TIPO']}: {r['DESCRIPCION']} ({r['CANTIDAD_UTILIZADA']})")
            y -= 16
            if y < 50:
                poner_fecha_creacion(c)
                c.showPage()
                dibujar_menbrete(c)
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, 720, "Detalle de Jornada")
                y = 690
    if observacion:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Observación:")
        y -= 18
        c.setFont("Helvetica", 11)
        c.drawString(60, y, str(observacion)[:90])
        y -= 16
    poner_fecha_creacion(c)
    c.save()