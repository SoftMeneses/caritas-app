import flet as ft

class NavBar:
    def __init__(self, cherry="#660924", wine="#630D13"):
        self.cherry = cherry
        self.wine = wine

        self.view = ft.Container(
            gradient=ft.LinearGradient(
                colors=[self.wine, self.cherry],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ),
            width=80,
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.NavigationRail(
                            bgcolor="transparent",
                            selected_index=0,
                            destinations=[
                                ft.NavigationRailDestination(
                                    icon=ft.Icons.HOME,
                                    selected_icon_content=ft.Icon(ft.Icons.HOME, color="white"),
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.Icons.ATTACH_MONEY_OUTLINED,
                                    selected_icon_content=ft.Icon(ft.Icons.ATTACH_MONEY_OUTLINED, color="white"),
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.Icons.CALENDAR_MONTH_SHARP,
                                    selected_icon_content=ft.Icon(ft.Icons.CALENDAR_MONTH_SHARP, color="white"),
                                ),
                                ft.NavigationRailDestination(
                                    icon=ft.Icons.SETTINGS,
                                    selected_icon_content=ft.Icon(ft.Icons.SETTINGS, color="white"),
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.IconButton(icon=ft.Icons.OUTPUT, icon_color="white")
                            ]
                        ),
                    ),
                ]
            )
        )
