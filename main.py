import flet as ft
import asyncio

from Helpers.TimeHelpers import get_actual_day, get_actual_hour
from UdpClient import UdpClient


class DataDisplay:
    def __init__(self, page):
        self.progress_bar = ft.ProgressBar(width=200)
        self.data_columns = ft.Column(spacing=5)
        self.page = page
        self.client_udp = UdpClient(server_ip='udpserver.bu.ac.th', server_port=5005)
        self.create_layout()

    def create_layout(self):
        self.page.title = "Data Display"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.header = ft.Row(
            [
                ft.Text("Time", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Humidity", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Temperature", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Light", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Moisture", weight=ft.FontWeight.BOLD, expand=1),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        self.page.add(ft.Container(self.header, padding=10, bgcolor=ft.colors.BLUE_GREY_900, border_radius=5))
        self.page.add(ft.Container(self.data_columns, padding=10, border_radius=5, bgcolor=ft.colors.BLUE_GREY_800))
        self.page.add(ft.Container(self.progress_bar, padding=10))
        self.page.update()

    async def retrieve_data(self):
        id_str = f"farm2000_" + str(get_actual_day())
        response = await self.client_udp.retrieve_data(command="GET", id_str=id_str)
        hour = get_actual_hour()

        if hour in response:
            return response

        return {f"{hour}": {"HUMIDITY": 0, "TEMPERATURE": 0, "LIGHT": 0, "MOISTURE": 0}}

    async def update_data(self):
        while True:
            try:
                response = await self.retrieve_data()

                # Réinitialiser la barre de progression
                self.progress_bar.value = 1

                self.display_data(response)
            except Exception as e:
                print(f"Error retrieving data: {e}")

            # Démarrage de la barre de progression (attendre 10secondes)
            for i in range(0, 100, 1):
                self.progress_bar.value = i / 100
                self.page.update()
                await asyncio.sleep(0.03)

    def display_data(self, data):
        self.data_columns.controls.clear()

        for time, values in data.items():
            is_current_time = time == get_actual_hour()
            row = ft.Row(
                [
                    ft.Text(f"{time} H", expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{values['HUMIDITY']} %",expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{values['TEMPERATURE']} °C",expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{values['LIGHT']} %",expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{values['MOISTURE']} %",expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
            self.data_columns.controls.append(row)
        self.page.update()


async def main(page: ft.Page):
    data_display = DataDisplay(page)
    await data_display.update_data()

ft.app(target=main)