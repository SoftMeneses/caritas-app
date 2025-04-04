import flet as ft
from datetime import date, datetime
import calendar

class CalendarioApp:
    def __init__(self, pagina: ft.Page):
        self.pagina = pagina
        # Paleta de colores
        self.cherry = "#660924"
        self.wine = "#630D13"
        
        # Configuración inicial
        self._configurar_pagina()
        self._inicializar_datos()
        self._crear_controles()
        self._construir_interfaz()
        self._actualizar_calendario()
        self._mostrar_eventos(self.fecha_seleccionada)

    def _configurar_pagina(self):
        """Configura las propiedades básicas de la página"""
        self.pagina.title = "Calendario de Eventos"
        self.pagina.window_min_width = 1000
        self.pagina.window_min_height = 700
        self.pagina.bgcolor = "#121212"
        self.pagina.padding = 0

    def _inicializar_datos(self):
        """Inicializa las variables de estado de la aplicación"""
        self.hoy = date.today()
        self.ano_actual = self.hoy.year
        self.mes_actual = self.hoy.month
        self.fecha_seleccionada = f"{self.hoy.day} {self._nombre_mes(self.mes_actual)} {self.ano_actual}"
        self.eventos = {}  # Diccionario para almacenar eventos por fecha
        self.eventos_expandidos = {}  # Controla qué eventos están expandidos

    def _nombre_mes(self, mes):
        """Devuelve el nombre del mes correspondiente al número"""
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return meses[mes-1]

    def _crear_controles(self):
        """Crea todos los controles de la interfaz de usuario"""
        
        # Barra de navegación lateral
        self.navigation_container = ft.Container(
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

        # Controles del calendario (expandible/colapsable)
        self.icono_expandir = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            icon_color="white70",
            on_click=self._alternar_calendario
        )
        
        self.icono_contraer = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            icon_color="white70",
            visible=False,
            on_click=self._alternar_calendario
        )
        
        self.txt_mes_ano = ft.Text(size=16, weight="bold", color="white70")
        self.columna_dias = ft.Column(spacing=0, alignment=ft.MainAxisAlignment.CENTER)
        
        # Controles de eventos
        self.txt_titulo_eventos = ft.Text("Eventos Programados", color="white70", weight="bold")
        self.campo_evento = ft.TextField(hint_text="Añadir nuevo evento...", expand=True)
        self.btn_agregar = ft.IconButton(icon=ft.Icons.ADD_CIRCLE, on_click=self._agregar_evento)
        self.lista_eventos = ft.Column(scroll="auto", expand=True, spacing=10)
        self.txt_fecha = ft.Text(self.fecha_seleccionada, color="white70")

    def _construir_interfaz(self):
        """Construye la estructura principal de la interfaz"""
        
        # Contenedor del calendario (colapsable)
        self.contenedor_calendario = ft.Container(
            width=40,
            bgcolor="#1a1a2e",
            border_radius=ft.border_radius.only(top_left=15, bottom_left=15),
            padding=10,
            content=ft.Column(
                controls=[
                    self.icono_expandir,
                    ft.Column(
                        visible=False,
                        controls=[
                            # Controles de navegación del mes
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS, on_click=lambda e: self._cambiar_mes(-1)),
                                    self.txt_mes_ano,
                                    ft.IconButton(icon=ft.Icons.ARROW_FORWARD_IOS, on_click=lambda e: self._cambiar_mes(1))
                                ],
                                alignment="center"
                            ),
                            # Encabezados de días de la semana
                            ft.Row(
                                controls=[
                                    ft.Container(width=40, content=ft.Text(dia, size=12, text_align="center")) 
                                    for dia in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
                                ],
                                spacing=0,
                                alignment="center"
                            ),
                            # Contenedor de los días del mes
                            ft.Container(
                                content=self.columna_dias, 
                                padding=5,
                                alignment=ft.alignment.center
                            ),
                            self.icono_contraer
                        ],
                        spacing=10,
                        alignment="center",
                        horizontal_alignment="center"
                    )
                ],
                spacing=10,
                alignment="center",
                horizontal_alignment="center"
            ),
            animate=ft.animation.Animation(300, "decelerate")
        )

        # Contenedor principal de eventos
        self.contenedor_eventos = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row([self.txt_titulo_eventos, ft.Container(expand=True), self.txt_fecha]),
                    ft.Divider(height=10),
                    ft.Row([self.campo_evento, self.btn_agregar]),
                    ft.Divider(height=20),
                    self.lista_eventos
                ]
            )
        )

        # Contenedor principal de la aplicación
        self.main_container = ft.Row(
            controls=[
                self.navigation_container,
                self.contenedor_eventos,
                self.contenedor_calendario
            ],
            expand=True
        )

        self.pagina.add(self.main_container)

    def _alternar_calendario(self, e):
        """Alterna entre calendario expandido y colapsado"""
        if self.contenedor_calendario.width == 40:
            # Expandir calendario
            self.contenedor_calendario.width = 350
            self.icono_expandir.visible = False
            self.contenedor_calendario.content.controls[1].visible = True
            self.icono_contraer.visible = True
        else:
            # Colapsar calendario
            self.contenedor_calendario.width = 40
            self.icono_expandir.visible = True
            self.contenedor_calendario.content.controls[1].visible = False
            self.icono_contraer.visible = False
        self.pagina.update()

    def _actualizar_calendario(self):
        """Actualiza la visualización del calendario para el mes/año actual"""
        self.txt_mes_ano.value = f"{self._nombre_mes(self.mes_actual)} {self.ano_actual}"
        self.columna_dias.controls.clear()
        
        calendario = calendar.Calendar()
        semanas = calendario.monthdayscalendar(self.ano_actual, self.mes_actual)
        
        for semana in semanas:
            fila = ft.Row(spacing=0, alignment="center")
            for dia in semana:
                celda = ft.Container(
                    width=40,
                    height=40,
                    margin=2,
                    border_radius=8,
                    alignment=ft.alignment.center,
                    animate=ft.animation.Animation(200, "easeInOut"),
                    on_hover=self._resaltar_dia,
                    on_click=lambda e, d=dia: self._seleccionar_dia(d) if d != 0 else None
                )
                
                if dia == 0:
                    # Día fuera del mes actual
                    celda.bgcolor = "#1a1a2e"
                else:
                    fecha_str = f"{dia} {self._nombre_mes(self.mes_actual)} {self.ano_actual}"
                    es_hoy = (dia == self.hoy.day and self.mes_actual == self.hoy.month and self.ano_actual == self.hoy.year)
                    seleccionado = self.fecha_seleccionada == fecha_str
                    tiene_eventos = len(self.eventos.get(fecha_str, [])) > 0
                    
                    # Establecer color según el estado del día
                    celda.bgcolor = "#42a5f5" if seleccionado else "#0f3460" if es_hoy else "#16213e"
                    celda.content = ft.Container(
                        width=36,
                        height=36,
                        border=ft.border.all(color="#ef4444" if tiene_eventos else "transparent", width=2),
                        border_radius=8,
                        content=ft.Text(
                            str(dia), 
                            color="white" if es_hoy or seleccionado else "white70",
                            text_align="center"
                        )
                    )
                    celda.data = {"fecha": fecha_str, "dia": dia, "es_hoy": es_hoy}
                
                fila.controls.append(celda)
            self.columna_dias.controls.append(fila)
        
        self.txt_mes_ano.update()
        self.columna_dias.update()

    def _resaltar_dia(self, e):
        """Resalta visualmente el día cuando el cursor pasa sobre él"""
        if e.control.data and e.control.data.get("dia", 0) != 0:
            e.control.bgcolor = "#1e88e5" if e.data == "true" else (
                "#42a5f5" if self.fecha_seleccionada == e.control.data["fecha"] else
                "#0f3460" if e.control.data["es_hoy"] else "#16213e"
            )
            e.control.update()

    def _seleccionar_dia(self, dia):
        """Selecciona un día específico en el calendario"""
        self.fecha_seleccionada = f"{dia} {self._nombre_mes(self.mes_actual)} {self.ano_actual}"
        self.txt_fecha.value = self.fecha_seleccionada
        self._actualizar_calendario()
        self._mostrar_eventos(self.fecha_seleccionada)
        self._alternar_calendario(None)

    def _cambiar_mes(self, delta):
        """Cambia al mes anterior o siguiente"""
        self.mes_actual += delta
        if self.mes_actual > 12:
            self.mes_actual = 1
            self.ano_actual += 1
        elif self.mes_actual < 1:
            self.mes_actual = 12
            self.ano_actual -= 1
        self._actualizar_calendario()

    def _crear_item_evento(self, evento, fecha_str, indice):
        """Crea un elemento visual para un evento en la lista"""
        evento_id = f"{fecha_str}_{indice}"
        if evento_id not in self.eventos_expandidos:
            self.eventos_expandidos[evento_id] = False
            
        fecha_creacion = evento.get("fecha_creacion", datetime.now())
        if isinstance(fecha_creacion, str):
            fecha_creacion = datetime.strptime(fecha_creacion, "%Y-%m-%d %H:%M:%S")
        
        # Crear columna de detalles (visible solo cuando el evento está expandido)
        detalles_column = ft.Column(spacing=5, visible=self.eventos_expandidos[evento_id])
        for det_idx, detalle in enumerate(evento["detalles"]):
            detalles_column.controls.append(
                ft.Row(
                    controls=[
                        ft.Checkbox(value=detalle.get("completado", False)),
                        ft.Text(
                            detalle["texto"], 
                            expand=True, 
                            style=ft.TextStyle(
                                decoration=ft.TextDecoration.LINE_THROUGH if detalle.get("completado", False) else None
                            )
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE, 
                            icon_size=16, 
                            on_click=lambda e, idx=det_idx: self._eliminar_detalle(e, fecha_str, indice, idx)
                        )
                    ],
                    spacing=10
                )
            )
        
        return ft.Container(
            bgcolor="#1e293b",
            border_radius=8,
            padding=12,
            content=ft.Column(
                controls=[
                    # Fila principal del evento
                    ft.Row(
                        controls=[
                            # Checkbox para marcar como completado
                            ft.Checkbox(
                                value=evento.get("completado", False),
                                on_change=lambda e, fs=fecha_str, i=indice: self._alternar_evento(e, fs, i)
                            ),
                            # Columna con texto del evento y fecha de creación
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        evento["texto"], 
                                        expand=True, 
                                        style=ft.TextStyle(
                                            decoration=ft.TextDecoration.LINE_THROUGH if evento.get("completado", False) else None
                                        )
                                    ),
                                    ft.Text(
                                        f"Creado: {fecha_creacion.strftime('%d/%m/%Y %H:%M')}", 
                                        color="white54", 
                                        size=12
                                    )
                                ],
                                expand=True
                            ),
                            # Botones de acción
                            ft.IconButton(
                                icon=ft.icons.DELETE, 
                                on_click=lambda e: self._eliminar_evento(e, fecha_str, indice)
                            ),
                            ft.IconButton(
                                icon=ft.icons.KEYBOARD_ARROW_DOWN if not self.eventos_expandidos[evento_id] else ft.icons.KEYBOARD_ARROW_UP,
                                on_click=lambda e: self._alternar_detalles(e, evento_id, fecha_str, indice)
                            )
                        ]
                    ),
                    # Detalles del evento (mostrados cuando está expandido)
                    detalles_column,
                    # Fila para agregar nuevos detalles
                    ft.Row(
                        controls=[
                            ft.TextField(
                                hint_text="Añadir detalle...", 
                                expand=True, 
                                visible=self.eventos_expandidos[evento_id]
                            ),
                            ft.IconButton(
                                icon=ft.icons.ADD, 
                                visible=self.eventos_expandidos[evento_id], 
                                on_click=lambda e: self._agregar_detalle(e, fecha_str, indice)
                            )
                        ],
                        visible=self.eventos_expandidos[evento_id]
                    )
                ],
                spacing=5
            )
        )

    def _mostrar_eventos(self, fecha_str):
        """Muestra los eventos para la fecha seleccionada"""
        self.lista_eventos.controls.clear()
        if fecha_str in self.eventos:
            for i, evento in enumerate(self.eventos[fecha_str]):
                self.lista_eventos.controls.append(self._crear_item_evento(evento, fecha_str, i))
        self.lista_eventos.update()

    def _agregar_evento(self, e):
        """Agrega un nuevo evento a la fecha seleccionada"""
        if texto := self.campo_evento.value.strip():
            if self.fecha_seleccionada not in self.eventos:
                self.eventos[self.fecha_seleccionada] = []
            
            self.eventos[self.fecha_seleccionada].append({
                "texto": texto,
                "completado": False,
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "detalles": []
            })
            
            self.campo_evento.value = ""
            self._mostrar_eventos(self.fecha_seleccionada)
            self._actualizar_calendario()

    def _alternar_evento(self, e, fecha_str, indice):
        """Alterna el estado completado/no completado de un evento"""
        if fecha_str in self.eventos and indice < len(self.eventos[fecha_str]):
            self.eventos[fecha_str][indice]["completado"] = e.control.value
            self._mostrar_eventos(fecha_str)
            self._actualizar_calendario()

    def _eliminar_evento(self, e, fecha_str, indice):
        """Elimina un evento de la lista"""
        if fecha_str in self.eventos and indice < len(self.eventos[fecha_str]):
            del self.eventos[fecha_str][indice]
            self._mostrar_eventos(fecha_str)
            self._actualizar_calendario()

    def _alternar_detalles(self, e, evento_id, fecha_str, indice_evento):
        """Alterna la visualización de los detalles de un evento"""
        self.eventos_expandidos[evento_id] = not self.eventos_expandidos[evento_id]
        self._mostrar_eventos(fecha_str)

    def _agregar_detalle(self, e, fecha_str, indice_evento):
        """Agrega un nuevo detalle a un evento"""
        for control in self.lista_eventos.controls[indice_evento].content.controls:
            if isinstance(control, ft.Row) and len(control.controls) == 2:
                if texto := control.controls[0].value.strip():
                    self.eventos[fecha_str][indice_evento]["detalles"].append({
                        "texto": texto, 
                        "completado": False
                    })
                    control.controls[0].value = ""
                    self._mostrar_eventos(fecha_str)
                break

    def _eliminar_detalle(self, e, fecha_str, indice_evento, indice_detalle):
        """Elimina un detalle de un evento"""
        if (fecha_str in self.eventos and 
            indice_evento < len(self.eventos[fecha_str]) and 
            indice_detalle < len(self.eventos[fecha_str][indice_evento]["detalles"])):
            del self.eventos[fecha_str][indice_evento]["detalles"][indice_detalle]
            self._mostrar_eventos(fecha_str)

def main(pagina: ft.Page):
    """Función principal que inicia la aplicación"""
    CalendarioApp(pagina)

ft.app(target=main)