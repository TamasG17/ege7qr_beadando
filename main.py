import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk

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

        # Stílusok beállítása a színezéshez
        style = ttk.Style()
        style.configure("black.Treenode", foreground="black")
        style.configure("yellow.Treenode", foreground="yellow")
        style.configure("brown.Treenode", foreground="brown")
        style.configure("red.Treenode", foreground="red")
        style.configure("blue.Treenode", foreground="blue")

        # Autó táblázat
        columns = ("tipus", "ar", "evjarat", "tulajdonosok", "muszaki", "baleset", "forgalomban")
        self.car_treeview = ttk.Treeview(self.root, columns=columns, show="headings")

        self.car_treeview.heading("tipus", text="Típus")
        self.car_treeview.heading("ar", text="Ár")
        self.car_treeview.heading("evjarat", text="Évjárat")
        self.car_treeview.heading("tulajdonosok", text="Tulajdonosok")
        self.car_treeview.heading("muszaki", text="Műszaki")
        self.car_treeview.heading("baleset", text="Baleset")
        self.car_treeview.heading("forgalomban", text="Állapot")

        # Oszlopok szélességének beállítása
        self.car_treeview.column("tipus", width=100)
        self.car_treeview.column("ar", width=80)
        self.car_treeview.column("evjarat", width=70)
        self.car_treeview.column("tulajdonosok", width=90)
        self.car_treeview.column("muszaki", width=90)
        self.car_treeview.column("baleset", width=70)
        self.car_treeview.column("forgalomban", width=120)

        self.car_treeview.pack(padx=10, pady=10, fill="both", expand=True)

        # Gombok
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Törlés", command=self._delete_selected_car).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Új autó hozzáadása", command=self._open_add_window).pack(side=tk.LEFT,
                                                                                                    padx=5)

    def _populate_car_list(self):
        """
        Feltölti a Treeview-t az autóadatokkal, a színes jelöléseket is figyelembe véve.
        """
        self.car_treeview.delete(*self.car_treeview.get_children())

        for car in self.cars:
            tags = ()

            muszaki_ervenyesseg = (datetime.strptime(car['muszaki'], '%Y-%m-%d').date() - datetime.today().date()).days
            baleset = car['baleset']
            forgalomban = car['forgalomban']

            if not forgalomban:
                tags = ("blue.Treenode",)
            elif muszaki_ervenyesseg <= 30 and baleset and forgalomban:
                tags = ("red.Treenode",)
            elif muszaki_ervenyesseg <= 30 and not baleset and forgalomban:
                tags = ("brown.Treenode",)
            elif muszaki_ervenyesseg > 30 and baleset and forgalomban:
                tags = ("yellow.Treenode",)
            elif muszaki_ervenyesseg > 30 and not baleset and forgalomban:
                tags = ("black.Treenode",)

            self.car_treeview.insert("", "end", values=(
                car['tipus'],
                f"{car['ar']} Ft",
                car['evjarat'],
                car['tulajdonosok'],
                car['muszaki'],
                'Igen' if car['baleset'] else 'Nem',
                'Forgalomban van' if car['forgalomban'] else 'Nincs forgalomban'
            ), tags=tags)

    def _delete_selected_car(self):
        """
        Eseménykezelő: a kiválasztott autó törlése.
        """
        selected_item = self.car_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Figyelmeztetés", "Kérlek, válassz ki egy autót a törléshez!")
            return

        index = self.car_treeview.index(selected_item)
        tg_autok.tg_delete_car(self.cars, index)
        self._populate_car_list()

    def _open_add_window(self):
        """
        Ablak megnyitása új autó hozzáadásához.
        """
        add_window = tk.Toplevel(self.root)
        add_window.title("Új autó hozzáadása")

        fields = [
            ("Típus:", 'tipus'), ("Ár:", 'ar'), ("Évjárat:", 'evjarat'), ("Tulajdonosok száma:", 'tulajdonosok'),
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
                new_car_data['ar'] = int(new_car_data['ar'])
                new_car_data['evjarat'] = int(new_car_data['evjarat'])
                new_car_data['tulajdonosok'] = int(new_car_data['tulajdonosok'])

                # A hiba itt volt: hiányzó zárójelek
                new_car_data['baleset'] = new_car_data['baleset'].lower() == 'igen'
                new_car_data['forgalomban'] = new_car_data['forgalomban'].lower() == 'igen'

                datetime.strptime(new_car_data['muszaki'], '%Y-%m-%d')
            except (ValueError, IndexError):
                messagebox.showerror("Hiba", "Helytelen adatformátum! Kérlek, ellenőrizd a bevitelt.")
                return

            tg_autok.tg_add_car(self.cars, new_car_data)
            self._populate_car_list()
            add_window.destroy()
# Saját függvény
def TG_start_app():
    root = tk.Tk()
    app = TGAutosApp(root)
    root.mainloop()

if __name__ == "__main__":
    TG_start_app()