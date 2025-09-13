import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Saját modul importálása
import tg_autok


# Saját osztály
class TGAutosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TG Autókereskedés")

        # Betöltjük az adatokat
        self.cars = tg_autok.tg_load_cars()

        self._create_widgets()
        self._populate_car_list()

    def _create_widgets(self):
        # UI elemek létrehozása

        # Autó lista
        self.car_list_frame = tk.Frame(self.root)
        self.car_list_frame.pack(pady=10)

        tk.Label(self.car_list_frame, text="Autók listája:", font=("Arial", 14, "bold")).pack()

        self.car_listbox = tk.Listbox(self.car_list_frame, width=80, height=15)
        self.car_listbox.pack(side=tk.LEFT, fill=tk.Y)

        scrollbar = tk.Scrollbar(self.car_list_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.car_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.car_listbox.config(yscrollcommand=scrollbar.set)

        # Gombok
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Törlés", command=self._delete_selected_car).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Új autó hozzáadása", command=self._open_add_window).pack(side=tk.LEFT,
                                                                                                    padx=5)

    def _populate_car_list(self):
        """
        Feltölti a listbox-ot az autóadatokkal, a színes jelöléseket is figyelembe véve.
        """
        self.car_listbox.delete(0, tk.END)
        for i, car in enumerate(self.cars):
            status = "Forgalomban van" if car['forgalomban'] else "Nincs forgalomban"
            display_text = (
                f"{car['tipus']} ({car['evjarat']}) - Tulajdonos: {car['tulajdonosok']}, "
                f"Műszaki: {car['muszaki']}, Baleset: {'Igen' if car['baleset'] else 'Nem'}, "
                f"Állapot: {status}"
            )
            self.car_listbox.insert(tk.END, display_text)

            # Színes jelölések
            if not car['forgalomban']:
                self.car_listbox.itemconfig(tk.END, {'fg': 'green'})  # Zöld, ha nincs forgalomban
            else:
                muszaki_datum = datetime.strptime(car['muszaki'], '%Y-%m-%d').date()
                if (muszaki_datum - datetime.today().date()).days <= 30:
                    self.car_listbox.itemconfig(tk.END, {'fg': 'red'})  # Piros, ha lejár 30 napon belül

    def _delete_selected_car(self):
        """
        Eseménykezelő: a kiválasztott autó törlése.
        """
        try:
            index = self.car_listbox.curselection()[0]
            tg_autok.tg_delete_car(self.cars, index)
            self._populate_car_list()
        except IndexError:
            messagebox.showwarning("Figyelmeztetés", "Kérlek, válassz ki egy autót a törléshez!")

    def _open_add_window(self):
        """
        Ablak megnyitása új autó hozzáadásához.
        """
        add_window = tk.Toplevel(self.root)
        add_window.title("Új autó hozzáadása")

        fields = [
            ("Típus:", 'tipus'), ("Évjárat:", 'evjarat'), ("Tulajdonosok száma:", 'tulajdonosok'),
            ("Műszaki érvényesség (ÉÉÉÉ-HH-NN):", 'muszaki'), ("Baleset volt (Igen/Nem):", 'baleset'),
            ("Forgalomban van (Igen/Nem):", 'forgalomban')
        ]

        entries = {}
        for i, (label_text, field_key) in enumerate(fields):
            tk.Label(add_window, text=label_text).grid(row=i, column=0, padx=5, pady=5)
            entries[field_key] = tk.Entry(add_window)
            entries[field_key].grid(row=i, column=1, padx=5, pady=5)

        def _add_car_to_list():
            new_car_data = {}
            for field, entry in entries.items():
                new_car_data[field] = entry.get()

            # Adatellenőrzés
            try:
                new_car_data['evjarat'] = int(new_car_data['evjarat'])
                new_car_data['tulajdonosok'] = int(new_car_data['tulajdonosok'])
                new_car_data['baleset'] = new_car_data['baleset'].lower() == 'igen'
                new_car_data['forgalomban'] = new_car_data['forgalomban'].lower() == 'igen'
                datetime.strptime(new_car_data['muszaki'], '%Y-%m-%d')
            except (ValueError, IndexError):
                messagebox.showerror("Hiba", "Helytelen adatformátum! Kérlek, ellenőrizd a bevitelt.")
                return

            tg_autok.tg_add_car(self.cars, new_car_data)
            self._populate_car_list()
            add_window.destroy()

        tk.Button(add_window, text="Hozzáadás", command=_add_car_to_list).grid(row=len(fields), columnspan=2, pady=10)


# Saját függvény
def TG_start_app():
    root = tk.Tk()
    app = TGAutosApp(root)
    root.mainloop()


if __name__ == "__main__":
    TG_start_app()