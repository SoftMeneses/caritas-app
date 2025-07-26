import flet as ft

class NavBar:
    def __init__(self, page, navegar, cherry="#660924", wine="#630D13"):
        self.page = page  
        self.navegar = navegar 
        self.cherry = cherry
        self.wine = wine
        self.usuario = page.session.get("usuario")
        self.nombre = self.usuario.get("USUARIO") if self.usuario else ""
        self.dlg_modal = self.create_dialog()
        self.selected_index = 0  

        # Construcción dinámica de los items del menú
        menu_items = [
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME),
                    title=ft.Text("Inicio", color="white"),
                    on_click=lambda e: self.navegar(0),
                ),
                on_hover=self.animar
            ),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.GROUP_ADD_ROUNDED),
                    title=ft.Text("Donantes", color="white"),
                    on_click=lambda e: self.navegar(1),
                    selected=self.selected_index == 1,
                ),
                on_hover=self.animar
            ),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.FORMAT_LIST_BULLETED_ADD),
                    title=ft.Text("Donaciones", color="white"),
                    on_click=lambda e: self.navegar(2),
                    selected=self.selected_index == 2,
                ),
                on_hover=self.animar
            ),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.GROUPS_ROUNDED),
                    title=ft.Text("Voluntarios", color="white"),
                    on_click=lambda e: self.navegar(3),
                    selected=self.selected_index == 3,
                ),
                on_hover=self.animar
            ),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.EDIT_CALENDAR_ROUNDED),
                    title=ft.Text("Jornadas", color="white"),
                    on_click=lambda e: self.navegar(4),
                    selected=self.selected_index == 4,
                ),
                on_hover=self.animar
            )
        ]
        # Solo agrega "Ajustes" si el usuario es admin
        if self.nombre and str(self.nombre).lower() == "admin":
            menu_items.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.SETTINGS),
                        title=ft.Text("Ajustes", color="white"),
                        on_click=lambda e: self.navegar(5),
                        selected=self.selected_index == 5,
                    ),
                    on_hover=self.animar
                )
            )
        self.view = ft.Container(
            gradient=ft.LinearGradient(
                colors=[self.wine, self.cherry],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ),
            width=200,
            height=1200,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.padding.only(top=80),
                        content=ft.Column(
                            controls=menu_items
                        )
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.Text(self.nombre, size=14, color="white"),
                                        ft.IconButton(icon=ft.Icons.OUTPUT, icon_color="white", on_click=lambda e: self.page.open(self.dlg_modal)),
                                    ]
                                )
                            ]
                        ),
                        on_hover=self.animar
                    )
                ]
            )
        )

    def animar(self, e):
        if e.data == "true":
            e.control.scale = ft.Scale(1.05)
        else:
            e.control.scale = ft.Scale(1.0)
        e.control.update()

    def create_dialog(self):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Estás Seguro?"),
            content=ft.Text("¿Deseas Salir de la Aplicación?"),
            actions=[
                ft.TextButton("Sí", on_click=self.salir_programa),
                ft.TextButton("No", on_click=self.cerrar_dialogo),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        return dlg_modal

    def salir_programa(self, e):
        self.page.window.close()

    def cerrar_dialogo(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def on_navigation_change(self, e):
        self.selected_index = e.control.selected_index  
        print(f"Índice seleccionado: {self.selected_index}")
        self.page.update()  
        self.navegar(self.selected_index)
