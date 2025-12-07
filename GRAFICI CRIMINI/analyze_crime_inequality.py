import pandas as pd
import matplotlib.pyplot as plt



COUNTRY_LABELS = {
    "ITA": "Italy",
    "ESP": "Spain",
    "FRA": "France",
    "DEU": "Germany",
    "GBR": "United Kingdom",
    "USA": "United States",
    "MEX": "Mexico",
    "BRA": "Brazil",
}

# Eventi importanti (anno, etichetta) per alcune nazioni
EVENTI = {
    "BRA": [
        (1994, "Plano Real"),
        (2003, "Inizio Lula"),
        (2010, "Fine Lula /\ninizio Dilma"),
        (2014, "Recessione\n+ crisi politica"),
        (2016, "Impeachment\nRousseff"),
        (2019, "Inizio\nBolsonaro"),
    ],
    "USA": [
        (1994, "Crime Bill"),
        (2001, "Attacchi\n11/9"),
        (2008, "Crisi\nfinanziaria"),
        (2014, "Tensioni\nrazziali"),
        (2020, "COVID-19"),
    ],
    "ITA": [
        (1992, "Stragi\nmafia"),
        (1994, "Seconda\nRepubblica"),
        (2008, "Crisi\nfinanziaria"),
        (2011, "Crisi debito /\nGoverno Monti"),
        (2020, "COVID-19"),
    ],
    "ESP": [
        (2008, "Crisi\nfinanziaria"),
        (2012, "Picco\ndisoccupazione"),
        (2020, "COVID-19"),
    ],
    "GBR": [
        (2008, "Crisi\nfinanziaria"),
        (2016, "Brexit\nreferendum"),
        (2020, "COVID-19"),
    ],
    "FRA": [
        (1995, "Proteste\nsociali"),
        (2008, "Crisi\nfinanziaria"),
        (2015, "Attacchi\nterroristici"),
        (2020, "COVID-19"),
    ],
    "DEU": [
        (1990, "Ri-unificazione"),
        (2008, "Crisi\nfinanziaria"),
        (2015, "Crisi\nmigratoria"),
        (2020, "COVID-19"),
    ],
    "MEX": [
        (1994, "Crisi\npeso"),
        (2006, "Guerra al\nnarcotraffico"),
        (2014, "Caso\nAyotzinapa"),
        (2020, "COVID-19"),
    ],
}


def scatter_gini_vs_homicide_by_country(df):
    """
    Grafico riassuntivo:
    - un punto medio per ogni paese (media Gini / media omicidi)
    """
    plt.figure(figsize=(8, 5))

    for code, sub in df.groupby("country_code"):
        name = COUNTRY_LABELS.get(code, code)
        mean_gini = sub["gini_index"].mean()
        mean_hom = sub["homicide_rate"].mean()

        plt.scatter(
            mean_gini,
            mean_hom,
            s=200,
            alpha=0.8,
            edgecolor="black",
            linewidth=1,
        )
        plt.text(
            mean_gini,
            mean_hom,
            f"  {name}",
            va="center",
            fontsize=10,
        )

    plt.xlabel("Indice di Gini (disuguaglianza)")
    plt.ylabel("Tasso di omicidi (per 100.000 abitanti)")
    plt.title("Disuguaglianza e omicidi per paese (media 1990–2020 circa)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def time_series_country(df, country_code):
    """
    Grafico nel tempo per un singolo paese:
    - GINI (asse sinistro, blu)
    - Tasso di omicidi (asse destro, rosso)
    - Linee verticali per eventi storici
    """
    sub = df[df["country_code"] == country_code].copy()
    sub = sub.sort_values("year")

    if sub.empty:
        print(f"Nessun dato per il paese {country_code}")
        return

    fig, ax1 = plt.subplots(figsize=(8, 4))

    # Gini (asse sinistro) - BLU
    line_gini, = ax1.plot(
        sub["year"],
        sub["gini_index"],
        marker="o",
        linestyle="-",
        color="blue",
        label="Indice di Gini",
    )
    ax1.set_xlabel("Anno")
    ax1.set_ylabel("Indice di Gini", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # Omicidi (secondo asse) - ROSSO
    ax2 = ax1.twinx()
    line_hom, = ax2.plot(
        sub["year"],
        sub["homicide_rate"],
        marker="s",
        linestyle="--",
        color="red",
        label="Tasso di omicidi",
    )
    ax2.set_ylabel("Tasso di omicidi (per 100.000 abitanti)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Eventi storici
    eventi_paese = EVENTI.get(country_code, [])
    if eventi_paese:
        ymin, ymax = ax1.get_ylim()
        y_testo = ymax
        for year, label in eventi_paese:
            ax1.axvline(x=year, linestyle=":", linewidth=1, color="gray")
            ax1.text(
                year,
                y_testo,
                label,
                rotation=90,
                va="bottom",
                ha="center",
                fontsize=8,
            )

    # Legenda combinata
    lines = [line_gini, line_hom]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper right", fontsize=8)

    title_name = COUNTRY_LABELS.get(country_code, country_code)
    plt.title(f"Disuguaglianza e omicidi nel tempo - {title_name}")
    fig.tight_layout()
    plt.show()


def plot_poverty_country(df, country_code):
    """
    Grafico della povertà assoluta nel tempo per un singolo paese
    + linea del tasso di omicidi per vedere la relazione.

    - Povertà: linea blu con punti (asse sinistro)
    - Omicidi: linea rossa (asse destro)
    - Asse x zoomato sugli anni in cui ho dati di povertà
    """
    sub = df[df["country_code"] == country_code].copy()
    sub = sub.sort_values("year")

    if "poverty_rate" not in sub.columns:
        print(f"Nessuna colonna poverty_rate per {country_code}")
        return

    # anni con dato di povertà
    sub_pov = sub[sub["poverty_rate"].notna()].copy()
    if sub_pov.empty:
        print(f"Nessun dato di povertà per il paese {country_code}")
        return

    year_min = sub_pov["year"].min()
    year_max = sub_pov["year"].max()

    # omicidi solo nello stesso intervallo
    sub_hom = sub[(sub["year"] >= year_min) & (sub["year"] <= year_max)].copy()

    fig, ax1 = plt.subplots(figsize=(8, 3.5))

    # Povertà: linea blu + marker
    line_pov, = ax1.plot(
        sub_pov["year"],
        sub_pov["poverty_rate"],
        marker="o",
        linestyle="-",
        color="blue",
        label="Povertà assoluta (% popolazione)",
    )
    ax1.set_xlabel("Anno")
    ax1.set_ylabel("Povertà assoluta (% popolazione)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.grid(True, alpha=0.3)

    # Omicidi: linea rossa
    line_hom = None
    if "homicide_rate" in sub_hom.columns and sub_hom["homicide_rate"].notna().any():
        ax2 = ax1.twinx()
        line_hom, = ax2.plot(
            sub_hom["year"],
            sub_hom["homicide_rate"],
            marker="s",
            linestyle="--",
            color="red",
            label="Tasso di omicidi",
        )
        ax2.set_ylabel("Tasso di omicidi (per 100.000 abitanti)", color="red")
        ax2.tick_params(axis="y", labelcolor="red")

    # Zoom sugli anni in cui ho povertà
    ax1.set_xlim(year_min - 1, year_max + 1)

    ax1.set_title(
        f"Povertà assoluta e omicidi nel tempo - "
        f"{COUNTRY_LABELS.get(country_code, country_code)}"
    )

    # Legenda combinata
    lines = [line_pov]
    labels = [line_pov.get_label()]
    if line_hom is not None:
        lines.append(line_hom)
        labels.append(line_hom.get_label())

    ax1.legend(lines, labels, loc="upper right", fontsize=8)

    fig.tight_layout()
    plt.show()


def plot_youth_country(df, country_code):
    """
    Grafico della quota di giovani maschi 15–24 anni nel tempo.
    """
    sub = df[df["country_code"] == country_code].copy()
    sub = sub.sort_values("year")

    if "youth_male_15_24" not in sub.columns or sub["youth_male_15_24"].isna().all():
        print(f"Nessun dato sui giovani 15–24 per il paese {country_code}")
        return

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(
        sub["year"],
        sub["youth_male_15_24"],
        marker="o",
        linestyle="-",
        label="Maschi 15–24 anni (% popolazione maschile)",
    )
    ax.set_xlabel("Anno")
    ax.set_ylabel("Maschi 15–24 anni (% uomini)")
    ax.set_title(
        f"Giovani maschi 15–24 nel tempo - "
        f"{COUNTRY_LABELS.get(country_code, country_code)}"
    )
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    plt.show()


def correlation_by_country(df):
    """
    Calcola e stampa la matrice di correlazione per ciascun paese
    tra:
        - homicide_rate
        - gini_index
        - poverty_rate
        - youth_male_15_24 (se presente)
    """
    vars_cols = ["homicide_rate", "gini_index", "poverty_rate", "youth_male_15_24"]
    existing_cols = [c for c in vars_cols if c in df.columns]

    print("\n===== MATRICI DI CORRELAZIONE PER PAESE =====")
    for code in sorted(df["country_code"].unique()):
        sub = df[df["country_code"] == code][existing_cols].dropna(how="any")
        name = COUNTRY_LABELS.get(code, code)

        if len(sub) < 3:
            print(f"\n{code} ({name}): dati insufficienti per calcolare la correlazione (meno di 3 anni utili).")
            continue

        corr = sub.corr()

        print(f"\n=== {code} - {name} ===")
        # Arrotondo a 2 decimali per leggibilità
        print(corr.round(2))


def main():
    df = pd.read_csv("crime_inequality.csv")
    print("Colonne nel CSV:", df.columns.tolist())

    required = ["country_code", "year", "homicide_rate", "gini_index"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Manca la colonna obbligatoria: {col}")

    # 0) Matrici di correlazione per ogni paese (stampa in console)
    correlation_by_country(df)

    # 1) Scatter riassuntivo
    scatter_gini_vs_homicide_by_country(df)

    # 2) Grafici temporali per ogni paese
    for code in sorted(df["country_code"].unique()):
        time_series_country(df, code)
        plot_poverty_country(df, code)
        plot_youth_country(df, code)


if __name__ == "__main__":
    main()

# Spiegazione matrice di correlazione – Brasile
#
# homicide_rate ↔ gini_index = -0.33
# → Correlazione negativa debole: quando la disuguaglianza aumenta, gli omicidi
#   tendono leggermente a diminuire. Questo risultato può sembrare controintuitivo,
#   ma nel caso del Brasile rispecchia periodi in cui le politiche sociali (anni 2000)
#   hanno ridotto il GINI mentre la violenza rimaneva elevata a causa di fattori
#   indipendenti (narcotraffico, guerre tra cartelli, controllo territoriale nelle favelas).
#
# homicide_rate ↔ poverty_rate = -0.66
# → Correlazione negativa moderata-forte: quando la povertà diminuisce, gli omicidi
#   NON diminuiscono necessariamente. Anzi, in diversi anni gli omicidi sono aumentati
#   mentre la povertà diminuiva. Questo indica che la povertà assoluta non è la
#   variabile chiave che determina la violenza in Brasile.
#
# homicide_rate ↔ youth_male_15_24 = -0.63
# → Correlazione negativa moderata: anche la quota di giovani maschi è inversamente
#   correlata agli omicidi. Ciò suggerisce che i picchi di violenza in Brasile
#   non dipendono tanto dalla demografia, ma da dinamiche criminali e istituzionali.
#
# gini_index ↔ poverty_rate = 0.82
# → Relazione positiva molto forte: quando la povertà diminuisce, diminuisce anche
#   la disuguaglianza, e viceversa. Le due variabili sono strettamente legate,
#   coerentemente con le politiche sociali brasiliane (es. Bolsa Família) che
#   hanno ridotto entrambe.
#
# gini_index ↔ youth_male_15_24 = 0.79
# → Anche la disuguaglianza si muove quasi parallelamente alla quota di giovani.
#   Non perché i giovani “creino” disuguaglianza, ma perché entrambe riflettono
#   fattori strutturali (sviluppo economico, urbanizzazione, mercato del lavoro).
#
# poverty_rate ↔ youth_male_15_24 = 0.96
# → Correlazione quasi perfetta: la presenza di giovani maschi è altissima proprio
#   negli anni in cui la povertà è più elevata. Questo riflette fenomeni socio-
#   demografici (alta natalità negli anni ’80–’90) che coincidono con periodi di
#   maggior povertà economica.
#
# In sintesi:
# - La povertà e la disuguaglianza sono fortemente collegate tra loro.
# - Tuttavia, entrambe mostrano correlazioni NEGATIVE con gli omicidi.
# - Questo indica che, nel caso del Brasile, i tassi di omicidio sono guidati più
#   da fattori legati al narcotraffico, alle gang e alla debolezza istituzionale
#   che da povertà o struttura socioeconomica.
#
# Questo risultato dimostra che la relazione tra povertà, disuguaglianza e violenza
# non è lineare: in Brasile le dinamiche criminali pesano molto più della condizione
# economica media della popolazione.
