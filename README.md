Python beadandó

Tamás Gábor -EGE7QR : Autónyilvántartás

"main.py", "tg_autok.py" 

1. Feladat leírása:
A program egy interaktív autónyilvántartó alkalmazás, amely grafikus felhasználói felületen (Tkinter) keresztül kezeli a járműadatokat.
A main.py elindításakor egy ablak jelenik meg, amely révén autókat az adott adataikkal vehetünk fel rekordonként - ezt egy json fájlban tárolja, ami akkor jön létre, amikor felvesszük az első rekordot (autok.json).
Különbőzö feltételek szerint szinezi ezeket, amelyeket lehet törölni is és a mező nevekre kattintva rendezi a rekordokat.).
A program színkódolással jelzi az autók műszaki állapotát, baleseti előéletét és forgalomban való részvételét.


A fő funkciók:

  - Autóadatok betöltése és mentése JSON fájlba

  - Autók listázása és rendezése

  - Színkódolt állapotjelzés (műszaki érvényesség, baleset, forgalomban van-e)

  - Új autó felvétele
    
  - Kijelölt autó törlése

  - Hibakezelés (érvénytelen bevitel esetén)

A program indító modulja: main.py.

2. Modulok és a bennük használt függvények
2.1. main.py

(Fő GUI modul – Tkinteres alkalmazás logikája)

main

Fontosabb metódusok:

_create_widgets()
A grafikus felület elemeit hozza létre (TreeView, gombok, legendák).

_create_legend()
Megjeleníti a színjelmagyarázatot az autók állapotához.

_sort_column(col)
Az oszlopok szerinti rendezést végzi (ár, évjárat, tulajdonosok, műszaki dátum stb.).

_populate_car_list()
Betölti az autóadatokat a táblázatba, és beállítja a megfelelő színtageket az állapotok alapján.

_delete_car_from_list()
A kijelölt autót törli a listából és a háttérfájlból.

_open_add_window()
Új ablakot nyit autó hozzáadásához, validálja a bevitt adatokat és elmenti az új elemet.

TG_start_app()
Elindítja a teljes alkalmazást.

2.2. tg_autok.py
(Adatkezelés és fájlműveletek)
tg_autok

Függvények:

  - tg_adatok_betoltese()
Betölti az autókat a autok.json fájlból.
Ha a fájl nem létezik vagy hibás, üres listát ad vissza.

  - tg_adatok_mentese(autok)
Mentést végez JSON formátumban az autok.json fájlba.

  - tg_add_car(autok, new_car_data)
Hozzáad egy új autót a listához, majd menti a változásokat.

  - tg_delete_car(autok, index)
Törli az adott indexű autót és elmenti az új listát.

3. Osztály(ok)
  - TGAutosApp osztály
(Definiálva a main.py fájlban)


main

Ez az alkalmazás fő osztálya, amely:

  - létrehozza és megjeleníti a teljes Tkinter GUI-t,

  - kezeli a felhasználói interakciókat,

  - kapcsolatot tart a háttérben működő adatkezelő modullal,

  - biztosítja az autók listájának betöltését, megjelenítését, rendezését, törlését és bővítését.

Főbb attribútumai:

  - self.cars – az autók adatait tartalmazó lista

  - self.car_treeview – táblázatos megjelenítés (TreeView)

  - self.sort_directions – nyilvántartja az oszloponkénti rendezési irányt


Fő feladatai:

  - GUI elemek létrehozása

  - Adatok megjelenítése

  - Rendezés kezelése

  - Színkódolás logikája

  - Adatbevitel validálása

  - Adatok mentése és törlése
