# Deník spojení

Desktopová aplikace pro evidenci rádiových spojení, poslechů, testů, DX provozu a experimentálního rádiového provozu.

Program je určen pro uživatele PMR, radioamatéry, SWL posluchače i další zájemce o evidenci rádiových spojení.

---

## Hlavní funkce

* Evidence analogových i digitálních spojení
* Výpočet vzdálenosti a azimutu z lokátorů
* Filtrování a vyhledávání záznamů
* Export a import dat do CSV
* Tisk filtrovaných záznamů
* Přehledné uživatelské rozhraní ve stylu Propagation Monitor
* Databáze SQLite
* Statistiky spojení
* Evidence DX spojení
* Evidence testů a experimentů
* Mapa spojení s grafickým zobrazením protistanic
* Správa vlastních seznamů a číselníků

---

## Správa seznamů

Program umožňuje vytvářet a upravovat vlastní seznamy používané při evidenci spojení.

### Analogový provoz

* Kanály
* CTCSS/DCS kódy
* Typy spojení
* Modulace
* Výkony
* Kvalita spojení
* Zařízení
* Antény

### Digitální provoz

* Digitální kanály
* Typy digitálních spojení
* Digitální modulace
* Výkony
* Kvalita spojení
* Zařízení
* Antény

---

## Podporované režimy

### Analogové

* FM
* NFM
* AM

### Digitální

* DMR
* C4FM (Yaesu System Fusion)
* D-STAR
* M17
* DIGI
* DATA

---

## Digitální záznamy

Program umožňuje evidovat například:

* DMR simplex
* DMR repeater
* DMR hotspot
* C4FM / Fusion
* D-STAR
* M17
* APRS DATA
* Další digitální provoz dle vlastního nastavení

---

## Databáze

Program používá databázi SQLite.

Veškerá nastavení, seznamy a záznamy jsou ukládány lokálně do jednoho databázového souboru.

Výhody:

* Není potřeba databázový server
* Snadné zálohování
* Přenositelnost mezi počítači
* Jednoduchá archivace dat

---

## Systémové požadavky

### Windows

* Windows 10 nebo Windows 11
* Není nutná instalace Pythonu
* Stačí stáhnout a spustit soubor EXE

### Linux

* Python 3.10 nebo novější
* Tkinter
* tkintermapview (pro mapu spojení)

Instalace:

```bash
sudo apt install python3-tk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 denik_spojeni.py
```

### macOS

* Python 3.10 nebo novější
* Tkinter
* tkintermapview

Instalace:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 denik_spojeni.py
```

---

## Budoucí plánovaný vývoj

* Rozšířené statistiky
* Další exportní formáty
* Vylepšená práce s mapou
* Podpora dalších digitálních režimů
* Modulární architektura programu

---

## Licence

MIT License

---

## Autor

Fionghal
