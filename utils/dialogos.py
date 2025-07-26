import flet as ft

def mostrar_dialogo_exito(page, mensaje):
    dialog = ft.AlertDialog(
        title=ft.Text("Éxito"),
        content=ft.Text(mensaje),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page))]
    )
    page.dialog = dialog
    page.open(dialog)
    page.update()

def mostrar_dialogo_error(page, mensaje):
    dialog = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text(mensaje),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page))]
    )
    page.dialog = dialog
    page.open(dialog)
    page.update()

def mostrar_confirmacion(page, mensaje, on_confirmar):
    dialog = ft.AlertDialog(
        title=ft.Text("Confirmar"),
        content=ft.Text(mensaje),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(page)),
            ft.TextButton("Aceptar", on_click=lambda e: (cerrar_dialogo(page), on_confirmar()))
        ]
    )
    page.dialog = dialog
    page.open(dialog)
    page.update()

def cerrar_dialogo(page, e=None):
    if hasattr(page, "dialog") and page.dialog:
        page.dialog.open = False
        page.update()