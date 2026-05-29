#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Deník spojení


import csv, math, sqlite3, calendar, os, tempfile, webbrowser, html
from datetime import datetime, date
from pathlib import Path

try:
    import tkintermapview
except Exception:
    tkintermapview = None
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# Základní informace o aplikaci a název databázového souboru

APP_TITLE = "Deník spojení"
APP_VERSION = "0.9.1"
DB_FILE = "denik.sqlite3"
# Výchozí PMR kanály, hodnoty signálu a kvality spojení

PMR_CHANNELS = {1:446.00625,2:446.01875,3:446.03125,4:446.04375,5:446.05625,6:446.06875,7:446.08125,8:446.09375,9:446.10625,10:446.11875,11:446.13125,12:446.14375,13:446.15625,14:446.16875,15:446.18125,16:446.19375}
SIGNAL_VALUES = ["1 - velmi slabý", "2 - slabý", "3 - použitelný", "4 - dobrý", "5 - vyborný"]
QUALITY_VALUES = ["čistá", "dobrá", "šum", "slabá modulace", "přebuzená modulace", "rušení", "nečitelná"]
# Výchozí hodnoty, které se při prvním spuštění doplní do databáze


DEFAULT_QUALITY_VALUES = [(name,) for name in QUALITY_VALUES]


DEFAULT_POWER_VALUES = [(name,) for name in ["0.5 W", "1 W", "2 W", "4 W", "5 W", "8 W", "10 W"]]


DEFAULT_ANALOG_OPERATION_TYPES = [(name,) for name in ["poslech", "spojení", "DX", "vysílání", "test", "skenování"]]
DEFAULT_DIGITAL_OPERATION_TYPES = [(name,) for name in ["DMR Simplex", "DMR Repeater", "DMR Hotspot", "C4FM / Fusion", "D-STAR", "M17", "digitální test"]]
DEFAULT_ANALOG_MODULATION_MODES = [(name,) for name in ["FM", "NFM", "AM"]]
DEFAULT_DIGITAL_MODULATION_MODES = [(name,) for name in ["DMR", "C4FM", "D-STAR", "M17", "DIGI", "DATA"]]


DEFAULT_DIGITAL_CHANNELS = [
# Seznam výchozích digitálních kanálů je zatím prázdný a lze jej doplnit později

]


DEFAULT_CTCSS_DCS_CODES = [
# Výchozí seznam CTCSS a DCS kódů pro analogový provoz
    ("Bez kódu", ""),
    ("CTCSS 67.0", "67.0"), ("CTCSS 69.3", "69.3"), ("CTCSS 71.9", "71.9"),
    ("CTCSS 74.4", "74.4"), ("CTCSS 77.0", "77.0"), ("CTCSS 79.7", "79.7"),
    ("CTCSS 82.5", "82.5"), ("CTCSS 85.4", "85.4"), ("CTCSS 88.5", "88.5"),
    ("CTCSS 91.5", "91.5"), ("CTCSS 94.8", "94.8"), ("CTCSS 97.4", "97.4"),
    ("CTCSS 100.0", "100.0"), ("CTCSS 103.5", "103.5"), ("CTCSS 107.2", "107.2"),
    ("CTCSS 110.9", "110.9"), ("CTCSS 114.8", "114.8"), ("CTCSS 118.8", "118.8"),
    ("CTCSS 123.0", "123.0"), ("CTCSS 127.3", "127.3"), ("CTCSS 131.8", "131.8"),
    ("CTCSS 136.5", "136.5"), ("CTCSS 141.3", "141.3"), ("CTCSS 146.2", "146.2"),
    ("CTCSS 151.4", "151.4"), ("CTCSS 156.7", "156.7"), ("CTCSS 159.8", "159.8"),
    ("CTCSS 162.2", "162.2"), ("CTCSS 165.5", "165.5"), ("CTCSS 167.9", "167.9"),
    ("CTCSS 171.3", "171.3"), ("CTCSS 173.8", "173.8"), ("CTCSS 177.3", "177.3"),
    ("CTCSS 179.9", "179.9"), ("CTCSS 183.5", "183.5"), ("CTCSS 186.2", "186.2"),
    ("CTCSS 189.9", "189.9"), ("CTCSS 192.8", "192.8"), ("CTCSS 196.6", "196.6"),
    ("CTCSS 199.5", "199.5"), ("CTCSS 203.5", "203.5"), ("CTCSS 206.5", "206.5"),
    ("CTCSS 210.7", "210.7"), ("CTCSS 218.1", "218.1"), ("CTCSS 225.7", "225.7"),
    ("CTCSS 229.1", "229.1"), ("CTCSS 233.6", "233.6"), ("CTCSS 241.8", "241.8"),
    ("CTCSS 250.3", "250.3"), ("CTCSS 254.1", "254.1"),
    ("DCS 023N", "D023N"), ("DCS 025N", "D025N"), ("DCS 026N", "D026N"),
    ("DCS 031N", "D031N"), ("DCS 032N", "D032N"), ("DCS 043N", "D043N"),
    ("DCS 047N", "D047N"), ("DCS 051N", "D051N"), ("DCS 054N", "D054N"),
    ("DCS 065N", "D065N"), ("DCS 071N", "D071N"), ("DCS 072N", "D072N"),
    ("DCS 073N", "D073N"), ("DCS 074N", "D074N"), ("DCS 114N", "D114N"),
    ("DCS 115N", "D115N"), ("DCS 116N", "D116N"), ("DCS 125N", "D125N"),
    ("DCS 131N", "D131N"), ("DCS 132N", "D132N"), ("DCS 134N", "D134N"),
    ("DCS 143N", "D143N"), ("DCS 152N", "D152N"), ("DCS 155N", "D155N"),
    ("DCS 156N", "D156N"), ("DCS 162N", "D162N"), ("DCS 165N", "D165N"),
    ("DCS 172N", "D172N"), ("DCS 174N", "D174N"), ("DCS 205N", "D205N"),
    ("DCS 223N", "D223N"), ("DCS 226N", "D226N"), ("DCS 243N", "D243N"),
    ("DCS 244N", "D244N"), ("DCS 245N", "D245N"), ("DCS 251N", "D251N"),
    ("DCS 261N", "D261N"), ("DCS 263N", "D263N"), ("DCS 265N", "D265N"),
    ("DCS 271N", "D271N"), ("DCS 306N", "D306N"), ("DCS 311N", "D311N"),
    ("DCS 315N", "D315N"), ("DCS 331N", "D331N"), ("DCS 343N", "D343N"),
    ("DCS 346N", "D346N"), ("DCS 351N", "D351N"), ("DCS 364N", "D364N"),
    ("DCS 365N", "D365N"), ("DCS 371N", "D371N"), ("DCS 411N", "D411N"),
    ("DCS 412N", "D412N"), ("DCS 413N", "D413N"), ("DCS 423N", "D423N"),
    ("DCS 431N", "D431N"), ("DCS 432N", "D432N"), ("DCS 445N", "D445N"),
    ("DCS 464N", "D464N"), ("DCS 465N", "D465N"), ("DCS 466N", "D466N"),
    ("DCS 503N", "D503N"), ("DCS 506N", "D506N"), ("DCS 516N", "D516N"),
    ("DCS 532N", "D532N"), ("DCS 546N", "D546N"), ("DCS 565N", "D565N"),
    ("DCS 606N", "D606N"), ("DCS 612N", "D612N"), ("DCS 624N", "D624N"),
    ("DCS 627N", "D627N"), ("DCS 631N", "D631N"), ("DCS 632N", "D632N"),
    ("DCS 654N", "D654N"), ("DCS 662N", "D662N"), ("DCS 664N", "D664N"),
    ("DCS 703N", "D703N"), ("DCS 712N", "D712N"), ("DCS 723N", "D723N"),
    ("DCS 731N", "D731N"), ("DCS 732N", "D732N"), ("DCS 734N", "D734N"),
    ("DCS 743N", "D743N"), ("DCS 754N", "D754N"),
]


THEME = {
# Barevné schéma světlého vzhledu aplikace


    "bg": "#eef3f7",


    "fg": "#111111",


    "sub": "#444444",


    "panel": "#ffffff",


    "panel_fg": "#111111",


    "button": "#dde4ec",


    "button_hover": "#cfd8e3",


    "border": "#b8c6d4",


    "accent": "#146c2e",


    "accent2": "#0b8a3a",


    "table_header": "#e7eef6",


    "table_row": "#ffffff",


    "table_alt": "#f3f7fb",


    "select": "#d7e9ff",


    "select_fg": "#111111",


    "entry_bg": "#ffffff",


    "disabled_bg": "#e0e0e0",


    "disabled_fg": "#777777",
}


# Nastaví světlý vzhled aplikace a základní styly Tkinter/ttk.
def apply_light_style(root):


    root.configure(bg=THEME["bg"])


    style = ttk.Style(root)


    try:
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:


        pass


    default_font = ("Ubuntu", 10)
    title_font = ("Ubuntu", 18, "bold")
    bold_font = ("Ubuntu", 10, "bold")


    style.configure(".", font=default_font, background=THEME["bg"], foreground=THEME["fg"])


    style.configure("TFrame", background=THEME["bg"])


    style.configure("TLabel", background=THEME["bg"], foreground=THEME["fg"])


    style.configure("Title.TLabel", background=THEME["bg"], foreground=THEME["fg"], font=title_font)


    style.configure("Subtitle.TLabel", background=THEME["bg"], foreground=THEME["sub"], font=("Ubuntu", 10))


    style.configure("Card.TFrame", background=THEME["panel"], relief="solid", borderwidth=1)
    style.configure("Card.TLabel", background=THEME["panel"], foreground=THEME["fg"])
    style.configure("CardTitle.TLabel", background=THEME["panel"], foreground=THEME["fg"], font=("Ubuntu", 10, "bold"))
    style.configure("BigTitle.TLabel", background=THEME["bg"], foreground=THEME["fg"], font=("Ubuntu", 20, "bold"))
    style.configure("SmallInfo.TLabel", background=THEME["panel"], foreground=THEME["sub"], font=("Ubuntu", 9))


    style.configure(
        "TLabelframe",
        background=THEME["bg"],
        foreground=THEME["fg"],
        bordercolor=THEME["border"],
        relief="solid",
    )
    style.configure(
        "TLabelframe.Label",
        background=THEME["bg"],
        foreground=THEME["fg"],
        font=bold_font,
    )


    style.configure(
        "TButton",
        background=THEME["button"],
        foreground=THEME["fg"],
        bordercolor=THEME["border"],
        focusthickness=1,
        focuscolor=THEME["accent"],
        padding=(10, 6),
        font=bold_font,
    )
    style.map(
        "TButton",
        background=[("active", THEME["button_hover"]), ("pressed", THEME["border"]), ("disabled", THEME["disabled_bg"])],
        foreground=[("disabled", THEME["disabled_fg"])],
    )


    style.configure(
        "Accent.TButton",
        background=THEME["accent"],
        foreground="#ffffff",
        bordercolor=THEME["accent2"],
        padding=(12, 7),
        font=bold_font,
    )
    style.map("Accent.TButton", background=[("active", THEME["accent2"]), ("pressed", THEME["border"])])


    style.configure("TEntry", fieldbackground=THEME["entry_bg"], foreground=THEME["panel_fg"], insertcolor=THEME["panel_fg"], padding=4)
    style.configure("TCombobox", fieldbackground=THEME["entry_bg"], foreground=THEME["panel_fg"], padding=4)
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", THEME["entry_bg"]), ("disabled", THEME["disabled_bg"])],
        foreground=[("disabled", THEME["disabled_fg"])],
    )


    style.configure("TCheckbutton", background=THEME["bg"], foreground=THEME["fg"], font=default_font)
    style.map("TCheckbutton", background=[("active", THEME["bg"])], foreground=[("disabled", THEME["disabled_fg"])])


    style.configure(
        "Treeview",
        background=THEME["table_row"],
        fieldbackground=THEME["table_row"],
        foreground=THEME["panel_fg"],
        rowheight=30,
        bordercolor=THEME["border"],
        borderwidth=1,
        font=("Ubuntu", 10),
    )
    style.configure(
        "Treeview.Heading",
        background=THEME["table_header"],
        foreground=THEME["fg"],
        bordercolor=THEME["border"],
        font=bold_font,
        padding=6,
    )
    style.map("Treeview", background=[("selected", THEME["select"])], foreground=[("selected", THEME["select_fg"])])


    style.configure("Vertical.TScrollbar", background=THEME["button"], troughcolor=THEME["bg"], bordercolor=THEME["border"], arrowcolor=THEME["fg"])
    style.configure("Horizontal.TScrollbar", background=THEME["button"], troughcolor=THEME["bg"], bordercolor=THEME["border"], arrowcolor=THEME["fg"])


    try:
        root.option_add("*Menu.background", THEME["button"])
        root.option_add("*Menu.foreground", THEME["fg"])
        root.option_add("*Menu.activeBackground", THEME["button_hover"])
        root.option_add("*Menu.activeForeground", THEME["fg"])
        root.option_add("*Menu.font", default_font)
        root.option_add("*TCombobox*Listbox.background", THEME["entry_bg"])
        root.option_add("*TCombobox*Listbox.foreground", THEME["panel_fg"])
        root.option_add("*TCombobox*Listbox.selectBackground", THEME["select"])
        root.option_add("*TCombobox*Listbox.selectForeground", THEME["select_fg"])
    except Exception:

        pass


# Upraví lokátor do jednotného tvaru bez mezer a velkými písmeny.
def norm_loc(s):


    return (s or "").strip().upper().replace(" ", "")


# Upraví volačku do jednotného tvaru velkými písmeny.
def norm_call(s):


    return (s or "").strip().upper()


# Převede Maidenhead lokátor na zeměpisnou šířku a délku.
def locator_to_latlon(locator):
    loc = norm_loc(locator)
    if len(loc) not in (4, 6):
        raise ValueError("Lokátor musí mít 4 nebo 6 znaků, např. JN99 nebo JN99AO.")
    if not ("A" <= loc[0] <= "R" and "A" <= loc[1] <= "R"):
        raise ValueError("První dva znaky lokátoru musí být A až R.")
    if not (loc[2].isdigit() and loc[3].isdigit()):
        raise ValueError("Třetí a čtvrtý znak lokátoru musí být číslice.")
    lon = (ord(loc[0])-65)*20.0 - 180.0 + int(loc[2])*2.0
    lat = (ord(loc[1])-65)*10.0 - 90.0 + int(loc[3])*1.0
    if len(loc) == 4:
        lon += 1.0; lat += 0.5
    else:
        if not ("A" <= loc[4] <= "X" and "A" <= loc[5] <= "X"):
            raise ValueError("Pátý a šestý znak lokátoru musí být A až X.")
        lon_step = 5.0/60.0; lat_step = 2.5/60.0
        lon += (ord(loc[4])-65)*lon_step + lon_step/2.0
        lat += (ord(loc[5])-65)*lat_step + lat_step/2.0
    return lat, lon


# Spočítá vzdálenost a azimut mezi dvěma lokátory.
def distance_bearing(my_locator, other_locator):
    lat1, lon1 = locator_to_latlon(my_locator); lat2, lon2 = locator_to_latlon(other_locator)
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    dist = r * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    y = math.sin(dl)*math.cos(p2)
    x = math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    bearing = (math.degrees(math.atan2(y, x))+360) % 360
    return dist, bearing


# Převede azimut ve stupních na textový směr.
def bearing_dir(b):
    dirs = ["S","SSV","SV","VSV","V","VJV","JV","JJV","J","JJZ","JZ","ZJZ","Z","ZSZ","SZ","SSZ"]
    return dirs[int((b+11.25)/22.5) % 16]


# Otevře SQLite databázi a vytvoří potřebné tabulky, pokud ještě neexistují.
def db_connect():


    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row


    con.execute("""
        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dt TEXT NOT NULL,
            channel INTEGER NOT NULL,
            channel_name TEXT,
            frequency TEXT NOT NULL,
            tone TEXT,
            my_call TEXT,
            other_call TEXT,
            my_locator TEXT,
            locator TEXT,
            distance_km TEXT,
            bearing_deg TEXT,
            direction TEXT,
            operation_type TEXT,
            signal TEXT,
            quality TEXT,
            power TEXT,
            modulation TEXT,
            mode TEXT,
            tg TEXT,
            cc TEXT,
            call_group TEXT,
            digital_id TEXT,
            contact TEXT,
            device TEXT,
            antenna TEXT,
            note TEXT
        )
    """)


    con.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)


    con.execute("""
        CREATE TABLE IF NOT EXISTS equipment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(kind, name)
        )
    """)


    con.execute("""
        CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            UNIQUE(name, frequency)
        )
    """)


    con.execute("""
        CREATE TABLE IF NOT EXISTS tone_codes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            UNIQUE(name, code)
        )
    """)


    con.execute("""
        CREATE TABLE IF NOT EXISTS quality_values(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS power_values(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS operation_types_analog(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS operation_types_digital(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS modulation_modes_analog(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS modulation_modes_digital(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)


    con.execute("""
        CREATE TABLE IF NOT EXISTS digital_channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            tg TEXT,
            cc TEXT,
            call_group TEXT,
            operation TEXT,
            station_name TEXT,
            digital_id TEXT,
            contact TEXT,
            UNIQUE(name, frequency, tg, cc, call_group, operation, station_name, digital_id, contact)
        )
    """)


    if con.execute("SELECT COUNT(*) AS c FROM quality_values").fetchone()["c"] == 0:
        con.executemany("INSERT INTO quality_values(name) VALUES(?)", DEFAULT_QUALITY_VALUES)

    if con.execute("SELECT COUNT(*) AS c FROM power_values").fetchone()["c"] == 0:
        con.executemany("INSERT INTO power_values(name) VALUES(?)", DEFAULT_POWER_VALUES)

    if con.execute("SELECT COUNT(*) AS c FROM operation_types_analog").fetchone()["c"] == 0:
        con.executemany("INSERT INTO operation_types_analog(name) VALUES(?)", DEFAULT_ANALOG_OPERATION_TYPES)

    if con.execute("SELECT COUNT(*) AS c FROM operation_types_digital").fetchone()["c"] == 0:
        con.executemany("INSERT INTO operation_types_digital(name) VALUES(?)", DEFAULT_DIGITAL_OPERATION_TYPES)

    if con.execute("SELECT COUNT(*) AS c FROM modulation_modes_analog").fetchone()["c"] == 0:
        con.executemany("INSERT INTO modulation_modes_analog(name) VALUES(?)", DEFAULT_ANALOG_MODULATION_MODES)

    if con.execute("SELECT COUNT(*) AS c FROM modulation_modes_digital").fetchone()["c"] == 0:
        con.executemany("INSERT INTO modulation_modes_digital(name) VALUES(?)", DEFAULT_DIGITAL_MODULATION_MODES)

    if con.execute("SELECT COUNT(*) AS c FROM digital_channels").fetchone()["c"] == 0:
        con.executemany(
            """
            INSERT INTO digital_channels(
                name, frequency, tg, cc, call_group, operation, station_name, digital_id, contact
            )
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            DEFAULT_DIGITAL_CHANNELS,
        )

    if con.execute("SELECT COUNT(*) AS c FROM tone_codes").fetchone()["c"] == 0:
        con.executemany("INSERT INTO tone_codes(name, code) VALUES(?, ?)", DEFAULT_CTCSS_DCS_CODES)

    if con.execute("SELECT COUNT(*) AS c FROM channels").fetchone()["c"] == 0:
        con.executemany(
            "INSERT INTO channels(name, frequency) VALUES(?, ?)",
            [(f"PMR {ch}", f"{fr:.5f}") for ch, fr in PMR_CHANNELS.items()],
        )

    con.commit()
    return con


# Malé vyskakovací okno pro výběr data z kalendáře.
class CalendarPopup:


    # Inicializace okna nebo části aplikace.
    def __init__(self, parent, target_var):
        self.parent=parent
        self.target_var=target_var

        today=datetime.now()

        current=target_var.get().strip()
        try:
            dt=datetime.strptime(current,"%Y-%m-%d")
            self.year=dt.year
            self.month=dt.month
        except Exception:
            self.year=today.year
            self.month=today.month

        self.win=tk.Toplevel(parent)
        self.win.configure(bg=THEME['bg'])
        self.win.title("Výběr data")
        self.win.geometry("360x360")
        self.win.resizable(False,False)
        self.win.transient(parent)


        self.build()
        self.win.update_idletasks()
        self.win.grab_set()

    # Sestaví obsah okna kalendáře.
    def build(self):
        top=ttk.Frame(self.win,padding=8)
        top.pack(fill='x')

        ttk.Button(top,text='◀',width=4,command=self.prev_month).pack(side='left')

        self.month_label=tk.StringVar()
        ttk.Label(top,textvariable=self.month_label,font=('TkDefaultFont',10,'bold'),anchor='center').pack(side='left',expand=True,fill='x')

        ttk.Button(top,text='▶',width=4,command=self.next_month).pack(side='left')

        year_frame=ttk.Frame(self.win,padding=(8,0,8,4))
        year_frame.pack(fill='x')

        ttk.Label(year_frame,text='Rok:').pack(side='left')
        years=[str(y) for y in range(datetime.now().year-10, datetime.now().year+11)]
        self.year_var=tk.StringVar(value=str(self.year))
        self.year_combo=ttk.Combobox(year_frame,textvariable=self.year_var,values=years,width=8,state='readonly')
        self.year_combo.pack(side='left',padx=5)
        self.year_combo.bind('<<ComboboxSelected>>',self.year_changed)

        self.days_frame=ttk.Frame(self.win,padding=8)
        self.days_frame.pack(fill='both',expand=True)

        bottom=ttk.Frame(self.win,padding=8)
        bottom.pack(fill='x')
        ttk.Button(bottom,text='Dnes',command=self.today).pack(side='left')
        ttk.Button(bottom,text='Zavřít',command=self.win.destroy).pack(side='right')

        self.draw_calendar()

    # Vrátí český název měsíce.
    def month_name(self, m):
        names=[
            'leden','únor','březen','duben','květen','červen',
            'červenec','srpen','září','říjen','listopad','prosinec'
        ]
        return names[m-1]

    # Vykreslí aktuální měsíc v kalendáři.
    def draw_calendar(self):
        self.month_label.set(f"{self.month_name(self.month)} {self.year}")
        self.year_var.set(str(self.year))

        for w in self.days_frame.winfo_children():
            w.destroy()


        day_names=['Po','Út','St','Čt','Pá','So','Ne']
        for col,name in enumerate(day_names):
            ttk.Label(self.days_frame,text=name,font=('TkDefaultFont',9,'bold'),anchor='center').grid(row=0,column=col,sticky='nsew',padx=3,pady=3)

        cal=calendar.Calendar(firstweekday=0)
        weeks=cal.monthdayscalendar(self.year,self.month)

        selected_date=self.target_var.get().strip()

        for r,week in enumerate(weeks,start=1):
            for c,day in enumerate(week):
                if day==0:
                    ttk.Label(self.days_frame,text='').grid(row=r,column=c,sticky='nsew',padx=3,pady=3)
                    continue

                date_text=f"{self.year:04d}-{self.month:02d}-{day:02d}"
                text= str(day)

                if date_text == selected_date:
                    btn=ttk.Button(self.days_frame,text=text,width=4,command=lambda d=day:self.select_day(d))
                else:
                    btn=ttk.Button(self.days_frame,text=text,width=4,command=lambda d=day:self.select_day(d))

                btn.grid(row=r,column=c,sticky='nsew',padx=3,pady=3)

        for c in range(7):
            self.days_frame.columnconfigure(c, weight=1, minsize=42)
        for r in range(1, 7):
            self.days_frame.rowconfigure(r, weight=1, minsize=32)

    # Přepne kalendář na předchozí měsíc.
    def prev_month(self):
        self.month-=1
        if self.month<1:
            self.month=12
            self.year-=1
        self.draw_calendar()

    # Přepne kalendář na další měsíc.
    def next_month(self):
        self.month+=1
        if self.month>12:
            self.month=1
            self.year+=1
        self.draw_calendar()

    # Zareaguje na změnu vybraného roku.
    def year_changed(self,event=None):
        try:
            self.year=int(self.year_var.get())
        except Exception:
            self.year=datetime.now().year
        self.draw_calendar()

    # Nastaví dnešní datum.
    def today(self):
        now=datetime.now()
        self.year=now.year
        self.month=now.month
        self.target_var.set(now.strftime("%Y-%m-%d"))
        self.win.destroy()

    # Uloží vybraný den a zavře kalendář.
    def select_day(self, day):
        self.target_var.set(f"{self.year:04d}-{self.month:02d}-{day:02d}")
        self.win.destroy()


# Pomocný ovládací prvek pro výběr data a času ve filtru.
class DateTimeSelector:


    # Inicializace okna nebo části aplikace.
    def __init__(self, parent, label, x, y):
        self.parent = parent
        now = datetime.now()
        self.enabled = tk.BooleanVar(value=False)
        self.date = tk.StringVar(value=now.strftime("%Y-%m-%d"))
        self.hour = tk.StringVar(value="00" if label.lower().startswith("od") else "23")
        self.minute = tk.StringVar(value="00" if label.lower().startswith("od") else "59")

        self.label = ttk.Label(parent, text=label, style='Card.TLabel', anchor='w')
        self.label.place(x=x, y=y + 3, width=32, height=28)

        self.date_label = tk.Label(
            parent,
            textvariable=self.date,
            anchor="w",
            padx=8,
            bg=THEME["entry_bg"],
            fg=THEME["panel_fg"],
            relief="solid",
            bd=1
        )
        self.date_label.place(x=x + 34, y=y, width=120, height=32)


        self.calendar_button = ttk.Button(parent, text="📅", command=self.open_calendar)
        self.calendar_button.place(x=x + 158, y=y, width=40, height=32)

        self.h = ttk.Combobox(parent, textvariable=self.hour, values=[f"{h:02d}" for h in range(24)], state="readonly")
        self.h.place(x=x + 208, y=y, width=58, height=32)

        self.colon = ttk.Label(parent, text=":", style='Card.TLabel', anchor="center")
        self.colon.place(x=x + 268, y=y + 3, width=12, height=26)

        self.mi = ttk.Combobox(parent, textvariable=self.minute, values=[f"{m:02d}" for m in range(60)], state="readonly")
        self.mi.place(x=x + 282, y=y, width=58, height=32)

        self.h.bind('<<ComboboxSelected>>', self.mark_enabled)
        self.mi.bind('<<ComboboxSelected>>', self.mark_enabled)

    # Označí datumový filtr jako aktivní.
    def mark_enabled(self, event=None):
        self.enabled.set(True)

    # Rezervovaná funkce pro budoucí úpravu stavu prvků.
    def update_state(self):
        pass

    # Otevře malé okno pro výběr data.
    def open_calendar(self):
        self.enabled.set(True)
        CalendarPopup(self.parent, self.date)

    # Vypne daný datumový filtr.
    def clear(self):
        self.enabled.set(False)

    # Vrátí datum a čas filtru ve formátu vhodném pro databázi.
    def get_datetime(self):
        if not self.enabled.get():
            return ""
        value = f"{self.date.get()} {self.hour.get()}:{self.minute.get()}:00"
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Filtr data", f"Neplatné datum/čas:\n{value}")
            return None
        return value


# Hlavní třída celé aplikace Deník spojení.
class App:


    # Inicializace okna nebo části aplikace.
    def __init__(self, root):


        self.root=root; self.root.title(APP_TITLE); self.root.geometry('1500x760'); self.root.minsize(1040,650)


        self.con=db_connect(); self.sort_col='dt'; self.sort_desc=True


        apply_light_style(self.root)
        self.menu(); self.ui(); self.load_user_panel(); self.load_rows()

    # Načte hodnotu nastavení z databáze.
    def getset(self,k,d=''):
        r=self.con.execute('SELECT value FROM settings WHERE key=?',(k,)).fetchone(); return r['value'] if r else d
    # Uloží hodnotu nastavení do databáze.
    def setset(self,k,v):
        self.con.execute('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)',(k,v)); self.con.commit()

    # Vytvoří horní menu aplikace.
    def menu(self):


        m=tk.Menu(self.root); f=tk.Menu(m,tearoff=False)
        f.add_command(label='Exportovat záznamy do CSV', command=self.export_csv)
        f.add_command(label='Import z CSV', command=self.import_csv)
        f.add_separator(); f.add_command(label='Konec', command=self.root.destroy); m.add_cascade(label='Soubor', menu=f)

        s=tk.Menu(m,tearoff=False)
        s.add_command(label='Nastavení uživatele', command=self.user_settings)
        s.add_command(label='Nastavení zařízení', command=self.equipment_settings)
        s.add_command(label='Nastavení výkonů', command=self.power_value_settings)
        s.add_command(label='Nastavení režimů modulace', command=self.modulation_mode_settings)
        s.add_command(label='Nastavení typů spojení', command=self.operation_type_settings)
        s.add_command(label='Nastavení kvality spojení', command=self.quality_value_settings)
        s.add_command(label='Nastavení analogových kanálů', command=self.analog_settings)
        s.add_command(label='Nastavení digitálních kanálů', command=self.digital_channel_settings)
        m.add_cascade(label='Nastavení', menu=s)

        h=tk.Menu(m,tearoff=False)
        h.add_command(
            label='O programu',
            command=lambda: messagebox.showinfo(
                'O programu',
                f'{APP_TITLE}\nVerze: {APP_VERSION}'
            )
        )
        m.add_cascade(label='Nápověda', menu=h)

        self.root.config(menu=m)

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):


        PAD = 14
        main = ttk.Frame(self.root)
        main.place(x=0, y=0, relwidth=1, relheight=1)


        header = ttk.Frame(main)
        header.place(x=PAD, y=10, relwidth=1.0, width=-(PAD * 2), height=92)

        ttk.Label(header, text='📻 Deník spojení', style='BigTitle.TLabel').place(x=0, y=0, width=430, height=36)
        ttk.Label(
            header,
            text='Lokální deník spojení, poslechu a testů pro rádiový provoz',
            style='Subtitle.TLabel'
        ).place(x=2, y=38, width=720, height=24)

        ttk.Button(header, text='🔄 Obnovit', command=self.load_rows).place(relx=1.0, x=-300, y=16, width=130, height=38)
        ttk.Button(
            header,
            text='✚  Vytvořit záznam',
            style='Accent.TButton',
            command=lambda: RecordWindow(self)
        ).place(relx=1.0, x=-160, y=16, width=155, height=38)


        ttk.Label(main, text='Stanice a rychlé akce', font=('Ubuntu', 10, 'bold')).place(x=PAD, y=104, width=250, height=22)
        station_card = ttk.Frame(main, style='Card.TFrame')
        station_card.place(x=PAD, y=128, relwidth=1.0, width=-(PAD * 2), height=56)

        self.user_var = tk.StringVar()
        ttk.Label(station_card, textvariable=self.user_var, style='CardTitle.TLabel',font=('Ubuntu', 16, 'bold'), anchor='center').place(
            x=16, y=13, relwidth=1.0, width=-32, height=28
        )


        ttk.Label(main, text='Filtry a vyhledávání', font=('Ubuntu', 10, 'bold')).place(x=PAD, y=194, width=250, height=22)
        flt = ttk.Frame(main, style='Card.TFrame')
        flt.place(x=PAD, y=218, relwidth=1.0, width=-(PAD * 2), height=118)

        ttk.Label(flt, text='Textové hledání', style='Card.TLabel').place(x=18, y=12, width=180, height=22)
        self.filter_var = tk.StringVar()
        ttk.Entry(flt, textvariable=self.filter_var).place(x=18, y=38, width=270, height=32)
        ttk.Label(flt, text='🔍', style='Card.TLabel', anchor='center').place(x=253, y=41, width=28, height=26)

        ttk.Label(flt, text='Kanál', style='Card.TLabel').place(x=310, y=12, width=100, height=22)
        self.filter_channel = tk.StringVar(value='vše')
        self.filter_channel_combo = ttk.Combobox(flt, textvariable=self.filter_channel, state='readonly')
        self.filter_channel_combo.place(x=310, y=38, width=170, height=32)

        ttk.Label(flt, text='Typ provozu', style='Card.TLabel').place(x=500, y=12, width=150, height=22)
        self.filter_type = tk.StringVar(value='vše')
        self.filter_type_combo = ttk.Combobox(flt, textvariable=self.filter_type, state='readonly')
        self.filter_type_combo.place(x=500, y=38, width=170, height=32)


        self.filter_from_picker = DateTimeSelector(flt, 'Od:', 18, 78)
        self.filter_to_picker = DateTimeSelector(flt, 'Do:', 360, 78)

        ttk.Button(flt, text='🔎 Použít filtr', command=self.load_rows).place(relx=1.0, x=-240, y=36, width=115, height=36)
        ttk.Button(flt, text='✖ Zrušit filtr', command=self.clear_filter).place(relx=1.0, x=-115, y=36, width=110, height=36)

        self.load_filter_channels()
        self.load_filter_operation_types()


        ttk.Label(main, text='Záznamy', font=('Ubuntu', 10, 'bold')).place(x=PAD, y=346, width=250, height=22)
        table_container = ttk.Frame(main, style='Card.TFrame')
        table_container.place(x=PAD, y=370, relwidth=1.0, width=-(PAD * 2), relheight=1.0, height=-418)

        table_frame = ttk.Frame(table_container, style='Card.TFrame')
        table_frame.place(x=10, y=10, relwidth=1.0, width=-20, relheight=1.0, height=-20)

        self.cols = (
            'dt', 'my_locator', 'locator', 'my_call', 'other_call', 'mode', 'operation_type',
            'power', 'modulation', 'distance_km', 'bearing_deg', 'quality', 'edit', 'delete'
        )

        heads = {
            'dt': 'Datum a čas',
            'my_locator': 'Můj lokátor',
            'locator': 'Lokátor PS',
            'my_call': 'Moje značka',
            'other_call': 'Protistanice',
            'mode': 'Režim',
            'operation_type': 'Typ',
            'power': 'Výkon',
            'modulation': 'Modulace',
            'distance_km': 'km',
            'bearing_deg': 'Azimut',
            'quality': 'Kvalita',
            'edit': '👁',
            'delete': '🗑',
        }

        widths = {
            'dt': 155,
            'my_locator': 105,
            'locator': 105,
            'my_call': 155,
            'other_call': 135,
            'mode': 80,
            'operation_type': 82,
            'power': 72,
            'modulation': 92,
            'distance_km': 72,
            'bearing_deg': 82,
            'quality': 120,
            'edit': 52,
            'delete': 52,
        }

        self.tree = ttk.Treeview(table_frame, columns=self.cols, show='headings', selectmode='browse')
        self.tree.place(x=0, y=0, relwidth=1.0, width=-18, relheight=1.0)
        self.tree.tag_configure('odd', background=THEME['table_row'])
        self.tree.tag_configure('even', background=THEME['table_alt'])

        for c in self.cols:
            self.tree.heading(c, text=heads[c], command=lambda x=c: self.sort(x))
            self.tree.column(c, width=widths[c], anchor='center' if c in ('mode', 'power', 'modulation', 'distance_km', 'bearing_deg', 'edit', 'delete') else 'w')

        sb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        sb.place(relx=1.0, x=-18, y=0, width=18, relheight=1.0)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.bind('<ButtonRelease-1>', self.click)
        self.tree.bind('<Double-1>', lambda e: self.detail_selected())


        self.status = tk.StringVar(value='Připraveno')
        ttk.Label(main, textvariable=self.status, anchor='w', style='Subtitle.TLabel').place(
            x=PAD, rely=1.0, y=-32, relwidth=1.0, width=-(PAD * 2 + 150), height=24
        )
        ttk.Button(
            main,
            text='🖨  Tisk',
            command=self.print_filtered_rows
        ).place(relx=1.0, x=-138, rely=1.0, y=-40, width=124, height=34)

    # Načte volačku a lokátor uživatele do horního panelu.
    def load_user_panel(self):
        self.user_var.set(f"Moje volačka: {self.getset('my_call','-') or '-'}     Domovský lokátor: {self.getset('my_locator','-') or '-'}")

    # Načte dostupné kanály do filtru.
    def load_filter_channels(self):
        if not hasattr(self,'filter_channel_combo'):
            return
        values=['vše']
        for r in self.con.execute('SELECT id,name,frequency FROM channels ORDER BY id'):
            values.append(f"{r['name']} / {r['frequency']} MHz")
        self.filter_channel_combo['values']=values
        if self.filter_channel.get() not in values:
            self.filter_channel.set('vše')

    # Načte typy provozu do filtru.
    def load_filter_operation_types(self):
        if not hasattr(self, 'filter_type_combo'):
            return
        values = ['vše']
        for table in ('operation_types_analog', 'operation_types_digital'):
            for r in self.con.execute(f'SELECT name FROM {table} ORDER BY id'):
                if r['name'] not in values:
                    values.append(r['name'])
        self.filter_type_combo['values'] = values
        if self.filter_type.get() not in values:
            self.filter_type.set('vše')

    # Vymaže všechny filtry a znovu načte záznamy.
    def clear_filter(self):
        self.filter_var.set('')
        self.filter_from_picker.clear()
        self.filter_to_picker.clear()
        self.filter_channel.set('vše')
        self.filter_type.set('vše')
        self.load_rows()

    # Nastaví řazení podle vybraného sloupce.
    def sort(self,c):
        if c in ('edit','delete'): return
        self.sort_desc = not self.sort_desc if self.sort_col==c else False; self.sort_col=c; self.load_rows()
    # Vrátí SQL řazení pro aktuální tabulku.
    def order_sql(self):
        mp={'dt':'dt','my_locator':'my_locator','locator':'locator','my_call':'my_call','other_call':'other_call','distance_km':'CAST(distance_km AS REAL)','bearing_deg':'CAST(bearing_deg AS REAL)','quality':'quality','operation_type':'operation_type','mode':'mode','power':'power','modulation':'modulation'}
        return f"{mp.get(self.sort_col,'dt')} {'DESC' if self.sort_desc else 'ASC'}, id DESC"

    # Načte záznamy z databáze podle aktuálních filtrů.
    def load_rows(self):
        self.load_filter_channels()
        self.load_filter_operation_types()
        for i in self.tree.get_children(): self.tree.delete(i)

        where=[]
        params=[]

        q=self.filter_var.get().strip()
        if q:
            like=f'%{q}%'
            where.append("(dt LIKE ? OR my_locator LIKE ? OR locator LIKE ? OR my_call LIKE ? OR other_call LIKE ? OR quality LIKE ? OR mode LIKE ? OR power LIKE ? OR modulation LIKE ? OR device LIKE ? OR antenna LIKE ? OR note LIKE ? OR operation_type LIKE ? OR channel_name LIKE ? OR frequency LIKE ?)")
            params += [like]*15

        dfrom=self.filter_from_picker.get_datetime()
        if dfrom is None:
            return
        if dfrom:
            where.append("dt >= ?")
            params.append(dfrom)

        dto=self.filter_to_picker.get_datetime()
        if dto is None:
            return
        if dto:
            where.append("dt <= ?")
            params.append(dto)

        typ=self.filter_type.get().strip()
        if typ and typ!='vše':
            where.append("operation_type = ?")
            params.append(typ)

        ch=self.filter_channel.get().strip()
        if ch and ch!='vše':

            if ' / ' in ch:
                name, rest = ch.split(' / ',1)
                freq = rest.replace(' MHz','').strip()
                where.append("(channel_name = ? AND frequency = ?)")
                params += [name.strip(), freq]
            else:
                where.append("channel_name = ?")
                params.append(ch)

        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        rows=self.con.execute(f'SELECT * FROM logs {where_sql} ORDER BY {self.order_sql()}',params).fetchall()
        for index, r in enumerate(rows):
            tag = 'even' if index % 2 else 'odd'
            self.tree.insert(
                '',
                'end',
                iid=str(r['id']),
                tags=(tag,),
                values=(
                    r['dt'],
                    r['my_locator'] or '',
                    r['locator'] or '',
                    r['my_call'] or '',
                    r['other_call'] or '',
                    r['mode'] or 'Analogový',
                    r['operation_type'] or '',
                    r['power'] or '',
                    r['modulation'] or '',
                    r['distance_km'] or '',
                    r['bearing_deg'] or '',
                    r['quality'] or '',
                    '👁',
                    '🗑'
                )
            )
        self.status.set(f'Záznamů: {len(rows)}')

    # Načte jeden konkrétní záznam podle ID.
    def get_record(self,rid): return self.con.execute('SELECT * FROM logs WHERE id=?',(rid,)).fetchone()
    # Zpracuje kliknutí v tabulce, například detail nebo smazání.
    def click(self,e):
        if self.tree.identify('region',e.x,e.y)!='cell': return
        row=self.tree.identify_row(e.y); col=self.tree.identify_column(e.x)
        if not row or not col: return
        name=self.cols[int(col[1:])-1]; rid=int(row)
        if name=='edit': DetailWindow(self,rid)
        elif name=='delete': self.delete(rid)
    # Otevře detail aktuálně vybraného záznamu.
    def detail_selected(self):
        s=self.tree.selection();
        if s: DetailWindow(self,int(s[0]))
    # Smaže vybraný záznam po potvrzení.
    def delete(self,rid):
        r=self.get_record(rid)
        if r and messagebox.askyesno('Smazat zaznam',f"Opravdu smazat záznam?\n\n{r['dt']} / {r['other_call'] or r['locator'] or 'bez popisu'}"):
            self.con.execute('DELETE FROM logs WHERE id=?',(rid,)); self.con.commit(); self.load_rows()

    # Otevře nastavení uživatele.
    def user_settings(self): UserSettings(self)
    # Otevře nastavení zařízení a antén.
    def equipment_settings(self): EquipmentSettings(self)
    # Otevře nastavení analogových kanálů.
    def analog_settings(self): AnalogSettings(self)
    # Otevře nastavení digitálních kanálů.
    def digital_channel_settings(self): DigitalChannelSettings(self)
    # Otevře nastavení typů spojení.
    def operation_type_settings(self):
        DualSimpleListSettings(
            self,
            'Nastavení typů spojení',
            'Typ spojení',
            'operation_types_analog',
            DEFAULT_ANALOG_OPERATION_TYPES,
            'operation_types_digital',
            DEFAULT_DIGITAL_OPERATION_TYPES,
        )
    # Otevře nastavení kvality spojení.
    def quality_value_settings(self): SimpleListSettings(self, 'Nastavení kvality spojení', 'quality_values', 'Kvalita spojení', DEFAULT_QUALITY_VALUES)
    # Otevře nastavení výkonů.
    def power_value_settings(self): SimpleListSettings(self, 'Nastavení výkonů', 'power_values', 'Výkon', DEFAULT_POWER_VALUES)
    # Otevře nastavení modulací.
    def modulation_mode_settings(self):
        DualSimpleListSettings(
            self,
            'Nastavení režimů modulace',
            'Režim modulace',
            'modulation_modes_analog',
            DEFAULT_ANALOG_MODULATION_MODES,
            'modulation_modes_digital',
            DEFAULT_DIGITAL_MODULATION_MODES,
        )


    # Vrátí aktuálně vyfiltrované záznamy pro tisk nebo export.
    def filtered_rows_for_output(self):


        where = []
        params = []

        q = self.filter_var.get().strip()
        if q:
            like = f'%{q}%'
            where.append(
                "(dt LIKE ? OR my_locator LIKE ? OR locator LIKE ? OR my_call LIKE ? "
                "OR other_call LIKE ? OR quality LIKE ? OR mode LIKE ? OR power LIKE ? "
                "OR modulation LIKE ? OR device LIKE ? OR antenna LIKE ? OR note LIKE ? "
                "OR operation_type LIKE ? OR channel_name LIKE ? OR frequency LIKE ?)"
            )
            params += [like] * 15

        dfrom = self.filter_from_picker.get_datetime()
        if dfrom is None:
            return None
        if dfrom:
            where.append("dt >= ?")
            params.append(dfrom)

        dto = self.filter_to_picker.get_datetime()
        if dto is None:
            return None
        if dto:
            where.append("dt <= ?")
            params.append(dto)

        typ = self.filter_type.get().strip()
        if typ and typ != 'vše':
            where.append("operation_type = ?")
            params.append(typ)

        ch = self.filter_channel.get().strip()
        if ch and ch != 'vše':
            if ' / ' in ch:
                name, rest = ch.split(' / ', 1)
                freq = rest.replace(' MHz', '').strip()
                where.append("(channel_name = ? AND frequency = ?)")
                params += [name.strip(), freq]
            else:
                where.append("channel_name = ?")
                params.append(ch)

        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        return list(self.con.execute(
            f'SELECT * FROM logs {where_sql} ORDER BY {self.order_sql()}',
            params
        ))

    # Vytvoří textový popis aktuálně nastaveného filtru.
    def current_filter_description(self):


        parts = []
        text = self.filter_var.get().strip()
        if text:
            parts.append(f'Text: {text}')

        if self.filter_from_picker.enabled.get():
            parts.append(
                f'Od: {self.filter_from_picker.date.get()} '
                f'{self.filter_from_picker.hour.get()}:{self.filter_from_picker.minute.get()}'
            )

        if self.filter_to_picker.enabled.get():
            parts.append(
                f'Do: {self.filter_to_picker.date.get()} '
                f'{self.filter_to_picker.hour.get()}:{self.filter_to_picker.minute.get()}'
            )

        channel = self.filter_channel.get().strip()
        if channel and channel != 'vše':
            parts.append(f'Kanál: {channel}')

        operation_type = self.filter_type.get().strip()
        if operation_type and operation_type != 'vše':
            parts.append(f'Typ provozu: {operation_type}')

        return ' | '.join(parts) if parts else 'Bez filtru'

    # Vytvoří HTML stránku pro tisk záznamů.
    def build_print_html(self, rows):


        def esc(value):
            return html.escape(str(value if value is not None else ''))

        printed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        my_call = self.getset('my_call', '-') or '-'
        my_locator = self.getset('my_locator', '-') or '-'
        filter_text = self.current_filter_description()

        headers = [
            'Datum a čas', 'Moje značka', 'Protistanice', 'Můj lokátor',
            'Lokátor PS', 'Režim', 'Kanál', 'Frekvence', 'Typ',
            'Výkon', 'Modulace', 'km', 'Azimut', 'Kvalita', 'Poznámka'
        ]

        body_rows = []
        for r in rows:
            channel_text = r['channel_name'] or (f"PMR {r['channel']}" if r['channel'] else '')
            body_rows.append(
                '<tr>'
                f'<td>{esc(r["dt"])}</td>'
                f'<td>{esc(r["my_call"])}</td>'
                f'<td>{esc(r["other_call"])}</td>'
                f'<td>{esc(r["my_locator"])}</td>'
                f'<td>{esc(r["locator"])}</td>'
                f'<td>{esc(r["mode"] or "Analogový")}</td>'
                f'<td>{esc(channel_text)}</td>'
                f'<td>{esc(r["frequency"])}</td>'
                f'<td>{esc(r["operation_type"])}</td>'
                f'<td>{esc(r["power"])}</td>'
                f'<td>{esc(r["modulation"])}</td>'
                f'<td>{esc(r["distance_km"])}</td>'
                f'<td>{esc(r["bearing_deg"])}</td>'
                f'<td>{esc(r["quality"])}</td>'
                f'<td>{esc(r["note"])}</td>'
                '</tr>'
            )

        header_cells = ''.join(f'<th>{esc(h)}</th>' for h in headers)
        rows_html = '\n'.join(body_rows)

        return f"""<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<title>{esc(APP_TITLE)} - tisk</title>
<style>
    body {{
        font-family: Arial, DejaVu Sans, sans-serif;
        color: #111;
        margin: 18px;
        font-size: 11px;
    }}
    h1 {{
        margin: 0 0 4px 0;
        font-size: 22px;
    }}
    .meta {{
        margin: 2px 0;
        color: #333;
        font-size: 12px;
    }}
    .toolbar {{
        margin: 12px 0 16px 0;
    }}
    button {{
        padding: 8px 14px;
        font-weight: bold;
        cursor: pointer;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }}
    th, td {{
        border: 1px solid #777;
        padding: 4px 5px;
        vertical-align: top;
        word-wrap: break-word;
        overflow-wrap: anywhere;
    }}
    th {{
        background: #e7eef6;
        font-weight: bold;
        text-align: left;
    }}
    tr:nth-child(even) td {{
        background: #f6f8fb;
    }}
    .small {{
        font-size: 10px;
        color: #555;
    }}
    @media print {{
        .toolbar {{ display: none; }}
        body {{ margin: 10mm; }}
        table {{ font-size: 9px; }}
        th, td {{ padding: 3px; }}
    }}
</style>
<script>
    window.addEventListener('load', function() {{
        setTimeout(function() {{ window.print(); }}, 400);
    }});
</script>
</head>
<body>
    <h1>{esc(APP_TITLE)}</h1>
    <div class="meta"><strong>Verze:</strong> {esc(APP_VERSION)}</div>
    <div class="meta"><strong>Moje volačka:</strong> {esc(my_call)} &nbsp;&nbsp; <strong>Domovský lokátor:</strong> {esc(my_locator)}</div>
    <div class="meta"><strong>Vytištěno:</strong> {esc(printed_at)}</div>
    <div class="meta"><strong>Filtr:</strong> {esc(filter_text)}</div>
    <div class="meta"><strong>Počet záznamů:</strong> {len(rows)}</div>

    <div class="toolbar">
        <button onclick="window.print()">🖨 Tisk</button>
    </div>

    <table>
        <thead><tr>{header_cells}</tr></thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    <p class="small">Tisková sestava byla vytvořena z aktuálně vyfiltrovaných záznamů v programu.</p>
</body>
</html>"""

    # Otevře tiskovou sestavu v prohlížeči.
    def print_filtered_rows(self):


        rows = self.filtered_rows_for_output()
        if rows is None:
            return
        if not rows:
            messagebox.showinfo('Tisk', 'Podle aktuálního filtru nejsou k tisku žádné záznamy.')
            return

        try:
            html_text = self.build_print_html(rows)
            fd, path = tempfile.mkstemp(prefix='denik_spojeni_tisk_', suffix='.html')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(html_text)

            webbrowser.open(Path(path).as_uri())
            self.status.set(f'Tisková sestava otevřena. Záznamů: {len(rows)}')
        except Exception as e:
            messagebox.showerror('Tisk', f'Tiskovou sestavu se nepodařilo vytvořit:\n\n{e}')


    # Exportuje všechny záznamy do CSV souboru.
    def export_csv(self):
        p=filedialog.asksaveasfilename(title='Export CSV',defaultextension='.csv',filetypes=[('CSV soubor','*.csv'),('Vsechny soubory','*.*')],initialfile=f'denik_{date.today().isoformat()}.csv')
        if not p: return
        headers=['dt','channel','channel_name','frequency','tone','my_call','other_call','my_locator','locator','distance_km','bearing_deg','direction','operation_type','signal','quality','power','modulation','mode','tg','cc','call_group','digital_id','contact','device','antenna','note']
        rows=self.con.execute('SELECT * FROM logs ORDER BY dt ASC,id ASC').fetchall()
        with open(p,'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f,delimiter=';'); w.writerow(headers)
            for r in rows: w.writerow([r[h] if r[h] is not None else '' for h in headers])
        messagebox.showinfo('Export',f'Export hotov:\n{p}')

    # Naimportuje záznamy z CSV souboru.
    def import_csv(self):
        p=filedialog.askopenfilename(title='Import CSV',filetypes=[('CSV soubor','*.csv'),('Vsechny soubory','*.*')])
        if not p: return
        n=0
        with open(p,'r',encoding='utf-8',newline='') as f:
            for r in csv.DictReader(f,delimiter=';'):
                data={k:r.get(k,'') for k in ['dt','channel_name','frequency','tone','my_call','other_call','my_locator','locator','distance_km','bearing_deg','direction','operation_type','signal','quality','power','modulation','mode','tg','cc','call_group','digital_id','contact','device','antenna','note']}
                data['dt']=data['dt'] or datetime.now().strftime('%Y-%m-%d %H:%M:%S'); data['channel']=int(r.get('channel','1') or 1)
                self.con.execute('''INSERT INTO logs(dt,channel,channel_name,frequency,tone,my_call,other_call,my_locator,locator,distance_km,bearing_deg,direction,operation_type,signal,quality,power,modulation,mode,tg,cc,call_group,digital_id,contact,device,antenna,note) VALUES(:dt,:channel,:channel_name,:frequency,:tone,:my_call,:other_call,:my_locator,:locator,:distance_km,:bearing_deg,:direction,:operation_type,:signal,:quality,:power,:modulation,:mode,:tg,:cc,:call_group,:digital_id,:contact,:device,:antenna,:note)''',data); n+=1
        self.con.commit(); self.load_rows(); messagebox.showinfo('Import',f'Importovano zaznamů: {n}')


# Okno pro vytvoření nebo úpravu jednoho záznamu spojení.
class RecordWindow:
    # Inicializace okna nebo části aplikace.
    def __init__(self,app,rid=None):
        self.app=app; self.con=app.con; self.rid=rid
        self.win=tk.Toplevel(app.root)
        self.win.configure(bg=THEME['bg'])
        self.win.title('Nový záznam' if rid is None else 'Editace záznamu')
        self.win.geometry('1020x650')
        self.win.minsize(760, 500)
        self.win.transient(app.root)
        self.win.grab_set()
        self._mousewheel_bound = False
        self.win.protocol('WM_DELETE_WINDOW', self.close_window)
        self.ui(); self.load_combo(); self.defaults() if rid is None else self.load(rid)

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):


        self.form_width = 1020
        self.form_height = 820

        main = ttk.Frame(self.win)
        main.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(main, bg=THEME['bg'], highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0, relwidth=1.0, width=-18, relheight=1.0)

        self.scrollbar = ttk.Scrollbar(main, orient='vertical', command=self.canvas.yview)
        self.scrollbar.place(relx=1.0, x=-18, y=0, width=18, relheight=1.0)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.configure(width=self.form_width, height=self.form_height)
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')

        self.scroll_frame.bind('<Configure>', self.update_scroll_region)
        self.canvas.bind('<Configure>', self.resize_scroll_window)
        self.canvas.bind('<Enter>', self.bind_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_mousewheel)

        self.card = ttk.Frame(self.scroll_frame, style='Card.TFrame')
        self.card.place(x=18, y=18, width=self.form_width-36, height=self.form_height-36)

        self.record_mode=tk.StringVar(value='Analogový')
        self.dt=tk.StringVar()
        self.my_loc=tk.StringVar()
        self.loc=tk.StringVar()
        self.other_call=tk.StringVar()
        self.channel=tk.StringVar()
        self.channel_rows=[]
        self.freq=tk.StringVar()
        self.signal=tk.StringVar(value='3 - použitelný')
        self.quality=tk.StringVar(value='dobrá')
        self.typ=tk.StringVar(value='spojení')
        self.power=tk.StringVar()
        self.modulation=tk.StringVar(value='FM')
        self.tg=tk.StringVar()
        self.cc=tk.StringVar()
        self.call_group=tk.StringVar()
        self.digital_id=tk.StringVar()
        self.contact=tk.StringVar()
        self.device=tk.StringVar()
        self.antenna=tk.StringVar()
        self.tone=tk.StringVar()
        self.dist=tk.StringVar()
        self.bearing=tk.StringVar()
        self.direction=tk.StringVar()

        self.lx, self.ix = 24, 200


        self.rx, self.rix = 550, 715
        self.left_w = 310
        self.right_w = 220
        self.row_h = 34
        self.gap = 42

        def make_label(text, x, w=165):
            return ttk.Label(self.card, text=text, style='CardTitle.TLabel', anchor='w')

        def make_entry(var, readonly=False):
            return ttk.Entry(self.card, textvariable=var, state='readonly' if readonly else 'normal')

        def make_combo(var, values=None, readonly=True):
            return ttk.Combobox(self.card, textvariable=var, values=values or [], state='readonly' if readonly else 'normal')

        self.widgets = {}
        def pair(key, text, widget, side='left', label_w=165, widget_w=None):
            if side == 'left':
                x_lab, x_wid, ww = self.lx, self.ix, widget_w or self.left_w
            else:
                x_lab, x_wid, ww = self.rx, self.rix, widget_w or self.right_w
            lab = make_label(text, x_lab, label_w)
            self.widgets[key] = (lab, widget, x_lab, x_wid, ww)
            return widget


        self.mode_combo = pair('mode', 'Režim záznamu:', make_combo(self.record_mode, ['Analogový', 'Digitální']), 'left')
        self.mode_combo.bind('<<ComboboxSelected>>', lambda e: self.mode_changed())

        self.dt_entry = pair('dt', 'Datum/čas:', make_entry(self.dt), 'left')
        self.dt_entry.bind('<KeyRelease>', lambda ev: self.recalc())
        self.now_button = ttk.Button(self.card, text="🕘  Teď", command=self.set_now)

        self.my_loc_entry = pair('my_loc', 'Můj lokátor:', make_entry(self.my_loc), 'left')
        self.my_loc_entry.bind('<KeyRelease>', lambda ev: self.recalc())
        self.home_button = ttk.Button(self.card, text='Použij domovskou stanici', command=self.use_home)

        self.loc_entry = pair('loc', 'Lokátor protistanice:', make_entry(self.loc), 'left')
        self.loc_entry.bind('<KeyRelease>', lambda ev: self.recalc())
        pair('other_call', 'Volačka protistanice:', make_entry(self.other_call), 'left')


        self.channel_label = make_label('Kanál:', self.lx)
        self.channel_combo = make_combo(self.channel, [])
        self.channel_combo.bind('<<ComboboxSelected>>', lambda e: self.update_freq())
        self.freq_label = make_label('Frekvence MHz:', self.rx)
        self.freq_entry = make_entry(self.freq, readonly=True)

        self.typcombo = pair('typ', 'Typ:', make_combo(self.typ, []), 'left')
        self.signal_combo = pair('signal', 'Síla signálu:', make_combo(self.signal, SIGNAL_VALUES), 'right')
        self.qualitycombo = pair('quality', 'Kvalita:', make_combo(self.quality, []), 'left')
        self.powercombo = pair('power', 'Výkon:', make_combo(self.power, []), 'right')
        self.modcombo = pair('modulation', 'Modulace:', make_combo(self.modulation, []), 'left')


        self.tone_label = make_label('CTCSS/DCS:', self.rx)
        self.tonecombo = make_combo(self.tone, [])


        self.tg_label = make_label('TG:', self.lx, 50)
        self.tg_entry = make_entry(self.tg)
        self.cc_label = make_label('CC:', self.lx + 210, 40)
        self.cc_entry = make_entry(self.cc)
        self.group_label = make_label('Volací skupina:', self.rx)
        self.group_entry = make_entry(self.call_group)
        self.dmrid_label = make_label('DMR ID:', self.lx)
        self.dmrid_entry = make_entry(self.digital_id)
        self.contact_label = make_label('Kontakt:', self.rx)
        self.contact_entry = make_entry(self.contact)


        self.devcombo = pair('device', 'Zařízení:', make_combo(self.device, [], readonly=False), 'left')
        self.antcombo = pair('antenna', 'Anténa:', make_combo(self.antenna, [], readonly=False), 'right')
        pair('dist', 'Vzdálenost (km):', make_entry(self.dist, readonly=True), 'left', widget_w=160)
        pair('bearing', 'Azimut:', make_entry(self.bearing, readonly=True), 'right', widget_w=160)
        pair('direction', 'Směr:', make_entry(self.direction, readonly=True), 'left', widget_w=160)
        self.map_button = ttk.Button(self.card, text='📍  Mapa spojení', command=self.open_map)

        self.note_label = make_label('Poznámka:', self.lx)
        self.note = tk.Text(
            self.card, height=6, wrap='word', bg=THEME['panel'], fg=THEME['panel_fg'],
            insertbackground=THEME['panel_fg'], relief='solid', bd=1
        )
        self.save_button = ttk.Button(self.card, text='💾  Uložit', style='Accent.TButton', command=self.save)
        self.close_button = ttk.Button(self.card, text='✖  Zavřít', command=self.close_window)

        self.update_record_layout()

    # Umístí popisek a vstupní prvek do formuláře.
    def place_pair(self, key, y):
        lab, widget, x_lab, x_wid, width = self.widgets[key]
        lab.place(x=x_lab, y=y + 2, width=165, height=28)
        widget.place(x=x_wid, y=y, width=width, height=self.row_h)

    # Skryje popisek a vstupní prvek z formuláře.
    def hide_pair(self, key):
        lab, widget, *_ = self.widgets[key]
        lab.place_forget(); widget.place_forget()

    # Přestaví formulář podle analogového nebo digitálního režimu.
    def update_record_layout(self):

        mode = self.record_mode.get().strip() or 'Analogový'
        y = 22
        gap = self.gap


        for key in self.widgets:
            self.hide_pair(key)
        for w in [self.channel_label, self.channel_combo, self.freq_label, self.freq_entry,
                  self.tone_label, self.tonecombo, self.tg_label, self.tg_entry,
                  self.cc_label, self.cc_entry, self.group_label, self.group_entry,
                  self.dmrid_label, self.dmrid_entry, self.contact_label, self.contact_entry,
                  self.map_button, self.note_label, self.note, self.save_button, self.close_button,
                  self.now_button, self.home_button]:
            try: w.place_forget()
            except Exception: pass


        self.place_pair('mode', y); y += gap
        self.place_pair('dt', y); self.now_button.place(x=700, y=y, width=240, height=36); y += gap
        self.place_pair('my_loc', y); self.home_button.place(x=700, y=y, width=240, height=36); y += gap
        self.place_pair('loc', y); y += gap
        self.place_pair('other_call', y); y += gap + 8


        self.channel_label.configure(text='Digitální kanál:' if mode == 'Digitální' else 'Analogový kanál:')
        self.channel_label.place(x=self.lx, y=y + 2, width=165, height=28)
        self.channel_combo.place(x=self.ix, y=y, width=self.left_w, height=self.row_h)
        self.freq_label.place(x=self.rx, y=y + 2, width=150, height=28)
        self.freq_entry.place(x=self.rix, y=y, width=self.right_w, height=self.row_h)
        y += gap

        if mode == 'Digitální':
            self.place_pair('typ', y); self.place_pair('power', y); y += gap
            self.place_pair('modulation', y); self.place_pair('signal', y); y += gap
            self.tg_label.place(x=self.lx, y=y+2, width=50, height=28)
            self.tg_entry.place(x=self.ix, y=y, width=90, height=self.row_h)
            self.cc_label.place(x=self.ix + 110, y=y+2, width=40, height=28)
            self.cc_entry.place(x=self.ix + 150, y=y, width=70, height=self.row_h)
            self.group_label.place(x=self.rx, y=y+2, width=150, height=28)
            self.group_entry.place(x=self.rix, y=y, width=self.right_w, height=self.row_h)
            y += gap
            self.dmrid_label.place(x=self.lx, y=y+2, width=165, height=28)
            self.dmrid_entry.place(x=self.ix, y=y, width=self.left_w, height=self.row_h)
            self.contact_label.place(x=self.rx, y=y+2, width=150, height=28)
            self.contact_entry.place(x=self.rix, y=y, width=self.right_w, height=self.row_h)
            y += gap
        else:
            self.place_pair('typ', y); self.place_pair('signal', y); y += gap
            self.place_pair('quality', y)
            self.tone_label.place(x=self.rx, y=y + 2, width=150, height=28)
            self.tonecombo.place(x=self.rix, y=y, width=self.right_w, height=self.row_h)
            y += gap
            self.place_pair('power', y); self.place_pair('modulation', y); y += gap

        self.place_pair('device', y); self.place_pair('antenna', y); y += gap
        self.place_pair('dist', y); self.place_pair('bearing', y); y += gap
        self.place_pair('direction', y)


        self.map_button.place(x=self.ix + 180, y=y, width=210, height=36)
        y += gap + 8
        self.note_label.place(x=self.lx, y=y+2, width=165, height=28)
        self.note.place(x=self.ix, y=y, width=735, height=120)
        y += 138
        self.save_button.place(x=625, y=y, width=150, height=40)
        self.close_button.place(x=795, y=y, width=150, height=40)

        required_height = max(820, y + 80)
        self.form_height = required_height
        self.scroll_frame.configure(height=required_height)
        self.card.place_configure(height=required_height-36)
        self.update_scroll_region()
    # Aktualizuje rolovatelnou oblast formuláře.
    def update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    # Přizpůsobí šířku rolovacího formuláře velikosti okna.
    def resize_scroll_window(self, event=None):
        visible_width = max(event.width if event else self.form_width, self.form_width)
        self.canvas.itemconfigure(self.scroll_window, width=visible_width)
        self.scroll_frame.configure(width=visible_width)
        self.card.place_configure(width=visible_width-36)

    # Zapne rolování kolečkem myši.
    def bind_mousewheel(self, event=None):
        if self._mousewheel_bound:
            return
        self._mousewheel_bound = True
        self.win.bind_all('<MouseWheel>', self.on_mousewheel)
        self.win.bind_all('<Button-4>', self.on_mousewheel)
        self.win.bind_all('<Button-5>', self.on_mousewheel)

    # Vypne rolování kolečkem myši.
    def unbind_mousewheel(self, event=None):
        if not self._mousewheel_bound:
            return
        self._mousewheel_bound = False
        self.win.unbind_all('<MouseWheel>')
        self.win.unbind_all('<Button-4>')
        self.win.unbind_all('<Button-5>')

    # Zpracuje rolování kolečkem myši.
    def on_mousewheel(self, event):
        if getattr(event, 'num', None) == 4:
            self.canvas.yview_scroll(-3, 'units')
        elif getattr(event, 'num', None) == 5:
            self.canvas.yview_scroll(3, 'units')
        else:
            delta = int(-1 * (event.delta / 120))
            self.canvas.yview_scroll(delta * 3, 'units')

    # Bezpečně zavře okno a odpojí obsluhu kolečka myši.
    def close_window(self):
        self.unbind_mousewheel()
        self.win.destroy()

    # Načte hodnoty do rozbalovacích seznamů formuláře.
    def load_combo(self):
        self.devcombo['values']=[x['name'] for x in self.con.execute("SELECT name FROM equipment WHERE kind='device' ORDER BY name")]
        self.antcombo['values']=[x['name'] for x in self.con.execute("SELECT name FROM equipment WHERE kind='antenna' ORDER BY name")]
        self.channel_rows=list(self.con.execute('SELECT id,name,frequency FROM channels ORDER BY id'))
        self.digital_channel_rows=list(self.con.execute('SELECT id,name,frequency,tg,cc,call_group,operation,station_name,digital_id,contact FROM digital_channels ORDER BY id'))
        self.channel_combo['values']=[self.format_channel(x) for x in self.channel_rows]
        self.tone_rows=list(self.con.execute('SELECT id,name,code FROM tone_codes ORDER BY id'))
        self.tonecombo['values']=[self.format_tone_code(x) for x in self.tone_rows]
        self.type_rows_analog=list(self.con.execute('SELECT id,name FROM operation_types_analog ORDER BY id'))
        self.type_rows_digital=list(self.con.execute('SELECT id,name FROM operation_types_digital ORDER BY id'))
        self.quality_rows=list(self.con.execute('SELECT id,name FROM quality_values ORDER BY id'))
        self.qualitycombo['values']=[x['name'] for x in self.quality_rows]
        self.power_rows=list(self.con.execute('SELECT id,name FROM power_values ORDER BY id'))
        self.powercombo['values']=[x['name'] for x in self.power_rows]
        self.modulation_rows_analog=list(self.con.execute('SELECT id,name FROM modulation_modes_analog ORDER BY id'))
        self.modulation_rows_digital=list(self.con.execute('SELECT id,name FROM modulation_modes_digital ORDER BY id'))
        self.mode_changed(refresh_only=True)
    # Vrátí text digitálního kanálu pro zobrazení v seznamu.
    def format_digital_channel(self, row):


        return row['name'] or ''

    # Vrátí seznam typů spojení podle aktuálního režimu.
    def mode_specific_type_rows(self):
        return self.type_rows_digital if self.record_mode.get().strip() == 'Digitální' else self.type_rows_analog

    # Vrátí seznam modulací podle aktuálního režimu.
    def mode_specific_modulation_rows(self):
        return self.modulation_rows_digital if self.record_mode.get().strip() == 'Digitální' else self.modulation_rows_analog

    # Obnoví nabídku typů spojení a modulací.
    def refresh_type_and_modulation_values(self, keep_current=True):
        current_type = self.typ.get().strip()
        current_mod = self.modulation.get().strip()

        type_values = [r['name'] for r in self.mode_specific_type_rows()]
        mod_values = [r['name'] for r in self.mode_specific_modulation_rows()]

        self.typcombo['values'] = type_values
        self.modcombo['values'] = mod_values

        if not keep_current or current_type not in type_values:
            self.typ.set(type_values[0] if type_values else '')
        else:
            self.typ.set(current_type)

        if not keep_current or current_mod not in mod_values:
            self.modulation.set(mod_values[0] if mod_values else '')
        else:
            self.modulation.set(current_mod)

    # Zareaguje na přepnutí analogového/digitálního režimu.
    def mode_changed(self, refresh_only=False):
        mode = self.record_mode.get().strip() or 'Analogový'
        self.refresh_type_and_modulation_values(keep_current=refresh_only)

        if mode == 'Digitální':
            self.channel_label.configure(text='Digitální kanál:')
            self.channel_combo['values']=[self.format_digital_channel(x) for x in getattr(self, 'digital_channel_rows', [])]
            if not refresh_only and getattr(self, 'digital_channel_rows', None):
                self.set_digital_channel_by_id(self.digital_channel_rows[0]['id'])
        else:
            self.channel_label.configure(text='Analogový kanál:')
            self.channel_combo['values']=[self.format_channel(x) for x in getattr(self, 'channel_rows', [])]
            if not refresh_only and getattr(self, 'channel_rows', None):
                self.set_channel_by_id(self.channel_rows[0]['id'])

        self.update_record_layout()

    # Vrátí text CTCSS/DCS kódu pro zobrazení v seznamu.
    def format_tone_code(self, row):
        if not row['code']:
            return row['name']
        return f"{row['name']} / {row['code']}"

    # Vrátí skutečnou hodnotu vybraného CTCSS/DCS kódu.
    def selected_tone_code_value(self):
        txt = self.tone.get().strip()
        if not txt or txt == 'Bez kódu':
            return ''
        for row in getattr(self, 'tone_rows', []):
            if self.format_tone_code(row) == txt:
                return row['code']
            if row['code'] and row['code'] == txt:
                return row['code']
            if row['name'] == txt:
                return row['code']
        return txt

    # Nastaví CTCSS/DCS podle uložené hodnoty.
    def set_tone_by_value(self, value):
        value = (value or '').strip()
        if not value:
            self.tone.set('Bez kódu')
            return
        for row in getattr(self, 'tone_rows', []):
            if row['code'] == value or row['name'] == value or self.format_tone_code(row) == value:
                self.tone.set(self.format_tone_code(row))
                return
        self.tone.set(value)

    # Vrátí text analogového kanálu pro zobrazení v seznamu.
    def format_channel(self, row):


        return f"{row['name']} / {row['frequency']} MHz"
    # Najde databázový řádek vybraného kanálu.
    def selected_channel_row(self):
        txt=self.channel.get().strip()
        if not txt:
            return None
        if self.record_mode.get().strip() == 'Digitální':
            for row in getattr(self, 'digital_channel_rows', []):
                if self.format_digital_channel(row) == txt or row['name'] == txt:
                    return row
            return None


        for row in self.channel_rows:
            if self.format_channel(row) == txt:
                return row

        try:
            cid=int(txt.split(':',1)[0])
            for row in self.channel_rows:
                if row['id'] == cid:
                    return row
        except Exception:
            pass

        return None

    # Nastaví digitální kanál podle ID.
    def set_digital_channel_by_id(self, cid):
        for row in getattr(self, 'digital_channel_rows', []):
            if row['id'] == cid:
                self.channel.set(self.format_digital_channel(row))
                self.freq.set(row['frequency'] or '')
                self.tg.set(row['tg'] or '')
                self.cc.set(row['cc'] or '')
                self.call_group.set(row['call_group'] or '')
                if row['operation']:
                    self.typ.set(row['operation'])
                if 'digital_id' in row.keys():
                    self.digital_id.set(row['digital_id'] or '')
                if 'contact' in row.keys():
                    self.contact.set(row['contact'] or '')
                return
    # Nastaví analogový kanál podle ID.
    def set_channel_by_id(self, cid):
        for row in self.channel_rows:
            if row['id'] == cid:
                self.channel.set(self.format_channel(row)); self.update_freq(); return
        if self.channel_rows:
            self.channel.set(self.format_channel(self.channel_rows[0])); self.update_freq()
    # Nastaví výchozí hodnoty pro nový záznam.
    def defaults(self):
        self.set_now(); self.use_home()
        if self.record_mode.get().strip() == 'Digitální' and getattr(self, 'digital_channel_rows', None) and not self.channel.get(): self.set_digital_channel_by_id(self.digital_channel_rows[0]['id'])
        elif self.channel_rows and not self.channel.get(): self.set_channel_by_id(self.channel_rows[0]['id'])
        if getattr(self, 'tone_rows', None) and not self.tone.get(): self.set_tone_by_value('')
        self.refresh_type_and_modulation_values(keep_current=True)
        if getattr(self, 'quality_rows', None) and not self.quality.get():
            self.quality.set(self.quality_rows[0]['name'])
        if getattr(self, 'power_rows', None) and not self.power.get():
            self.power.set(self.power_rows[0]['name'])
        self.update_freq()
    # Nastaví aktuální datum a čas.
    def set_now(self): self.dt.set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # Použije domovský lokátor z nastavení uživatele.
    def use_home(self): self.my_loc.set(norm_loc(self.app.getset('my_locator',''))); self.recalc()
    # Aktualizuje frekvenci podle vybraného kanálu.
    def update_freq(self):
        row=self.selected_channel_row()
        if not row:
            self.freq.set('')
            return
        self.freq.set(row['frequency'] if row else '')
        if self.record_mode.get().strip() == 'Digitální':
            self.tg.set(row['tg'] or self.tg.get())
            self.cc.set(row['cc'] or self.cc.get())
            self.call_group.set(row['call_group'] or self.call_group.get())
            if row['operation']:
                self.typ.set(row['operation'])
            if 'digital_id' in row.keys():
                self.digital_id.set(row['digital_id'] or self.digital_id.get())
            if 'contact' in row.keys():
                self.contact.set(row['contact'] or self.contact.get())
    # Přepočítá vzdálenost, azimut a směr podle lokátorů.
    def recalc(self):
        ml,ol=norm_loc(self.my_loc.get()),norm_loc(self.loc.get()); self.my_loc.set(ml); self.loc.set(ol)
        if not ml or not ol: self.dist.set(''); self.bearing.set(''); self.direction.set(''); return
        try:
            d,b=distance_bearing(ml,ol); self.dist.set(f'{d:.1f}'); self.bearing.set(f'{b:.0f}'); self.direction.set(bearing_dir(b))
        except ValueError: self.dist.set(''); self.bearing.set(''); self.direction.set('')
    # Otevře mapu spojení z rozpracovaného záznamu.
    def open_map(self):


        my_locator = norm_loc(self.my_loc.get())
        other_locator = norm_loc(self.loc.get())

        if not my_locator or not other_locator:
            messagebox.showwarning('Mapa', 'Zadej můj lokátor i lokátor protistanice.')
            return

        try:

            d, b = distance_bearing(my_locator, other_locator)
            self.dist.set(f'{d:.1f}')
            self.bearing.set(f'{b:.0f}')
            self.direction.set(bearing_dir(b))
        except Exception as e:
            messagebox.showerror('Mapa', str(e))
            return


        row = {
            'my_locator': my_locator,
            'locator': other_locator,
            'my_call': norm_call(self.app.getset('my_call','')),
            'other_call': norm_call(self.other_call.get()),
            'distance_km': self.dist.get().strip(),
            'bearing_deg': self.bearing.get().replace('°','').strip(),
            'direction': self.direction.get().strip(),
        }

        LocatorMapWindow(self.win, row)
    # Načte data do okna nebo tabulky.
    def load(self,rid):
        r=self.app.get_record(rid)
        if not r: self.win.destroy(); return
        self.record_mode.set(r['mode'] or 'Analogový'); self.mode_changed(refresh_only=True); self.dt.set(r['dt'] or '')
        if self.record_mode.get() == 'Digitální':
            self.channel.set(r['channel_name'] or '')
        else:
            self.set_channel_by_id(int(r['channel'] or 1))
        self.freq.set(r['frequency'] or ''); self.set_tone_by_value(r['tone'] or ''); self.other_call.set(r['other_call'] or ''); self.my_loc.set(r['my_locator'] or ''); self.loc.set(r['locator'] or ''); self.dist.set(r['distance_km'] or ''); self.bearing.set(r['bearing_deg'] or ''); self.direction.set(r['direction'] or ''); self.typ.set(r['operation_type'] or 'spojeni'); self.signal.set(r['signal'] or '3 - pouzitelny'); self.quality.set(r['quality'] or 'dobra'); self.power.set(r['power'] or ''); self.modulation.set(r['modulation'] or ('DMR' if self.record_mode.get() == 'Digitální' else 'FM')); self.tg.set(r['tg'] or ''); self.cc.set(r['cc'] or ''); self.call_group.set(r['call_group'] or ''); self.digital_id.set(r['digital_id'] or ''); self.contact.set(r['contact'] or ''); self.device.set(r['device'] or ''); self.antenna.set(r['antenna'] or ''); self.note.insert('1.0',r['note'] or '')
    # Zkontroluje formulář a připraví data pro uložení.
    def data(self):
        try: datetime.strptime(self.dt.get().strip(),'%Y-%m-%d %H:%M:%S')
        except ValueError: messagebox.showerror('Chyba','Datum/čas musí být YYYY-MM-DD HH:MM:SS'); return None
        row=self.selected_channel_row()
        mode=self.record_mode.get().strip() or 'Analogový'
        if not row:
            messagebox.showerror('Chyba','Vyber kanál ze seznamu.'); return None
        if mode == 'Digitální':
            ch=0
            channel_name=row['name']
            self.freq.set(row['frequency'])
            self.tone.set('')
        else:
            ch=int(row['id']); channel_name=row['name']; self.freq.set(row['frequency'])
        for title,loc in [('Můj lokátor',self.my_loc.get()),('Lokátor protistanice',self.loc.get())]:
            if norm_loc(loc):
                try: locator_to_latlon(loc)
                except ValueError as e: messagebox.showerror(title,str(e)); return None
        self.update_freq(); self.recalc()
        return {'dt':self.dt.get().strip(),'channel':ch,'channel_name':channel_name,'frequency':self.freq.get(),'tone':('' if mode == 'Digitální' else self.selected_tone_code_value()),'my_call':norm_call(self.app.getset('my_call','')),'other_call':norm_call(self.other_call.get()),'my_locator':norm_loc(self.my_loc.get()),'locator':norm_loc(self.loc.get()),'distance_km':self.dist.get().strip(),'bearing_deg':self.bearing.get().replace('°','').strip(),'direction':self.direction.get().strip(),'operation_type':self.typ.get().strip(),'signal':self.signal.get().strip(),'quality':self.quality.get().strip(),'power':self.power.get().strip(),'modulation':self.modulation.get().strip(),'mode':mode,'tg':self.tg.get().strip(),'cc':self.cc.get().strip(),'call_group':self.call_group.get().strip(),'digital_id':self.digital_id.get().strip(),'contact':self.contact.get().strip(),'device':self.device.get().strip(),'antenna':self.antenna.get().strip(),'note':self.note.get('1.0','end').strip()}
    # Uloží nový nebo upravený záznam do databáze.
    def save(self):
        d=self.data();
        if not d: return
        if self.rid is None:
            self.con.execute('''INSERT INTO logs(dt,channel,channel_name,frequency,tone,my_call,other_call,my_locator,locator,distance_km,bearing_deg,direction,operation_type,signal,quality,power,modulation,mode,tg,cc,call_group,digital_id,contact,device,antenna,note) VALUES(:dt,:channel,:channel_name,:frequency,:tone,:my_call,:other_call,:my_locator,:locator,:distance_km,:bearing_deg,:direction,:operation_type,:signal,:quality,:power,:modulation,:mode,:tg,:cc,:call_group,:digital_id,:contact,:device,:antenna,:note)''',d)
        else:
            d['id']=self.rid; self.con.execute('''UPDATE logs SET dt=:dt,channel=:channel,channel_name=:channel_name,frequency=:frequency,tone=:tone,my_call=:my_call,other_call=:other_call,my_locator=:my_locator,locator=:locator,distance_km=:distance_km,bearing_deg=:bearing_deg,direction=:direction,operation_type=:operation_type,signal=:signal,quality=:quality,power=:power,modulation=:modulation,mode=:mode,tg=:tg,cc=:cc,call_group=:call_group,digital_id=:digital_id,contact=:contact,device=:device,antenna=:antenna,note=:note WHERE id=:id''',d)
        self.con.commit(); self.app.load_rows(); self.close_window()


# Okno s přehledným detailem uloženého záznamu.
class DetailWindow:
    # Inicializace okna nebo části aplikace.
    def __init__(self,app,rid):
        self.app=app; self.r=app.get_record(rid)
        if not self.r: return
        self.win=tk.Toplevel(app.root)
        self.win.configure(bg=THEME['bg'])
        self.win.title('Detail záznamu')
        self.win.geometry('760x620')
        self.win.minsize(560,420)
        self.win.transient(app.root)
        self.ui()

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):
        shell=ttk.Frame(self.win)
        shell.pack(fill='both',expand=True)

        self.canvas=tk.Canvas(shell,bg=THEME['bg'],highlightthickness=0)
        self.canvas.pack(side='left',fill='both',expand=True)

        scrollbar=ttk.Scrollbar(shell,orient='vertical',command=self.canvas.yview)
        scrollbar.pack(side='right',fill='y')
        self.canvas.configure(yscrollcommand=scrollbar.set)

        outer=ttk.Frame(self.canvas,padding=12)
        self.canvas_window=self.canvas.create_window((0,0),window=outer,anchor='nw')

        def update_scrollregion(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        def update_inner_width(event=None):
            self.canvas.itemconfigure(self.canvas_window,width=self.canvas.winfo_width())

        outer.bind('<Configure>',update_scrollregion)
        self.canvas.bind('<Configure>',update_inner_width)
        self.canvas.bind_all('<MouseWheel>',self._on_mousewheel)
        self.canvas.bind_all('<Button-4>',self._on_mousewheel)
        self.canvas.bind_all('<Button-5>',self._on_mousewheel)
        self.win.bind('<Destroy>',self._on_destroy)

        title=(self.r['other_call'] or self.r['locator'] or 'Protistanice').strip()
        ttk.Label(outer,text=f"Detail záznamu: {title}",font=('TkDefaultFont',13,'bold')).pack(anchor='w',pady=(0,8))

        main=ttk.Frame(outer)
        main.pack(fill='both',expand=True)

        left=ttk.LabelFrame(main,text='Základní údaje',padding=10)
        left.pack(side='left',fill='both',expand=True,padx=(0,6))

        right=ttk.LabelFrame(main,text='Technika a poznámka',padding=10)
        right.pack(side='left',fill='both',expand=True,padx=(6,0))

        fields_left=[
            ('Datum a čas',self.r['dt']),
            ('Režim',self.r['mode'] or 'Analogový'),
            ('Typ',self.r['operation_type']),
            ('Moje volačka',self.r['my_call']),
            ('Volačka protistanice',self.r['other_call']),
            ('Můj lokátor',self.r['my_locator']),
            ('Lokátor protistanice',self.r['locator']),
            ('Vzdálenost',f"{self.r['distance_km'] or ''} km"),
            ('Azimut',f"{self.r['bearing_deg'] or ''}°"),
            ('Směr',self.r['direction']),
            ('Kanál',f"{self.r['channel_name'] or ('PMR ' + str(self.r['channel']))} / {self.r['frequency']} MHz"),
        ]

        fields_right=[
            ('CTCSS/DCS',self.r['tone']),
            ('Signál',self.r['signal']),
            ('Kvalita',self.r['quality']),
            ('Výkon',self.r['power']),
            ('Modulace',self.r['modulation']),
            ('TG',self.r['tg']),
            ('CC',self.r['cc']),
            ('Volací skupina',self.r['call_group']),
            ('DMR ID',self.r['digital_id']),
            ('Kontakt',self.r['contact']),
            ('Zařízení',self.r['device']),
            ('Anténa',self.r['antenna']),
        ]

        for i,(n,v) in enumerate(fields_left):
            ttk.Label(left,text=n+':',font=('TkDefaultFont',9,'bold')).grid(row=i,column=0,sticky='nw',pady=3)
            ttk.Label(left,text=v or '-',wraplength=260).grid(row=i,column=1,sticky='nw',pady=3)

        for i,(n,v) in enumerate(fields_right):
            ttk.Label(right,text=n+':',font=('TkDefaultFont',9,'bold')).grid(row=i,column=0,sticky='nw',pady=3)
            ttk.Label(right,text=v or '-',wraplength=260).grid(row=i,column=1,sticky='nw',pady=3)

        ttk.Label(right,text='Poznámka:',font=('TkDefaultFont',9,'bold')).grid(row=len(fields_right),column=0,sticky='nw',pady=(10,3))
        t=tk.Text(right,height=10,width=34,wrap='word',bg=THEME['panel'],fg=THEME['panel_fg'],insertbackground=THEME['panel_fg'])
        t.grid(row=len(fields_right),column=1,sticky='nsew',pady=(10,3))
        t.insert('1.0',self.r['note'] or '')
        t.configure(state='disabled')

        right.columnconfigure(1,weight=1)
        right.rowconfigure(len(fields_right),weight=1)

        b=ttk.Frame(outer)
        b.pack(fill='x',pady=12)
        ttk.Button(b,text='Upravit',command=self.edit).pack(side='left',padx=4)
        ttk.Button(b,text='Vlastní mapa spojení',command=self.map_conn).pack(side='left',padx=4)
        ttk.Button(b,text='Mapa jen bodu protistanice',command=self.map_other).pack(side='left',padx=4)
        ttk.Button(b,text='Zavřít',command=self.win.destroy).pack(side='right',padx=4)

    # Zpracuje rolování v detailu záznamu.
    def _on_mousewheel(self,event):
        if not hasattr(self,'canvas') or not self.canvas.winfo_exists():
            return
        if event.num == 4:
            self.canvas.yview_scroll(-3,'units')
        elif event.num == 5:
            self.canvas.yview_scroll(3,'units')
        elif getattr(event,'delta',0):
            self.canvas.yview_scroll(int(-1*(event.delta/120)),'units')

    # Při zavření okna odpojí obsluhu kolečka myši.
    def _on_destroy(self,event):
        if event.widget is self.win and hasattr(self,'canvas'):
            try:
                self.canvas.unbind_all('<MouseWheel>')
                self.canvas.unbind_all('<Button-4>')
                self.canvas.unbind_all('<Button-5>')
            except Exception:
                pass

    # Otevře vybraný záznam k úpravě.
    def edit(self):
        RecordWindow(self.app,self.r['id'])
        self.win.destroy()

    # Otevře mapu celého spojení.
    def map_conn(self):
        try:
            LocatorMapWindow(self.app.root,self.r)
        except Exception as e:
            messagebox.showerror('Mapa',str(e))

    # Otevře mapu pouze bodu protistanice.
    def map_other(self):
        try:
            LocatorMapWindow(self.app.root,self.r,only_other=True)
        except Exception as e:
            messagebox.showerror('Mapa',str(e))


# Okno pro zobrazení spojení nebo protistanice na mapě.
class LocatorMapWindow:


    # Inicializace okna nebo části aplikace.
    def __init__(self,parent,row,only_other=False):
        self.row=row
        self.only_other=only_other
        self.win=tk.Toplevel(parent)
        self.win.configure(bg=THEME['bg'])
        self.win.title('Mapa spojení')
        self.win.geometry('900x680')
        self.win.transient(parent)

        self.my_point, self.other_point = self.get_points()

        toolbar=ttk.Frame(self.win,padding=(10,8))
        toolbar.pack(fill='x')

        ttk.Button(toolbar,text='Centrovat na spojení',command=self.center_on_connection).pack(side='left',padx=3)
        ttk.Button(toolbar,text='Zavřít',command=self.win.destroy).pack(side='right',padx=3)

        info_top=ttk.Frame(self.win,padding=(10,0))
        info_top.pack(fill='x')

        self.connection_info_var=tk.StringVar(value=self.connection_info_text())
        ttk.Label(info_top,textvariable=self.connection_info_var,font=('TkDefaultFont',10,'bold')).pack(anchor='w',pady=(0,6))

        info=ttk.Frame(self.win,padding=(10,4))
        info.pack(side='bottom',fill='x')

        self.info_var=tk.StringVar()
        ttk.Label(info,textvariable=self.info_var).pack(side='left')

        self.zoom=12

        if tkintermapview is not None:
            self.create_tkintermapview()
        else:
            self.create_fallback_canvas()

    # Bezpečně přečte hodnotu ze záznamu.
    def row_get(self, key, default=''):
        try:
            return self.row[key]
        except Exception:
            return default

    # Sestaví stručný text o spojení pro mapové okno.
    def connection_info_text(self):
        my_call=self.row_get('my_call','') or ''
        other_call=self.row_get('other_call','') or ''
        my_loc=self.row_get('my_locator','') or ''
        other_loc=self.row_get('locator','') or ''
        dist=self.row_get('distance_km','') or '?'
        bearing=self.row_get('bearing_deg','') or '?'
        direction=self.row_get('direction','') or ''

        left=f"{my_call} {my_loc}".strip() or "JA"
        right=f"{other_call} {other_loc}".strip() or "PROTISTANICE"

        return f"{left}  →  {right}     Vzdálenost: {dist} km     Azimut: {bearing}°     Směr: {direction}"

    # Převede lokátory na souřadnice pro mapu.
    def get_points(self):
        my_loc=norm_loc(self.row_get('my_locator','') or '')
        other_loc=norm_loc(self.row_get('locator','') or '')

        if self.only_other:
            if not other_loc:
                raise ValueError('Lokátor protistanice není vyplněn.')
            lat2,lon2=locator_to_latlon(other_loc)
            return None,(lat2,lon2)

        if not my_loc or not other_loc:
            raise ValueError('Pro mapu spojení musí být vyplněn můj lokátor i lokátor protistanice.')

        lat1,lon1=locator_to_latlon(my_loc)
        lat2,lon2=locator_to_latlon(other_loc)
        return (lat1,lon1),(lat2,lon2)

    # Odhadne vhodné přiblížení mapy podle vzdálenosti.
    def estimate_zoom(self):
        if self.my_point is None:
            return 12

        try:
            dist=float(self.row_get('distance_km','') or 0)
        except Exception:
            dist=0

        if dist <= 3:
            return 14
        if dist <= 8:
            return 13
        if dist <= 20:
            return 12
        if dist <= 60:
            return 10
        if dist <= 150:
            return 8
        if dist <= 350:
            return 7
        return 6

    # Vytvoří plnohodnotnou mapu pomocí knihovny tkintermapview.
    def create_tkintermapview(self):
        self.map_widget = tkintermapview.TkinterMapView(self.win, width=860, height=540, corner_radius=0)
        self.map_widget.pack(fill='both',expand=True,padx=10,pady=(0,6))

        try:
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png")
        except Exception:
            pass

        self.center_on_connection(initial=True)
        self.info_var.set('Mapa je otevřena uvnitř programu. Lze posouvat myší a zoomovat kolečkem.')

    # Vytvoří nouzové zobrazení mapy bez mapového podkladu.
    def create_fallback_canvas(self):
        self.canvas=tk.Canvas(self.win,width=860,height=540,bg='white',highlightthickness=1,highlightbackground='#999')
        self.canvas.pack(fill='both',expand=True,padx=10,pady=(0,6))
        self.win.bind('<Configure>',lambda e:self.draw_fallback())
        self.center_on_connection(initial=True)
        self.info_var.set('Knihovna tkintermapview neni nainstalovana. Zobrazuji nouzovou mapu bez podkladu.')

    # Vycentruje mapu na spojení nebo protistanici.
    def center_on_connection(self,initial=False):
        self.zoom=self.estimate_zoom()

        if tkintermapview is not None and hasattr(self,'map_widget'):
            if self.my_point is None:
                lat,lon=self.other_point
                self.map_widget.set_position(lat,lon)
            else:
                lat=(self.my_point[0]+self.other_point[0])/2
                lon=(self.my_point[1]+self.other_point[1])/2
                self.map_widget.set_position(lat,lon)

            self.map_widget.set_zoom(self.zoom)
            self.draw_tkintermapview_items()
        else:
            self.draw_fallback()

        self.connection_info_var.set(self.connection_info_text())

    # Vykreslí značky a trasu do mapy tkintermapview.
    def draw_tkintermapview_items(self):
        try:
            self.map_widget.delete_all_marker()
            self.map_widget.delete_all_path()
        except Exception:
            pass

        other_label=f"PS: {self.row_get('other_call','') or ''} {self.row_get('locator','') or ''}".strip()

        if self.my_point is not None:
            my_label=f"JA: {self.row_get('my_call','') or ''} {self.row_get('my_locator','') or ''}".strip()
            self.map_widget.set_marker(self.my_point[0], self.my_point[1], text=my_label)
            self.map_widget.set_path([
                (self.my_point[0], self.my_point[1]),
                (self.other_point[0], self.other_point[1])
            ])

        self.map_widget.set_marker(self.other_point[0], self.other_point[1], text=other_label)

    # Vykreslí jednoduchou náhradní mapu do Canvasu.
    def draw_fallback(self):
        if not hasattr(self,'canvas'):
            return

        self.canvas.delete('all')

        w=max(self.canvas.winfo_width(),300)
        h=max(self.canvas.winfo_height(),250)
        margin=60

        points=[p for p in (self.my_point,self.other_point) if p is not None]
        lats=[p[0] for p in points]
        lons=[p[1] for p in points]

        min_lat,max_lat=min(lats),max(lats)
        min_lon,max_lon=min(lons),max(lons)

        if abs(max_lat-min_lat)<0.01:
            min_lat-=0.01; max_lat+=0.01
        if abs(max_lon-min_lon)<0.01:
            min_lon-=0.01; max_lon+=0.01

        lat_pad=(max_lat-min_lat)*0.35
        lon_pad=(max_lon-min_lon)*0.35
        min_lat-=lat_pad; max_lat+=lat_pad
        min_lon-=lon_pad; max_lon+=lon_pad

        def to_xy(lat,lon):
            x=margin+(lon-min_lon)/(max_lon-min_lon)*(w-2*margin)
            y=h-margin-(lat-min_lat)/(max_lat-min_lat)*(h-2*margin)
            return x,y

        for i in range(6):
            x=margin+i*(w-2*margin)/5
            y=margin+i*(h-2*margin)/5
            self.canvas.create_line(x,margin,x,h-margin,fill='#e5e5e5')
            self.canvas.create_line(margin,y,w-margin,y,fill='#e5e5e5')

        self.canvas.create_rectangle(margin,margin,w-margin,h-margin,outline='#999')

        self.canvas.create_text(w-35,30,text='S',font=('TkDefaultFont',14,'bold'))
        self.canvas.create_line(w-35,50,w-35,90,arrow='first')

        if self.my_point is not None:
            x1,y1=to_xy(self.my_point[0],self.my_point[1])
            self.canvas.create_oval(x1-7,y1-7,x1+7,y1+7,fill='#2b7cff',outline='')
            self.canvas.create_text(
                x1+10,y1-12,anchor='w',
                text=f"JA: {self.row_get('my_call','')} {self.row_get('my_locator','')}",
                fill='#1f4faf'
            )

        x2,y2=to_xy(self.other_point[0],self.other_point[1])
        self.canvas.create_oval(x2-7,y2-7,x2+7,y2+7,fill='#e53935',outline='')
        self.canvas.create_text(
            x2+10,y2+12,anchor='w',
            text=f"PS: {self.row_get('other_call','')} {self.row_get('locator','')}",
            fill='#9f1f1f'
        )

        if self.my_point is not None:
            self.canvas.create_line(x1,y1,x2,y2,fill='#111',width=2)
            midx=(x1+x2)/2
            midy=(y1+y2)/2
            label=f"{self.row_get('distance_km','?') or '?'} km / {self.row_get('bearing_deg','?') or '?'}° {self.row_get('direction','') or ''}"
            self.canvas.create_rectangle(midx-95,midy-14,midx+95,midy+14,fill='white',outline='#aaa')
            self.canvas.create_text(midx,midy,text=label)

        self.connection_info_var.set(self.connection_info_text())


# Okno pro nastavení vlastní volačky a domovského lokátoru.
class UserSettings:
    # Inicializace okna nebo části aplikace.
    def __init__(self,app):
        self.app=app; self.win=tk.Toplevel(app.root); self.win.title('Nastavení uživatele'); self.win.geometry('420x220'); self.win.transient(app.root); self.win.grab_set()
        f=ttk.Frame(self.win,padding=12); f.pack(fill='both',expand=True)
        self.call=tk.StringVar(value=app.getset('my_call','')); self.loc=tk.StringVar(value=app.getset('my_locator',''))
        ttk.Label(f,text='Moje volačka:').grid(row=0,column=0,sticky='w',pady=6); ttk.Entry(f,textvariable=self.call,width=25).grid(row=0,column=1,sticky='w')
        ttk.Label(f,text='Domovský lokátor:').grid(row=1,column=0,sticky='w',pady=6); ttk.Entry(f,textvariable=self.loc,width=25).grid(row=1,column=1,sticky='w')
        b=ttk.Frame(f); b.grid(row=2,column=0,columnspan=2,sticky='e',pady=14);

        ttk.Button(
            b,
            text='Uložit',
            style='Accent.TButton',
            command=self.save
        ).pack(side='left', padx=4);

        ttk.Button(b,text='Zavřít',command=self.win.destroy).pack(side='left',padx=4)
    # Uloží nový nebo upravený záznam do databáze.
    def save(self):
        call=norm_call(self.call.get()); loc=norm_loc(self.loc.get())
        if loc:
            try: locator_to_latlon(loc)
            except ValueError as e: messagebox.showerror('Lokátor',str(e)); return
        self.app.setset('my_call',call); self.app.setset('my_locator',loc); self.app.load_user_panel(); self.win.destroy()


# Okno pro správu seznamu zařízení a antén.
class EquipmentSettings:
    # Inicializace okna nebo části aplikace.
    def __init__(self, app):
        self.app = app
        self.con = app.con
        self.win = tk.Toplevel(app.root)
        self.win.title('Nastavení zařízeni')
        self.win.geometry('900x390')
        self.win.minsize(900, 390)
        self.win.transient(app.root)
        self.win.grab_set()
        self.ui()
        self.load()

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):

        self.win.geometry('900x390')
        self.win.minsize(900, 390)
        main = ttk.Frame(self.win)
        main.place(x=0, y=0, relwidth=1, relheight=1)

        left = ttk.Frame(main, style='Card.TFrame')
        left.place(x=16, y=32, width=340, height=300)
        right = ttk.Frame(main, style='Card.TFrame')
        right.place(x=380, y=32, width=340, height=300)

        ttk.Label(main, text='Vysílačky / radiostanice', font=('Ubuntu', 10, 'bold')).place(x=16, y=8, width=260, height=22)
        ttk.Label(main, text='Antény', font=('Ubuntu', 10, 'bold')).place(x=380, y=8, width=260, height=22)

        self.dev_var=tk.StringVar(); self.ant_var=tk.StringVar()

        self.dev_list=tk.Listbox(left,bg=THEME['panel'],fg=THEME['panel_fg'],selectbackground=THEME['select'],selectforeground=THEME['select_fg'],relief='solid',bd=1,activestyle='none')
        self.dev_list.place(x=12,y=12,width=316,height=172)
        ttk.Entry(left,textvariable=self.dev_var).place(x=12,y=194,width=316,height=32)
        ttk.Button(left,text='✚  Přidat',command=lambda:self.add('device')).place(x=58,y=246,width=120,height=36)
        ttk.Button(left,text='🗑  Smazat',command=lambda:self.delete('device')).place(x=190,y=246,width=120,height=36)

        self.ant_list=tk.Listbox(right,bg=THEME['panel'],fg=THEME['panel_fg'],selectbackground=THEME['select'],selectforeground=THEME['select_fg'],relief='solid',bd=1,activestyle='none')
        self.ant_list.place(x=12,y=12,width=316,height=172)
        ttk.Entry(right,textvariable=self.ant_var).place(x=12,y=194,width=316,height=32)
        ttk.Button(right,text='✚  Přidat',command=lambda:self.add('antenna')).place(x=58,y=246,width=120,height=36)
        ttk.Button(right,text='🗑  Smazat',command=lambda:self.delete('antenna')).place(x=190,y=246,width=120,height=36)

        ttk.Button(main,text='✖  Zavřít',command=self.win.destroy).place(x=760,y=278,width=120,height=36)

    # Načte data do okna nebo tabulky.
    def load(self):
        self.dev_list.delete(0, 'end')
        self.ant_list.delete(0, 'end')
        for x in self.con.execute("SELECT name FROM equipment WHERE kind='device' ORDER BY name"):
            self.dev_list.insert('end', x['name'])
        for x in self.con.execute("SELECT name FROM equipment WHERE kind='antenna' ORDER BY name"):
            self.ant_list.insert('end', x['name'])

    # Přidá novou položku do nastavení.
    def add(self, kind):
        var = self.dev_var if kind == 'device' else self.ant_var
        name = var.get().strip()
        if name:
            self.con.execute('INSERT OR IGNORE INTO equipment(kind,name) VALUES(?,?)', (kind, name))
            self.con.commit()
            var.set('')
            self.load()

    # Smaže vybraný záznam po potvrzení.
    def delete(self, kind):
        lb = self.dev_list if kind == 'device' else self.ant_list
        sel = lb.curselection()
        if not sel:
            return
        name = lb.get(sel[0])
        if messagebox.askyesno('Smazat', f'Smazat položku?\n\n{name}'):
            self.con.execute('DELETE FROM equipment WHERE kind=? AND name=?', (kind, name))
            self.con.commit()
            self.load()


# Univerzální okno pro správu analogových a digitálních seznamů.
class DualSimpleListSettings:


    # Inicializace okna nebo části aplikace.
    def __init__(self, app, title, item_label, analog_table, analog_defaults, digital_table, digital_defaults):
        self.app = app
        self.con = app.con
        self.title = title
        self.item_label = item_label
        self.analog_table = analog_table
        self.digital_table = digital_table
        self.analog_defaults = analog_defaults
        self.digital_defaults = digital_defaults
        self.editing = None

        self.win = tk.Toplevel(app.root)
        self.win.title(title)
        self.win.geometry('900x500')
        self.win.minsize(900, 500)
        self.win.transient(app.root)
        self.win.grab_set()
        self.ui()
        self.load()

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):
        main = ttk.Frame(self.win)
        main.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Label(main, text=f'{self.item_label}. Dvojklikem upravíš buňku.', font=('Ubuntu', 10, 'bold')).place(x=14, y=12, width=860, height=24)

        ttk.Label(main, text='Analogový režim', font=('Ubuntu', 10, 'bold')).place(x=14, y=44, width=300, height=22)
        ttk.Label(main, text='Digitální režim', font=('Ubuntu', 10, 'bold')).place(x=460, y=44, width=300, height=22)

        self.left_card = ttk.Frame(main, style='Card.TFrame')
        self.left_card.place(x=14, y=68, width=420, relheight=1.0, height=-150)
        self.right_card = ttk.Frame(main, style='Card.TFrame')
        self.right_card.place(x=460, y=68, width=420, relheight=1.0, height=-150)

        self.analog_tree = self.create_tree(self.left_card)
        self.digital_tree = self.create_tree(self.right_card)

        buttons = ttk.Frame(main)
        buttons.place(x=14, rely=1.0, y=-72, relwidth=1.0, width=-28, height=42)
        ttk.Button(buttons, text='✚  Přidat analog', command=lambda: self.add_row(self.analog_tree)).pack(side='left', padx=(0, 6))
        ttk.Button(buttons, text='✚  Přidat digitál', command=lambda: self.add_row(self.digital_tree)).pack(side='left', padx=6)
        ttk.Button(buttons, text='🗑  Smazat', command=self.delete_selected).pack(side='left', padx=6)
        ttk.Button(buttons, text='💾  Uložit změny', command=self.save_changes, style='Accent.TButton').pack(side='left', padx=6)
        ttk.Button(buttons, text='Obnovit výchozí', command=self.reset_defaults).pack(side='left', padx=6)
        ttk.Button(buttons, text='✖  Zavřít', command=self.win.destroy).pack(side='right', padx=(6, 0))

        self.status_var = tk.StringVar(value='Připraveno')
        ttk.Label(main, textvariable=self.status_var, anchor='w', style='Subtitle.TLabel').place(x=14, rely=1.0, y=-28, width=650, height=20)

    # Vytvoří jednoduchou editační tabulku.
    def create_tree(self, parent):
        tree = ttk.Treeview(parent, columns=('name',), show='headings', selectmode='browse')
        tree.place(x=10, y=10, relwidth=1.0, width=-28, relheight=1.0, height=-20)
        tree.heading('name', text='Název')
        tree.column('name', width=360, anchor='w')
        sb = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        sb.place(relx=1.0, x=-18, y=10, width=18, relheight=1.0, height=-20)
        tree.configure(yscrollcommand=sb.set)
        tree.bind('<Double-1>', lambda e, t=tree: self.start_cell_edit(t, e))
        tree.bind('<Return>', lambda e, t=tree: self.start_cell_edit(t, e))
        tree.bind('<Escape>', lambda e: self.cancel_cell_edit())
        return tree

    # Načte data do vybrané tabulky.
    def load_tree(self, tree, table):
        for item in tree.get_children():
            tree.delete(item)
        for row in self.con.execute(f'SELECT id, name FROM {table} ORDER BY id'):
            tree.insert('', 'end', iid=str(row['id']), values=(row['name'],))

    # Načte data do okna nebo tabulky.
    def load(self):
        self.cancel_cell_edit()
        self.load_tree(self.analog_tree, self.analog_table)
        self.load_tree(self.digital_tree, self.digital_table)
        self.status_var.set(f'Analog: {len(self.analog_tree.get_children())} | Digitál: {len(self.digital_tree.get_children())}')

    # Přidá nový řádek do editační tabulky.
    def add_row(self, tree):
        self.cancel_cell_edit()
        prefix = 'new_a_' if tree is self.analog_tree else 'new_d_'
        temp_id = prefix + str(len([i for i in tree.get_children() if str(i).startswith(prefix)]) + 1)
        while tree.exists(temp_id):
            temp_id += '_x'
        tree.insert('', 'end', iid=temp_id, values=('Nová položka',))
        tree.selection_set(temp_id)
        tree.see(temp_id)

    # Zjistí, ve které tabulce je vybraný řádek.
    def active_tree(self):
        if self.analog_tree.selection():
            return self.analog_tree
        if self.digital_tree.selection():
            return self.digital_tree
        return None

    # Smaže vybraný řádek z dvojitého seznamu.
    def delete_selected(self):
        self.cancel_cell_edit()
        tree = self.active_tree()
        if tree is None:
            messagebox.showwarning('Smazat řádek', 'Nejdříve vyber řádek.')
            return
        item = tree.selection()[0]
        label = (tree.item(item, 'values') or [''])[0]
        if not messagebox.askyesno('Smazat řádek', f'Opravdu smazat vybraný řádek?\n\n{label}'):
            return
        if not str(item).startswith('new_'):
            table = self.analog_table if tree is self.analog_tree else self.digital_table
            self.con.execute(f'DELETE FROM {table} WHERE id=?', (int(item),))
            self.con.commit()
        tree.delete(item)
        self.status_var.set('Řádek smazán.')

    # Spustí editaci buňky přímo v tabulce.
    def start_cell_edit(self, tree, event=None):
        self.cancel_cell_edit()
        if event is not None:
            if tree.identify('region', event.x, event.y) != 'cell':
                return
            item = tree.identify_row(event.y)
            column = tree.identify_column(event.x)
        else:
            selected = tree.selection()
            if not selected:
                return
            item = selected[0]
            column = '#1'
        if not item or column != '#1':
            return
        bbox = tree.bbox(item, column)
        if not bbox:
            return
        x, y, width, height = bbox
        old = (tree.item(item, 'values') or [''])[0]
        self.editing = (tree, item)
        self.edit_var = tk.StringVar(value=old)
        self.edit_entry = ttk.Entry(tree, textvariable=self.edit_var)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.focus_set()
        self.edit_entry.select_range(0, 'end')
        self.edit_entry.bind('<Return>', lambda e: self.finish_cell_edit())
        self.edit_entry.bind('<KP_Enter>', lambda e: self.finish_cell_edit())
        self.edit_entry.bind('<Escape>', lambda e: self.cancel_cell_edit())
        self.edit_entry.bind('<FocusOut>', lambda e: self.finish_cell_edit())

    # Dokončí editaci buňky a uloží hodnotu do tabulky.
    def finish_cell_edit(self):
        if not self.editing:
            return
        tree, item = self.editing
        value = self.edit_var.get().strip()
        tree.item(item, values=(value,))
        self.cancel_cell_edit(clear_only=True)

    # Zruší právě probíhající editaci buňky.
    def cancel_cell_edit(self, clear_only=False):
        if hasattr(self, 'edit_entry'):
            try: self.edit_entry.destroy()
            except Exception: pass
            del self.edit_entry
        if hasattr(self, 'edit_var'):
            del self.edit_var
        self.editing = None

    # Načte a zkontroluje hodnoty z editační tabulky.
    def values_from_tree(self, tree):
        values = []
        seen = set()
        for index, item in enumerate(tree.get_children(), start=1):
            value = (tree.item(item, 'values') or [''])[0].strip()
            if not value:
                messagebox.showerror('Chyba', f'Řádek {index}: název nesmí být prázdný.')
                return None
            key = value.lower()
            if key in seen:
                messagebox.showerror('Chyba', f'Řádek {index}: duplicitní položka {value}.')
                return None
            seen.add(key)
            values.append((item, value))
        return values

    # Uloží jednu editační tabulku do databáze.
    def save_one_table(self, tree, table):
        values = self.values_from_tree(tree)
        if values is None:
            return False
        for item, value in values:
            if str(item).startswith('new_'):
                self.con.execute(f'INSERT OR IGNORE INTO {table}(name) VALUES(?)', (value,))
            else:
                self.con.execute(f'UPDATE {table} SET name=? WHERE id=?', (value, int(item)))
        return True

    # Uloží změny z editačního okna.
    def save_changes(self):
        self.finish_cell_edit()
        try:
            if not self.save_one_table(self.analog_tree, self.analog_table):
                return
            if not self.save_one_table(self.digital_tree, self.digital_table):
                return
            self.con.commit()
            self.load()
            messagebox.showinfo('Hotovo', f'{self.title} bylo uloženo.')
        except sqlite3.Error as e:
            messagebox.showerror('Chyba databáze', str(e))

    # Doplní výchozí hodnoty do nastavení.
    def reset_defaults(self):
        self.cancel_cell_edit()
        if not messagebox.askyesno('Obnovit výchozí', 'Doplnit výchozí analogové i digitální položky?\n\nExistující položky zůstanou.'):
            return
        try:
            for (name,) in self.analog_defaults:
                self.con.execute(f'INSERT OR IGNORE INTO {self.analog_table}(name) VALUES(?)', (name,))
            for (name,) in self.digital_defaults:
                self.con.execute(f'INSERT OR IGNORE INTO {self.digital_table}(name) VALUES(?)', (name,))
            self.con.commit()
            self.load()
            self.status_var.set('Výchozí položky doplněny.')
        except sqlite3.Error as e:
            messagebox.showerror('Chyba', str(e))


# Univerzální okno pro správu jednoduchého seznamu hodnot.
class SimpleListSettings:


    # Inicializace okna nebo části aplikace.
    def __init__(self, app, title, table_name, item_label, defaults):
        self.app = app
        self.con = app.con
        self.title = title
        self.table_name = table_name
        self.item_label = item_label
        self.defaults = defaults

        self.win = tk.Toplevel(app.root)
        self.win.title(title)
        self.win.geometry("700x460")
        self.win.minsize(620, 460)
        self.win.transient(app.root)
        self.win.grab_set()

        self.editing_item = None
        self.sort_col = "id"
        self.sort_desc = False

        self.ui()
        self.load()

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):
        main = ttk.Frame(self.win)
        main.place(x=0, y=0, relwidth=1, relheight=1)

        ttk.Label(
            main,
            text=f"{self.item_label}. Kliknutím na záhlaví seřadíš sloupec. Dvojklikem upravíš buňku.",
            font=('Ubuntu', 10, 'bold')
        ).place(x=14, y=12, width=590, height=24)

        table_card = ttk.Frame(main, style='Card.TFrame')
        table_card.place(x=14, y=44, relwidth=1.0, width=-28, relheight=1.0, height=-142)

        self.tree = ttk.Treeview(table_card, columns=("name",), show="headings", selectmode="browse")
        self.tree.place(x=10, y=10, relwidth=1.0, width=-28, relheight=1.0, height=-20)

        self.tree.heading("name", text="Název", command=lambda: self.sort("name"))
        self.tree.column("name", width=520, anchor="w")

        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar.place(relx=1.0, x=-18, y=10, width=18, relheight=1.0, height=-20)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.start_cell_edit)
        self.tree.bind("<Return>", self.start_cell_edit)
        self.tree.bind("<Escape>", lambda e: self.cancel_cell_edit())

        buttons = ttk.Frame(main)
        buttons.place(x=14, rely=1.0, y=-72, relwidth=1.0, width=-28, height=42)

        ttk.Button(buttons, text="✚  Přidat řádek", command=self.add_row).pack(side="left", padx=(0, 6))
        ttk.Button(buttons, text="🗑  Smazat řádek", command=self.delete_selected_row).pack(side="left", padx=6)
        ttk.Button(buttons, text="💾  Uložit změny", command=self.save_changes, style='Accent.TButton').pack(side="left", padx=6)
        ttk.Button(buttons, text="Obnovit výchozí", command=self.reset_defaults).pack(side="left", padx=6)
        ttk.Button(buttons, text="✖  Zavřít", command=self.win.destroy).pack(side="right", padx=(6, 0))

        self.status_var = tk.StringVar(value="Připraveno")
        ttk.Label(main, textvariable=self.status_var, anchor="w", style='Subtitle.TLabel').place(x=14, rely=1.0, y=-28, width=500, height=20)

    # Vrátí SQL řazení pro aktuální tabulku.
    def order_sql(self):
        direction = "DESC" if self.sort_desc else "ASC"
        if self.sort_col == "name":
            return f"name COLLATE NOCASE {direction}, id ASC"
        return "id ASC"

    # Načte data do okna nebo tabulky.
    def load(self):
        self.cancel_cell_edit()
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = list(self.con.execute(f"SELECT id, name FROM {self.table_name} ORDER BY {self.order_sql()}"))
        for row in rows:
            self.tree.insert("", "end", iid=str(row["id"]), values=(row["name"],))

        self.status_var.set(f"Načteno položek: {len(rows)}")

    # Nastaví řazení podle vybraného sloupce.
    def sort(self, column):
        self.finish_cell_edit()
        if self.sort_col == column:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_col = column
            self.sort_desc = False
        self.load()

    # Přidá nový řádek do editační tabulky.
    def add_row(self):
        self.cancel_cell_edit()
        temp_id = "new_" + str(len([i for i in self.tree.get_children() if str(i).startswith("new_")]) + 1)
        counter = 1
        base = temp_id
        while self.tree.exists(temp_id):
            counter += 1
            temp_id = f"{base}_{counter}"

        self.tree.insert("", "end", iid=temp_id, values=("Nová položka",))
        self.tree.selection_set(temp_id)
        self.tree.see(temp_id)
        self.status_var.set("Přidán nový řádek. Hodnotu upravíš dvojklikem do buňky.")

    # Smaže vybraný řádek z editační tabulky.
    def delete_selected_row(self):
        self.cancel_cell_edit()
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Smazat řádek", "Nejdříve vyber řádek.")
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")
        label = values[0] if values else ""

        if not messagebox.askyesno("Smazat řádek", f"Opravdu smazat vybraný řádek?\n\n{label}"):
            return

        if not str(item_id).startswith("new_"):
            try:
                self.con.execute(f"DELETE FROM {self.table_name} WHERE id=?", (int(item_id),))
                self.con.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Chyba", str(e))
                return

        self.tree.delete(item_id)
        self.status_var.set("Řádek smazán.")

    # Spustí editaci buňky přímo v tabulce.
    def start_cell_edit(self, event=None):
        self.cancel_cell_edit()

        if event is not None:
            if self.tree.identify("region", event.x, event.y) != "cell":
                return
            item_id = self.tree.identify_row(event.y)
            column_id = self.tree.identify_column(event.x)
        else:
            selected = self.tree.selection()
            if not selected:
                return
            item_id = selected[0]
            column_id = "#1"

        if not item_id or column_id != "#1":
            return

        bbox = self.tree.bbox(item_id, column_id)
        if not bbox:
            return

        x, y, width, height = bbox
        values = list(self.tree.item(item_id, "values"))
        old_value = values[0] if values else ""

        self.editing_item = item_id
        self.edit_var = tk.StringVar(value=old_value)
        self.edit_entry = ttk.Entry(self.tree, textvariable=self.edit_var)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.focus_set()
        self.edit_entry.select_range(0, "end")

        self.edit_entry.bind("<Return>", lambda e: self.finish_cell_edit())
        self.edit_entry.bind("<KP_Enter>", lambda e: self.finish_cell_edit())
        self.edit_entry.bind("<Escape>", lambda e: self.cancel_cell_edit())
        self.edit_entry.bind("<FocusOut>", lambda e: self.finish_cell_edit())

    # Dokončí editaci buňky a uloží hodnotu do tabulky.
    def finish_cell_edit(self):
        if not self.editing_item:
            return

        item_id = self.editing_item
        new_value = self.edit_var.get().strip()
        self.tree.item(item_id, values=(new_value,))

        self.cancel_cell_edit(clear_only=True)
        self.status_var.set("Buňka upravena. Nezapomeň uložit změny.")

    # Zruší právě probíhající editaci buňky.
    def cancel_cell_edit(self, clear_only=False):
        if hasattr(self, "edit_entry"):
            try:
                self.edit_entry.destroy()
            except Exception:
                pass
        if hasattr(self, "edit_var"):
            del self.edit_var
        if hasattr(self, "edit_entry"):
            del self.edit_entry
        self.editing_item = None

    # Zkontroluje, zda název položky není prázdný.
    def validate_name(self, name, row_number):
        name = (name or "").strip()
        if not name:
            messagebox.showerror("Chyba", f"Řádek {row_number}: název nesmí být prázdný.")
            return None
        return name

    # Uloží změny z editačního okna.
    def save_changes(self):
        self.finish_cell_edit()
        seen = set()
        items = self.tree.get_children()

        try:
            for index, item_id in enumerate(items, start=1):
                values = list(self.tree.item(item_id, "values"))
                name = values[0] if values else ""
                name = self.validate_name(name, index)
                if not name:
                    return

                key = name.lower()
                if key in seen:
                    messagebox.showerror("Chyba", f"Řádek {index}: duplicitní položka '{name}'.")
                    return
                seen.add(key)

            for item_id in items:
                values = list(self.tree.item(item_id, "values"))
                name = values[0].strip() if values else ""
                if str(item_id).startswith("new_"):
                    self.con.execute(f"INSERT OR IGNORE INTO {self.table_name}(name) VALUES(?)", (name,))
                else:
                    self.con.execute(f"UPDATE {self.table_name} SET name=? WHERE id=?", (name, int(item_id)))

            self.con.commit()
            self.load()
            self.status_var.set("Změny uloženy.")
            messagebox.showinfo("Hotovo", f"{self.title} bylo uloženo.")

        except sqlite3.Error as e:
            messagebox.showerror("Chyba databáze", str(e))

    # Doplní výchozí hodnoty do nastavení.
    def reset_defaults(self):
        self.cancel_cell_edit()
        if not messagebox.askyesno(
            "Obnovit výchozí hodnoty",
            "Doplnit výchozí položky?\n\nExistující položky zůstanou."
        ):
            return

        try:
            for (name,) in self.defaults:
                self.con.execute(f"INSERT OR IGNORE INTO {self.table_name}(name) VALUES(?)", (name,))
            self.con.commit()
            self.load()
            self.status_var.set("Výchozí položky doplněny.")
        except sqlite3.Error as e:
            messagebox.showerror("Chyba", str(e))


# Okno pro správu analogových kanálů a CTCSS/DCS kódů.
class AnalogSettings:

    # Inicializace okna nebo části aplikace.
    def __init__(self, app):
        self.app = app
        self.con = app.con
        self.win = tk.Toplevel(app.root)
        self.win.title("Nastavení analogových kanálů")
        self.win.geometry("980x560")
        self.win.minsize(980, 560)
        self.win.transient(app.root)
        self.win.grab_set()
        self.editing = None
        self.ui()
        self.load_channels()
        self.load_tones()

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):
        main = ttk.Frame(self.win)
        main.place(x=0, y=0, relwidth=1, relheight=1)
        ttk.Label(main, text="Nastavení analogových kanálů", font=('Ubuntu', 14, 'bold')).place(x=14, y=10, width=500, height=28)
        ttk.Label(main, text="Dvojklikem upravíš buňku.").place(x=14, y=40, width=760, height=24)

        left_card = ttk.Frame(main, style='Card.TFrame')
        left_card.place(x=14, y=78, width=455, relheight=1.0, height=-150)
        right_card = ttk.Frame(main, style='Card.TFrame')
        right_card.place(x=490, y=78, width=476, relheight=1.0, height=-150)

        ttk.Label(left_card, text="Analogové kanály", style='CardTitle.TLabel').place(x=10, y=8, width=260, height=24)
        self.channel_tree = ttk.Treeview(left_card, columns=('name','frequency'), show='headings', selectmode='browse')
        self.channel_tree.place(x=10, y=38, relwidth=1.0, width=-28, relheight=1.0, height=-92)
        self.channel_tree.heading('name', text='Název')
        self.channel_tree.heading('frequency', text='Frekvence MHz')
        self.channel_tree.column('name', width=230, anchor='w')
        self.channel_tree.column('frequency', width=160, anchor='center')
        sb1 = ttk.Scrollbar(left_card, orient='vertical', command=self.channel_tree.yview)
        sb1.place(relx=1.0, x=-18, y=38, width=18, relheight=1.0, height=-92)
        self.channel_tree.configure(yscrollcommand=sb1.set)
        self.channel_tree.bind('<Double-1>', lambda e: self.start_edit(self.channel_tree, ('name','frequency'), e))


        ch_buttons = tk.Frame(left_card, bg=THEME['panel'], bd=0, highlightthickness=0)
        ch_buttons.place(x=10, rely=1.0, y=-46, relwidth=1.0, width=-20, height=40)
        ttk.Button(ch_buttons, text='✚ Přidat', command=self.add_channel).pack(side='left', padx=(0,8), pady=2)
        ttk.Button(ch_buttons, text='🗑 Smazat', command=self.delete_channel).pack(side='left', padx=8, pady=2)
        ttk.Button(ch_buttons, text='Obnovit PMR 1-16', command=self.reset_channels).pack(side='right', pady=2)

        ttk.Label(right_card, text="CTCSS/DCS kódy", style='CardTitle.TLabel').place(x=10, y=8, width=260, height=24)
        self.tone_tree = ttk.Treeview(right_card, columns=('name','code'), show='headings', selectmode='browse')
        self.tone_tree.place(x=10, y=38, relwidth=1.0, width=-28, relheight=1.0, height=-92)
        self.tone_tree.heading('name', text='Název')
        self.tone_tree.heading('code', text='Kód')
        self.tone_tree.column('name', width=250, anchor='w')
        self.tone_tree.column('code', width=140, anchor='center')
        sb2 = ttk.Scrollbar(right_card, orient='vertical', command=self.tone_tree.yview)
        sb2.place(relx=1.0, x=-18, y=38, width=18, relheight=1.0, height=-92)
        self.tone_tree.configure(yscrollcommand=sb2.set)
        self.tone_tree.bind('<Double-1>', lambda e: self.start_edit(self.tone_tree, ('name','code'), e))


        tone_buttons = tk.Frame(right_card, bg=THEME['panel'], bd=0, highlightthickness=0)
        tone_buttons.place(x=10, rely=1.0, y=-46, relwidth=1.0, width=-20, height=40)
        ttk.Button(tone_buttons, text='✚ Přidat', command=self.add_tone).pack(side='left', padx=(0,8), pady=2)
        ttk.Button(tone_buttons, text='🗑 Smazat', command=self.delete_tone).pack(side='left', padx=8, pady=2)
        ttk.Button(tone_buttons, text='Obnovit výchozí', command=self.reset_tones).pack(side='right', pady=2)

        bottom = ttk.Frame(main)
        bottom.place(x=14, rely=1.0, y=-70, relwidth=1.0, width=-28, height=42)

        ttk.Button(bottom, text='💾 Uložit změny', style='Accent.TButton', command=self.save_all).pack(side='left', padx=(0,8))
        ttk.Button(bottom, text='✖ Zavřít', command=self.win.destroy).pack(side='right')
        self.status_var = tk.StringVar(value='Připraveno')
        ttk.Label(main, textvariable=self.status_var, anchor='w', style='Subtitle.TLabel').place(x=14, rely=1.0, y=-24, width=700, height=20)

    def start_edit(self, tree, columns, event):
        self.finish_edit()
        if tree.identify('region', event.x, event.y) != 'cell':
            return
        item = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        if not item or not col:
            return
        idx = int(col[1:]) - 1
        bbox = tree.bbox(item, col)
        if not bbox:
            return
        x,y,w,h = bbox
        vals = list(tree.item(item, 'values'))
        self.editing = (tree, item, idx, columns)
        self.edit_var = tk.StringVar(value=vals[idx] if idx < len(vals) else '')
        self.edit_entry = ttk.Entry(tree, textvariable=self.edit_var)
        self.edit_entry.place(x=x, y=y, width=w, height=h)
        self.edit_entry.focus_set(); self.edit_entry.select_range(0,'end')
        self.edit_entry.bind('<Return>', lambda e: self.finish_edit())
        self.edit_entry.bind('<Escape>', lambda e: self.cancel_edit())
        self.edit_entry.bind('<FocusOut>', lambda e: self.finish_edit())

    def finish_edit(self):
        if not self.editing:
            return
        tree, item, idx, columns = self.editing
        vals = list(tree.item(item, 'values'))
        while len(vals) < len(columns): vals.append('')
        vals[idx] = self.edit_var.get().strip()
        tree.item(item, values=vals)
        self.cancel_edit(clear_only=True)
        self.status_var.set('Buňka upravena. Nezapomeň uložit změny.')

    def cancel_edit(self, clear_only=False):
        if hasattr(self, 'edit_entry'):
            try: self.edit_entry.destroy()
            except Exception: pass
            del self.edit_entry
        if hasattr(self, 'edit_var'):
            del self.edit_var
        self.editing = None

    # Načte analogové kanály do tabulky.
    def load_channels(self):
        self.channel_tree.delete(*self.channel_tree.get_children())
        for r in self.con.execute('SELECT id,name,frequency FROM channels ORDER BY id'):
            self.channel_tree.insert('', 'end', iid=str(r['id']), values=(r['name'], r['frequency']))

    # Načte CTCSS/DCS kódy do tabulky.
    def load_tones(self):
        self.tone_tree.delete(*self.tone_tree.get_children())
        for r in self.con.execute('SELECT id,name,code FROM tone_codes ORDER BY id'):
            self.tone_tree.insert('', 'end', iid=str(r['id']), values=(r['name'], r['code']))

    # Přidá nový analogový kanál.
    def add_channel(self):
        iid = 'new_ch_' + str(len([i for i in self.channel_tree.get_children() if str(i).startswith('new_ch_')]) + 1)
        self.channel_tree.insert('', 'end', iid=iid, values=('Nový kanál', '446.00000'))
        self.channel_tree.selection_set(iid); self.channel_tree.see(iid)

    # Přidá nový CTCSS/DCS kód.
    def add_tone(self):
        iid = 'new_tone_' + str(len([i for i in self.tone_tree.get_children() if str(i).startswith('new_tone_')]) + 1)
        self.tone_tree.insert('', 'end', iid=iid, values=('Nový kód', ''))
        self.tone_tree.selection_set(iid); self.tone_tree.see(iid)

    # Smaže vybraný analogový kanál.
    def delete_channel(self):
        sel = self.channel_tree.selection()
        if not sel: return
        iid = sel[0]
        if not messagebox.askyesno('Smazat', 'Smazat vybraný analogový kanál?'):
            return
        if not str(iid).startswith('new_ch_'):
            self.con.execute('DELETE FROM channels WHERE id=?', (int(iid),)); self.con.commit()
        self.channel_tree.delete(iid)

    # Smaže vybraný CTCSS/DCS kód.
    def delete_tone(self):
        sel = self.tone_tree.selection()
        if not sel: return
        iid = sel[0]
        if not messagebox.askyesno('Smazat', 'Smazat vybraný CTCSS/DCS kód?'):
            return
        if not str(iid).startswith('new_tone_'):
            self.con.execute('DELETE FROM tone_codes WHERE id=?', (int(iid),)); self.con.commit()
        self.tone_tree.delete(iid)

    # Doplní výchozí PMR kanály 1 až 16.
    def reset_channels(self):
        for ch, fr in PMR_CHANNELS.items():
            self.con.execute('INSERT OR IGNORE INTO channels(name, frequency) VALUES(?, ?)', (f'PMR {ch}', f'{fr:.5f}'))
        self.con.commit(); self.load_channels(); self.status_var.set('Výchozí PMR kanály doplněny.')

    # Doplní výchozí CTCSS/DCS kódy.
    def reset_tones(self):
        for name, code in DEFAULT_CTCSS_DCS_CODES:
            self.con.execute('INSERT OR IGNORE INTO tone_codes(name, code) VALUES(?, ?)', (name, code))
        self.con.commit(); self.load_tones(); self.status_var.set('Výchozí CTCSS/DCS kódy doplněny.')

    # Uloží analogové kanály i CTCSS/DCS kódy.
    def save_all(self):
        self.finish_edit()
        try:
            for item in self.channel_tree.get_children():
                vals = list(self.channel_tree.item(item, 'values'))
                name = (vals[0] if len(vals)>0 else '').strip()
                freq = (vals[1] if len(vals)>1 else '').strip().replace(',', '.')
                if not name or not freq:
                    messagebox.showerror('Chyba', 'Název a frekvence analogového kanálu musí být vyplněné.'); return
                float(freq)
                if str(item).startswith('new_ch_'):
                    self.con.execute('INSERT OR IGNORE INTO channels(name, frequency) VALUES(?, ?)', (name, freq))
                else:
                    self.con.execute('UPDATE channels SET name=?, frequency=? WHERE id=?', (name, freq, int(item)))
            for item in self.tone_tree.get_children():
                vals = list(self.tone_tree.item(item, 'values'))
                name = (vals[0] if len(vals)>0 else '').strip()
                code = (vals[1] if len(vals)>1 else '').strip().upper().replace(' ', '')
                if not name:
                    messagebox.showerror('Chyba', 'Název CTCSS/DCS kódu musí být vyplněný.'); return
                if str(item).startswith('new_tone_'):
                    self.con.execute('INSERT OR IGNORE INTO tone_codes(name, code) VALUES(?, ?)', (name, code))
                else:
                    self.con.execute('UPDATE tone_codes SET name=?, code=? WHERE id=?', (name, code, int(item)))
            self.con.commit(); self.load_channels(); self.load_tones()
            self.status_var.set('Změny uloženy.'); messagebox.showinfo('Hotovo', 'Analogová nastavení byla uložena.')
        except ValueError:
            messagebox.showerror('Chyba', 'Frekvence musí být číslo, například 446.00625.')
        except sqlite3.Error as e:
            messagebox.showerror('Chyba databáze', str(e))


# Okno pro správu digitálních kanálů a jejich parametrů.
class DigitalChannelSettings:

    # Inicializace okna nebo části aplikace.
    def __init__(self, app):
        self.app = app
        self.con = app.con
        self.win = tk.Toplevel(app.root)
        self.win.title("Nastavení digitálních kanálů")
        self.win.geometry("1180x560")
        self.win.minsize(1180, 560)
        self.win.transient(app.root)
        self.win.grab_set()
        self.editing_item = None
        self.sort_col = "id"
        self.sort_desc = False
        self.columns = ("name", "frequency", "tg", "cc", "call_group", "operation", "station_name", "digital_id", "contact")


        self.digital_operation_values = []

        self.ui()
        self.load()

    # Načte povolené typy digitálního provozu.
    def load_digital_operation_values(self):


        self.digital_operation_values = [
            row["name"]
            for row in self.con.execute("SELECT name FROM operation_types_digital ORDER BY id")
        ]
        return self.digital_operation_values

    # Vrátí první dostupný typ digitálního provozu.
    def first_digital_operation_value(self):

        values = self.load_digital_operation_values()
        return values[0] if values else ""

    # Vytvoří grafické rozhraní daného okna.
    def ui(self):
        main = ttk.Frame(self.win)
        main.place(x=0, y=0, relwidth=1, relheight=1)
        ttk.Label(main, text="Tabulka digitálních kanálů", font=('Ubuntu', 14, 'bold')).place(x=14, y=10, width=500, height=28)
        ttk.Label(main, text="Dvojklikem upravíš buňku.").place(x=14, y=40, width=760, height=24)
        table_card = ttk.Frame(main, style='Card.TFrame')
        table_card.place(x=14, y=78, relwidth=1.0, width=-28, relheight=1.0, height=-152)
        self.tree = ttk.Treeview(table_card, columns=self.columns, show="headings", selectmode="browse")
        self.tree.place(x=10, y=10, relwidth=1.0, width=-28, relheight=1.0, height=-20)
        heads = {
            "name":"Název", "frequency":"Frekvence MHz", "tg":"TG", "cc":"CC",
            "call_group":"Volací skupina", "operation":"Provoz", "station_name":"Jméno",
            "digital_id":"ID", "contact":"Kontakt"
        }
        widths = {"name":150, "frequency":120, "tg":60, "cc":55, "call_group":120, "operation":130, "station_name":190, "digital_id":90, "contact":120}
        for c in self.columns:
            self.tree.heading(c, text=heads[c], command=lambda x=c: self.sort(x))
            self.tree.column(c, width=widths[c], anchor='center' if c in ('frequency','tg','cc','call_group','digital_id','contact') else 'w')
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        scrollbar.place(relx=1.0, x=-18, y=10, width=18, relheight=1.0, height=-20)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<Double-1>", self.start_cell_edit)
        self.tree.bind("<Return>", self.start_cell_edit)
        buttons = ttk.Frame(main)
        buttons.place(x=14, rely=1.0, y=-72, relwidth=1.0, width=-28, height=42)
        ttk.Button(buttons, text="✚  Přidat řádek", command=self.add_row).pack(side="left", padx=(0, 6))
        ttk.Button(buttons, text="🗑  Smazat řádek", command=self.delete_selected_row).pack(side="left", padx=6)
        ttk.Button(buttons, text="💾  Uložit změny", command=self.save_changes, style='Accent.TButton').pack(side="left", padx=6)
        ttk.Button(buttons, text="Doplnit výchozí", command=self.reset_defaults).pack(side="left", padx=6)
        ttk.Button(buttons, text="✖  Zavřít", command=self.win.destroy).pack(side="right", padx=(6,0))
        self.status_var = tk.StringVar(value="Připraveno")
        ttk.Label(main, textvariable=self.status_var, anchor="w", style='Subtitle.TLabel').place(x=14, rely=1.0, y=-28, width=700, height=20)

    # Vrátí SQL řazení pro aktuální tabulku.
    def order_sql(self):
        direction = "DESC" if self.sort_desc else "ASC"
        if self.sort_col in self.columns:
            return f"{self.sort_col} COLLATE NOCASE {direction}, id ASC"
        return "id ASC"

    # Načte data do okna nebo tabulky.
    def load(self):
        self.cancel_cell_edit()
        self.load_digital_operation_values()
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = list(self.con.execute(f"SELECT id,name,frequency,tg,cc,call_group,operation,station_name,digital_id,contact FROM digital_channels ORDER BY {self.order_sql()}"))
        for r in rows:
            self.tree.insert('', 'end', iid=str(r['id']), values=tuple(r[c] or '' for c in self.columns))
        self.status_var.set(f"Načteno digitálních kanálů: {len(rows)}")

    # Nastaví řazení podle vybraného sloupce.
    def sort(self, column):
        self.finish_cell_edit()
        if self.sort_col == column:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_col = column
            self.sort_desc = False
        self.load()

    # Přidá nový řádek do editační tabulky.
    def add_row(self):
        self.cancel_cell_edit()
        temp_id = "new_" + str(len([i for i in self.tree.get_children() if str(i).startswith('new_')]) + 1)


        default_operation = self.first_digital_operation_value()

        self.tree.insert('', 'end', iid=temp_id, values=("Nový digitální kanál", "", "", "", "", default_operation, "", "", ""))
        self.tree.selection_set(temp_id); self.tree.see(temp_id)

    # Smaže vybraný řádek z editační tabulky.
    def delete_selected_row(self):
        self.cancel_cell_edit(); sel=self.tree.selection()
        if not sel:
            messagebox.showwarning("Smazat řádek", "Nejdříve vyber řádek."); return
        item=sel[0]
        if not messagebox.askyesno("Smazat řádek", "Opravdu smazat vybraný řádek?"):
            return
        if not str(item).startswith('new_'):
            self.con.execute("DELETE FROM digital_channels WHERE id=?", (int(item),)); self.con.commit()
        self.tree.delete(item)

    # Spustí editaci buňky přímo v tabulce.
    def start_cell_edit(self, event=None):
        self.cancel_cell_edit()
        if event is not None:
            if self.tree.identify('region', event.x, event.y) != 'cell': return
            item = self.tree.identify_row(event.y); col = self.tree.identify_column(event.x)
        else:
            sel = self.tree.selection();
            if not sel: return
            item = sel[0]; col = '#1'
        if not item or col not in [f'#{i}' for i in range(1, len(self.columns)+1)]: return
        idx = int(col[1:]) - 1
        bbox = self.tree.bbox(item, col)
        if not bbox: return
        x,y,w,h = bbox
        vals = list(self.tree.item(item, 'values'))
        self.editing_item=(item,idx)
        self.edit_var=tk.StringVar(value=vals[idx] if idx < len(vals) else '')


        if self.columns[idx] == "operation":
            values = self.load_digital_operation_values()
            self.edit_entry = ttk.Combobox(
                self.tree,
                textvariable=self.edit_var,
                values=values,
                state="readonly"
            )
            if self.edit_var.get().strip() not in values:
                self.edit_var.set(values[0] if values else "")
        else:
            self.edit_entry=ttk.Entry(self.tree, textvariable=self.edit_var)

        self.edit_entry.place(x=x,y=y,width=w,height=h)
        self.edit_entry.focus_set()
        try:
            self.edit_entry.select_range(0,'end')
        except Exception:
            pass
        self.edit_entry.bind('<Return>', lambda e: self.finish_cell_edit())
        self.edit_entry.bind('<Escape>', lambda e: self.cancel_cell_edit())


        if self.columns[idx] == "operation":
            self.edit_entry.bind('<<ComboboxSelected>>', lambda e: self.finish_cell_edit())
        else:
            self.edit_entry.bind('<FocusOut>', lambda e: self.finish_cell_edit())

    # Dokončí editaci buňky a uloží hodnotu do tabulky.
    def finish_cell_edit(self):
        if not self.editing_item: return
        item, idx = self.editing_item
        vals = list(self.tree.item(item, 'values'))
        while len(vals) < len(self.columns): vals.append('')
        vals[idx] = self.edit_var.get().strip()
        self.tree.item(item, values=vals)
        self.cancel_cell_edit(clear_only=True)

    # Zruší právě probíhající editaci buňky.
    def cancel_cell_edit(self, clear_only=False):
        if hasattr(self, 'edit_entry'):
            try: self.edit_entry.destroy()
            except Exception: pass
            del self.edit_entry
        if hasattr(self, 'edit_var'): del self.edit_var
        self.editing_item=None

    # Uloží změny z editačního okna.
    def save_changes(self):
        self.finish_cell_edit()
        try:
            for item in self.tree.get_children():
                vals=list(self.tree.item(item,'values'))
                while len(vals) < len(self.columns): vals.append('')
                name, frequency, tg, cc, call_group, operation, station_name, digital_id, contact = [str(v).strip() for v in vals[:9]]
                if not name:
                    messagebox.showerror('Chyba', 'Název digitálního kanálu nesmí být prázdný.'); return


                allowed_operations = self.load_digital_operation_values()
                if not allowed_operations:
                    messagebox.showerror(
                        'Chyba',
                        'Seznam digitálních typů spojení je prázdný.\n'
                        'Nejdříve jej doplň v Nastavení -> Nastavení typů spojení.'
                    )
                    return
                if operation not in allowed_operations:
                    messagebox.showerror(
                        'Chyba',
                        f'Řádek digitálního kanálu "{name}" má neplatný provoz:\n\n'
                        f'{operation or "(prázdné)"}\n\n'
                        'Vyber hodnotu ze seznamu digitálních typů spojení.'
                    )
                    return

                if str(item).startswith('new_'):
                    self.con.execute("INSERT OR IGNORE INTO digital_channels(name,frequency,tg,cc,call_group,operation,station_name,digital_id,contact) VALUES(?,?,?,?,?,?,?,?,?)", (name,frequency,tg,cc,call_group,operation,station_name,digital_id,contact))
                else:
                    self.con.execute("UPDATE digital_channels SET name=?,frequency=?,tg=?,cc=?,call_group=?,operation=?,station_name=?,digital_id=?,contact=? WHERE id=?", (name,frequency,tg,cc,call_group,operation,station_name,digital_id,contact,int(item)))
            self.con.commit(); self.load(); messagebox.showinfo('Hotovo','Digitální kanály byly uloženy.')
        except sqlite3.Error as e:
            messagebox.showerror('Chyba databáze', str(e))

    # Doplní výchozí hodnoty do nastavení.
    def reset_defaults(self):
        if not messagebox.askyesno('Doplnit výchozí', 'Doplnit výchozí digitální kanály?'):
            return
        for row in DEFAULT_DIGITAL_CHANNELS:
            self.con.execute('INSERT OR IGNORE INTO digital_channels(name,frequency,tg,cc,call_group,operation,station_name,digital_id,contact) VALUES(?,?,?,?,?,?,?,?,?)', row)
        self.con.commit(); self.load()


# Vytvoří hlavní okno a spustí aplikaci.
def main():

    root=tk.Tk()
    apply_light_style(root)
    App(root); root.mainloop()

if __name__=='__main__': main()
