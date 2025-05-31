from abc import ABC, abstractmethod
from datetime import date, datetime
import uuid

# --- Absztrakt Autó osztály ---
class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.berles_alatt = False

    @abstractmethod
    def auto_info(self):
        pass


# --- Személyautó osztály ---
class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama

    def auto_info(self):
        return f"Személyautó: {self.rendszam}, {self.tipus}, {self.berleti_dij} Ft/nap, {self.ajtok_szama} ajtó"


# --- Teherautó osztály ---
class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras_kg):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras_kg = teherbiras_kg

    def auto_info(self):
        return f"Teherautó: {self.rendszam}, {self.tipus}, {self.berleti_dij} Ft/nap, {self.teherbiras_kg} kg teherbírás"


# --- Bérlés osztály ---
class Berles:
    def __init__(self, auto, datum):
        self.id = str(uuid.uuid4())[:8]
        self.auto = auto
        self.datum = datum

    def __str__(self):
        return f"Bérlés ID: {self.id}, Autó: {self.auto.rendszam}, Dátum: {self.datum}, Ár: {self.auto.berleti_dij} Ft"


# --- Autókölcsönző osztály ---
class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadas(self, auto):
        self.autok.append(auto)

    def berel_auto(self, rendszam, datum_str):
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
            if datum < date.today():
                print("Nem lehet múltbeli dátumra bérlést rögzíteni.")
                return None
        except ValueError:
            print("Érvénytelen dátumformátum! Használj ÉÉÉÉ-HH-NN formátumot.")
            return None

        for auto in self.autok:
            if auto.rendszam == rendszam:
                if auto.berles_alatt:
                    print("Ez az autó jelenleg nem elérhető.")
                    return None
                else:
                    auto.berles_alatt = True
                    uj_berles = Berles(auto, datum)
                    self.berlesek.append(uj_berles)
                    print(f"Sikeres bérlés! Ár: {auto.berleti_dij} Ft")
                    return uj_berles
        print("Nincs ilyen rendszámú autó.")
        return None

    def lemond_berles(self, berles_id):
        for berles in self.berlesek:
            if berles.id == berles_id:
                berles.auto.berles_alatt = False
                self.berlesek.remove(berles)
                print("A bérlés sikeresen le lett mondva.")
                return True
        print("Nem található ilyen azonosítójú bérlés.")
        return False

    def listaz_berlesek(self):
        if not self.berlesek:
            print("Nincs aktív bérlés.")
        for berles in self.berlesek:
            print(berles)

    def listaz_autok(self):
        for auto in self.autok:
            status = "FOGLALT" if auto.berles_alatt else "SZABAD"
            print(f"{auto.auto_info()} - {status}")


# --- Alapértelmezett adatok betöltése ---
def indulasi_adatok():
    kolcsonzo = Autokolcsonzo("CityRent")

    # Autók
    auto1 = Szemelyauto("ABC-123", "Opel Astra", 10000, 5)
    auto2 = Teherauto("XYZ-789", "Ford Transit", 15000, 1200)
    auto3 = Szemelyauto("DEF-456", "Suzuki Swift", 8000, 3)

    kolcsonzo.auto_hozzaadas(auto1)
    kolcsonzo.auto_hozzaadas(auto2)
    kolcsonzo.auto_hozzaadas(auto3)

    # Bérlések (mai napra)
    kolcsonzo.berel_auto("ABC-123", str(date.today()))
    kolcsonzo.berel_auto("XYZ-789", str(date.today()))
    kolcsonzo.berel_auto("DEF-456", str(date.today()))

    return kolcsonzo


# --- Felhasználói felület ---
def menu(kolcsonzo):
    while True:
        print("\n--- Autókölcsönző Menü ---")
        print("1. Autók listázása")
        print("2. Autó bérlése")
        print("3. Bérlés lemondása")
        print("4. Bérlések listázása")
        print("0. Kilépés")

        valasztas = input("Válassz egy opciót: ")

        if valasztas == "1":
            kolcsonzo.listaz_autok()
        elif valasztas == "2":
            rendszam = input("Add meg a bérelni kívánt autó rendszámát: ")
            datum = input("Add meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ")
            kolcsonzo.berel_auto(rendszam, datum)
        elif valasztas == "3":
            berles_id = input("Add meg a lemondani kívánt bérlés azonosítóját: ")
            kolcsonzo.lemond_berles(berles_id)
        elif valasztas == "4":
            kolcsonzo.listaz_berlesek()
        elif valasztas == "0":
            print("Kilépés a programból.")
            break
        else:
            print("Érvénytelen választás, próbáld újra.")


# --- Program indítása ---
if __name__ == "__main__":
    kolcsonzo = indulasi_adatok()
    menu(kolcsonzo)