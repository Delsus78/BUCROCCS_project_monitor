import flet as ft
import asyncio

from Helpers.TimeHelpers import get_actual_day, get_actual_hour, get_actual_day_as_int, get_actual_day_from_int
from UdpClient import UdpClient


class DataDisplay:
    def __init__(self, page):
        self.progress_bar = ft.ProgressBar(width=200)
        self.data_columns = ft.Column(spacing=5)
        self.page = page
        self.day = get_actual_day()
        self.client_udp = UdpClient(server_ip='udpserver.bu.ac.th', server_port=5005)
        self.create_layout()

    async def change_day(self, event):
        day_index = int(event.data)
        day = get_actual_day_from_int(day_index)

        self.day = day
        await self.update_data()

    def create_layout(self):
        self.page.title = "Data Display"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # create a tab for selecting the day
        tabOfDays = ft.Tabs(
            selected_index=get_actual_day_as_int() - 1,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Monday"),
                ft.Tab(text="Tuesday"),
                ft.Tab(text="Wednesday"),
                ft.Tab(text="Thursday"),
                ft.Tab(text="Friday"),
                ft.Tab(text="Saturday"),
                ft.Tab(text="Sunday")
            ],
            expand=1
        )

        # add a callback to the tab
        tabOfDays.on_change = self.change_day

        self.header = ft.Row(
            [
                ft.Text("Time", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Humidity", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Temperature", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Light", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Moisture", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Light Activated", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Pump Activated", weight=ft.FontWeight.BOLD, expand=1),
                ft.Text("Pump Activated This Hour", weight=ft.FontWeight.BOLD, expand=1),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

        self.page.add(ft.Container(tabOfDays, padding=10, border_radius=5, bgcolor=ft.colors.BLUE_GREY))
        self.page.add(ft.Container(self.header, padding=10, bgcolor=ft.colors.BLUE_GREY_900, border_radius=5))
        self.page.add(ft.Container(self.data_columns, padding=10, border_radius=5, bgcolor=ft.colors.BLUE_GREY_800))
        self.page.add(ft.Container(self.progress_bar, padding=10))
        self.page.update()

    async def retrieve_data(self):
        daySelected = self.day

        id_str = f"farm2000_" + str(daySelected)
        response = await self.client_udp.retrieve_data(command="GET", id_str=id_str)
        hour = get_actual_hour()

        if hour in response:
            return response

        return {f"{hour}": {"HUMIDITY": 0, "TEMPERATURE": 0, "LIGHT": 0, "MOISTURE": 0, "LIGHTSTATE": False, "PUMPSTATE": False, "PUMPWASACTIVATEDTHISHOUR": False}}

    async def update_data(self):
        response = await self.retrieve_data()

        # Réinitialiser la barre de progression
        self.progress_bar.value = 1

        self.display_data(response)

    async def loop_data(self):
        while True:
            try:
                await self.update_data()
            except Exception as e:
                print(f"Error retrieving data: {e}")

            # Démarrage de la barre de progression (attendre 10secondes)
            for i in range(0, 100, 1):
                self.progress_bar.value = i / 100
                self.page.update()
                await asyncio.sleep(0.03)

    def display_data(self, data):
        self.data_columns.controls.clear()

        # trier les données par heure
        data = dict(sorted(data.items(), key=lambda x: int(x[0])))

        for time, values in data.items():
            is_current_time = time == get_actual_hour() and get_actual_day() == self.day

            humidity = "%.2f" % values['HUMIDITY'] if values.get('HUMIDITY') else 0
            temperature = "%.2f" % values['TEMPERATURE'] if values.get('TEMPERATURE') else 0
            light = "%.2f" % values['LIGHT'] if values.get('LIGHT') else 0
            moisture = "%.2f" % values['MOISTURE'] if values.get('MOISTURE') else 0
            if values.get('LIGHTSTATE') is not None:
                light_state = "ON" if values['LIGHTSTATE'] else "OFF"
                light_state_color = ft.colors.GREEN if values['LIGHTSTATE'] else ft.colors.RED
            else:
                light_state = "NONE"
                light_state_color = ft.colors.GREY

            if values.get('PUMPSTATE') is not None:
                pump_state = "ON" if values['PUMPSTATE'] else "OFF"
                pump_state_color = ft.colors.GREEN if values['PUMPSTATE'] else ft.colors.RED
            else:
                pump_state = "NONE"
                pump_state_color = ft.colors.GREY

            if values.get('PUMPWASACTIVATEDTHISHOUR') is not None:
                pump_activated_this_hour_state = "ON" if values['PUMPWASACTIVATEDTHISHOUR'] else "OFF"
                pump_activated_this_hour_color = ft.colors.GREEN if values['PUMPWASACTIVATEDTHISHOUR'] else ft.colors.RED
            else:
                pump_activated_this_hour_state = "NONE"
                pump_activated_this_hour_color = ft.colors.GREY

            row = ft.Row(
                [
                    ft.Text(f"{time} H", expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{humidity} %", expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{temperature} °C", expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{light} %", expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(f"{moisture} %", expand=1, color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(light_state, expand=1, color=light_state_color,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(pump_state, expand=1, color=pump_state_color,
                            weight=ft.FontWeight.BOLD if is_current_time else ft.FontWeight.NORMAL,
                            size=16 if is_current_time else 14),
                    ft.Text(pump_activated_this_hour_state, expand=1, color=pump_activated_this_hour_color,
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
    await data_display.loop_data()

ft.app(target=main)