# Deník spojení

Desktopová aplikace pro evidenci rádiových spojení, poslechů, testů a DX provozu.

## Hlavní funkce

* Evidence analogových i digitálních spojení
* Výpočet vzdálenosti a azimutu z lokátorů
* Filtrování a vyhledávání záznamů
* Export a import dat do CSV
* Tisk filtrovaných záznamů
* Přehledné uživatelské rozhraní ve stylu Propagation Monitor
* Databáze SQLite
* Správa vlastních seznamů:

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

## Podporované režimy

### Analogové

* FM
* NFM
* AM

### Digitální

* DMR
* C4FM
* D-STAR
* M17
* DIGI
* DATA

## Digitální záznamy

Program umožňuje evidovat například:

* DMR simplex
* DMR repeater
* DMR hotspot
* C4FM / Fusion
* D-STAR
* M17
* Další digitální provoz dle vlastního nastavení

## Databáze

Program používá databázi SQLite.

Veškerá nastavení, seznamy a záznamy jsou ukládány lokálně do jednoho databázového souboru.

## Systémové požadavky

### Windows

* Windows 10 nebo Windows 11
* Není nutná instalace Pythonu
* Stačí stáhnout a spustit soubor EXE

### Linux

* Python 3.10+
* Tkinter
* tkintermapview (pro mapu spojení)

## Licence

MIT License

## Autor

Petr Molek
