# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
#   print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#   print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import datetime

# Saját modul importálása
import tg_web_utils

# Fő API végpont
OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"


# Saját függvény, monogrammal
def save_tg_plot(fig: plt.Figure, out_path: str):
    """
    A matplotlib grafikont PNG fájlba menti az adott útvonalra.

    Args:
        fig (plt.Figure): A menteni kívánt grafikon objektum.
        out_path (str): A kimeneti fájl teljes elérési útja.
    """
    try:
        fig.savefig(out_path)
        print(f"Grafikon sikeresen mentve: {out_path}")
    except Exception as e:
        print(f"Hiba a grafikon mentése során: {e}")


# Saját osztály, monogrammal
class TGWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TGWeatherMap - Időjárás minialkalmazás")
        self.root.geometry("600x600")

        self._setup_ui()

    def _setup_ui(self):
        # UI elemek létrehozása
        self.title_label = tk.Label(self.root, text="Város Időjárása", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.city_frame = tk.Frame(self.root)
        self.city_frame.pack(pady=5)

        tk.Label(self.city_frame, text="Város:").pack(side=tk.LEFT, padx=5)

        self.city_entry = tk.Entry(self.city_frame, width=30)
        self.city_entry.pack(side=tk.LEFT)
        self.city_entry.bind("<Return>", self._on_enter_pressed)  # Eseménykezelés

        self.search_button = tk.Button(self.city_frame, text="Keresés", command=self._on_button_click)
        self.search_button.pack(side=tk.LEFT, padx=5)  # Eseménykezelés

        self.weather_info_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.weather_info_label.pack(pady=10)

        # Matplotlib grafikon beágyazása
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)

        self.save_button = tk.Button(self.root, text="Grafikon mentése PNG-be", command=self._save_plot)
        self.save_button.pack(pady=5)

        # Kezdő érték beállítása
        self.city_entry.insert(0, "Budapest")
        self.search_button.invoke()  # Automatikus keresés a program indulásakor

    def _on_enter_pressed(self, event):
        """Eseménykezelő: Enter gomb lenyomására indítja a keresést."""
        self._get_weather()

    def _on_button_click(self):
        """Eseménykezelő: Keresés gombra kattintva indítja a keresést."""
        self._get_weather()

    def _get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Hiányzó adat", "Kérlek, adj meg egy városnevet!")
            return

        # A geokódolás API használata a koordináták lekérdezéséhez
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1}
        geo_data = tg_web_utils.fetch_tg_json(geo_url, geo_params)

        if not geo_data or 'results' not in geo_data or not geo_data['results']:
            messagebox.showerror("Hiba", f"Nem található város a '{city}' néven.")
            return

        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']

        # Fő időjárás-lekérés az Open-Meteo API-ról
        weather_params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m',
            'current_weather': True,
            'forecast_days': 1
        }

        weather_data = tg_web_utils.fetch_tg_json(OPEN_METEO_API, weather_params)

        if weather_data:
            # Adatok feldolgozása a saját modul segítségével
            times, temps = tg_web_utils.parse_tg_weather(weather_data)

            # A GUI frissítése
            self._update_plot(times, temps, city)
            self._update_weather_info(weather_data, city)

    def _update_plot(self, times, temps, city):
        self.ax.clear()
        if times and temps:
            self.ax.plot(times, temps, marker='o', linestyle='-', color='b')
            self.ax.set_title(f"Hőmérséklet előrejelzés: {city}")
            self.ax.set_xlabel("Idő (óra)")
            self.ax.set_ylabel("Hőmérséklet (°C)")
            self.ax.grid(True)
            self.ax.tick_params(axis='x', rotation=45)
            self.ax.set_xticks(self.ax.get_xticks()[::3])  # 3 óránkénti jelölés
        else:
            self.ax.set_title("Nincs adat a grafikonhoz")

        self.fig.tight_layout()
        self.canvas.draw()

    def _update_weather_info(self, weather_data, city):
        try:
            current = weather_data['current_weather']
            temp = current['temperature']
            wind_speed = current['wind_speed']
            wind_direction_deg = current['wind_direction']
            wind_direction_text = tg_web_utils.deg_to_tg_cardinal(wind_direction_deg)

            info_text = (
                f"Város: {city}\n"
                f"Aktuális hőmérséklet: {temp}°C\n"
                f"Szélsebesség: {wind_speed} km/h\n"
                f"Szélirány: {wind_direction_text}"
            )
            self.weather_info_label.config(text=info_text)
        except (KeyError, IndexError) as e:
            print(f"Hiba az aktuális adatok megjelenítése során: {e}")
            self.weather_info_label.config(text=f"A '{city}' város aktuális adatai nem elérhetők.")

    def _save_plot(self):
        file_name = f"idojaras_grafikon_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        save_tg_plot(self.fig, file_name)
        messagebox.showinfo("Mentés", f"A grafikon sikeresen mentve: {file_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TGWeatherApp(root)
    root.mainloop()
