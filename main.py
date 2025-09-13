import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta

import tg_autok


class TGAutosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TG Autónyilvántartás")

        self.cars = tg_autok.tg_adatok_betoltese()
        self.sort_directions = {}

        self._create_widgets()
        self._populate_car_list()

    def _create_widgets(self):
        style = ttk.Style()

        self.car_treeview = ttk.Treeview(self.root, show="headings")
        self.car_treeview.tag_configure("black_tag", foreground="white", background="black")
        self.car_treeview.tag_configure("goldenrod_tag", foreground="black", background="goldenrod")
        self.car_treeview.tag_configure("saddlebrown_tag", foreground="white", background="saddlebrown")
        self.car_treeview.tag_configure("red_tag", foreground="white", background="red")
        self.car_treeview.tag_configure("blue_tag", foreground="white", background="blue")

        columns = ("tipus", "ar", "evjarat", "tulajdonosok", "muszaki", "baleset", "forgalomban")
        self.car_treeview.configure(columns=columns)

        self.car_treeview.heading("tipus", text="Típus", command=lambda _col="tipus": self._sort_column("tipus"))
        self.car_treeview.heading("ar", text="Ár", command=lambda _col="ar": self._sort_column("ar"))
        self.car_treeview.heading("evjarat", text="Évjárat",
                                  command=lambda _col="evjarat": self._sort_column("evjarat"))
        self.car_treeview.heading("tulajdonosok", text="Tulajdonosok",
                                  command=lambda _col="tulajdonosok": self._sort_column("tulajdonosok"))
        self.car_treeview.heading("muszaki", text="Műszaki",
                                  command=lambda _col="muszaki": self._sort_column("muszaki"))
        self.car_treeview.heading("baleset", text="Baleset",
                                  command=lambda _col="baleset": self._sort_column("baleset"))
        self.car_treeview.heading("forgalomban", text="Forgalomban",
                                  command=lambda _col="forgalomban": self._sort_column("forgalomban"))

        for col in columns:
            self.sort_directions[col] = False

        self.car_treeview.column("tipus", width=100)
        self.car_treeview.column("ar", width=80)
        self.car_treeview.column("evjarat", width=70)
        self.car_treeview.column("tulajdonosok", width=90)
        self.car_treeview.column("muszaki", width=90)
        self.car_treeview.column("baleset", width=70)
        self.car_treeview.column("forgalomban", width=120)

        self.car_treeview.pack(padx=10, pady=10, fill="both", expand=True)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Törlés", command=self._delete_car_from_list).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Új autó hozzáadása", command=self._open_add_window).pack(side=tk.LEFT,
                                                                                                    padx=5)

        self._create_legend()

    def _create_legend(self):
        legend_frame = tk.LabelFrame(self.root, text="Színjelmagyarázat")
        legend_frame.pack(padx=10, pady=5, fill="x")

        legend_data = [
            ("Műsz. érv., baleset: nem, forg. van:", "black", "white"),
            ("Műsz. érv., baleset: igen, forg. van:", "goldenrod", "black"),
            ("Műsz. nem érv., baleset: nem, forg. van:", "saddlebrown", "white"),
            ("Műsz. nem érv., baleset: igen, forg, van:", "red", "white"),
            ("Nincs forg.", "blue", "white")
        ]

        for i, (text, bg, fg) in enumerate(legend_data):
            label = tk.Label(legend_frame, text=text, bg=bg, fg=fg)
            label.pack(side=tk.LEFT, padx=5, pady=2)

    def _sort_column(self, col):
        data = [(self.car_treeview.set(item, col), item) for item in self.car_treeview.get_children("")]

        reverse_sort = self.sort_directions[col]

        if col == "ar":
            data.sort(key=lambda x: int(x[0].replace(' Ft', '')), reverse=reverse_sort)
        elif col in ["evjarat", "tulajdonosok"]:
            data.sort(key=lambda x: int(x[0]), reverse=reverse_sort)
        elif col == "muszaki":
            data.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=reverse_sort)
        elif col == "baleset":
            order = ["Nem", "Igen"]
            data.sort(key=lambda x: order.index(x[0]), reverse=reverse_sort)
        elif col == "forgalomban":
            order = ["Nincs forgalomban", "Forgalomban van"]
            data.sort(key=lambda x: order.index(x[0]), reverse=reverse_sort)
        else:
            data.sort(reverse=reverse_sort)

        for index, (val, item) in enumerate(data):
            self.car_treeview.move(item, "", index)

        self.sort_directions[col] = not reverse_sort

    def _populate_car_list(self):
        self.car_treeview.delete(*self.car_treeview.get_children())

        for car in self.cars:
            tags = ()

            muszaki_ervenyesseg_napokban = (
                        datetime.strptime(car['muszaki'], '%Y-%m-%d').date() - datetime.today().date()).days
            baleset_logikai = car['baleset']
            forgalomban_logikai = car['forgalomban']

            if not forgalomban_logikai:
                tags = ("blue_tag",)
            elif muszaki_ervenyesseg_napokban <= 30 and baleset_logikai:
                tags = ("red_tag",)
            elif muszaki_ervenyesseg_napokban <= 30 and not baleset_logikai:
                tags = ("saddlebrown_tag",)
            elif muszaki_ervenyesseg_napokban > 30 and baleset_logikai:
                tags = ("goldenrod_tag",)
            elif muszaki_ervenyesseg_napokban > 30 and not baleset_logikai:
                tags = ("black_tag",)

            self.car_treeview.insert("", "end", values=(
                car['tipus'],
                f"{car['ar']} Ft",
                car['evjarat'],
                car['tulajdonosok'],
                car['muszaki'],
                'Igen' if car['baleset'] else 'Nem',
                'Forgalomban van' if forgalomban_logikai else 'Nincs forgalomban'
            ), tags=tags)

    def _delete_car_from_list(self):
        selected_item = self.car_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Figyelmeztetés", "Kérlek, válassz ki egy autót a törléshez!")
            return

        index = self.car_treeview.index(selected_item)
        tg_autok.tg_delete_car(self.cars, index)
        self._populate_car_list()

    def _open_add_window(self):
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

            try:
                new_car_data['ar'] = int(new_car_data['ar'])
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


def TG_start_app():
    root = tk.Tk()
    app = TGAutosApp(root)
    root.mainloop()


if __name__ == "__main__":
    TG_start_app()