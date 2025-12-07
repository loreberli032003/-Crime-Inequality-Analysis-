import requests
import pandas as pd


def fetch_world_bank_indicator(indicator, countries, start_year, end_year):
    """dati scaricata da World Bank """
    rows = []

    for country in countries:
        url = (
            f"https://api.worldbank.org/v2/country/{country}/indicator/"
            f"{indicator}?format=json&per_page=1000&date={start_year}:{end_year}"
        )
        print(f"Scarico {indicator} per {country}...")
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        # data[0] = metadati, data[1] = lista dei record
        if len(data) < 2 or data[1] is None:
            print(f"Nessun dato per {country} - indicatore {indicator}")
            continue

        for item in data[1]:
            if item["value"] is None:
                continue

            year = int(item["date"])
            value = float(item["value"])
            country_name = item["country"]["value"]
            rows.append({
                "country_code": country,
                "country_name": country_name,
                "year": year,
                "value": value
            })

    
    df = pd.DataFrame(rows, columns=["country_code", "country_name", "year", "value"])
    print(f"Scaricati {len(df)} record per indicatore {indicator}")
    print("Colonne del DataFrame:", df.columns.tolist())
    return df


def main():
    countries   = ["ITA", "ESP", "FRA", "DEU", "GBR", "USA", "MEX", "BRA"]
    start_year  = 1990
    end_year    = 2020

    # 1) Tasso di omicidi (per 100.000 abitanti)
    homicide_indicator = "VC.IHR.PSRC.P5"
    df_homicide = fetch_world_bank_indicator(
        homicide_indicator, countries, start_year, end_year
    )
    df_homicide = df_homicide.rename(columns={"value": "homicide_rate"})
    print("df_homicide colonne:", df_homicide.columns.tolist())

    # 2) Indice di GINI (disuguaglianza)
    gini_indicator = "SI.POV.GINI"
    df_gini = fetch_world_bank_indicator(
        gini_indicator, countries, start_year, end_year
    )
    df_gini = df_gini.rename(columns={"value": "gini_index"})
    print("df_gini colonne:", df_gini.columns.tolist())

    # 3) Povertà (nuovo indicatore con più dati):
    #    SI.POV.LMIC = % popolazione sotto la soglia di povertà
    #    a 3.65 $/giorno PPP (lower-middle-income poverty line)
    poverty_indicator = "SI.POV.LMIC"
    df_pov = fetch_world_bank_indicator(
        poverty_indicator, countries, start_year, end_year
    )
    df_pov = df_pov.rename(columns={"value": "poverty_rate"})
    print("df_pov colonne:", df_pov.columns.tolist())

    # 4) Giovani maschi 15–24 (% forza lavoro maschile 15–24)
    #    SL.TLF.ACTI.1524.MA.ZS = labour force participation rate 15–24, male (%)
    youth_indicator = "SL.TLF.ACTI.1524.MA.ZS"
    df_youth = fetch_world_bank_indicator(
        youth_indicator, countries, start_year, end_year
    )
    df_youth = df_youth.rename(columns={"value": "youth_male_15_24"})
    print("df_youth colonne:", df_youth.columns.tolist())

    # Merge progressivo di tutti gli indicatori
    try:
        df = pd.merge(
            df_homicide,
            df_gini[["country_code", "year", "gini_index"]],
            on=["country_code", "year"],
            how="inner"
        )
        df = pd.merge(
            df,
            df_pov[["country_code", "year", "poverty_rate"]],
            on=["country_code", "year"],
            how="left"    # left per non perdere anni/paesi se manca la povertà
        )
        df = pd.merge(
            df,
            df_youth[["country_code", "year", "youth_male_15_24"]],
            on=["country_code", "year"],
            how="left"
        )
    except KeyError as e:
        print("ERRORE NEL MERGE, MANCANO DELLE COLONNE:", e)
        print("Colonne df_homicide:", df_homicide.columns.tolist())
        print("Colonne df_gini:", df_gini.columns.tolist())
        print("Colonne df_pov:", df_pov.columns.tolist())
        print("Colonne df_youth:", df_youth.columns.tolist())
        return

    # Togliamo righe senza dati base (omicidi / gini)
    df = df.dropna(subset=["homicide_rate", "gini_index"])

    # Ordiniamo il DataFrame
    df = df.sort_values(["country_code", "year"])

    # Salviamo il CSV
    df.to_csv("crime_inequality.csv", index=False)
    print("File crime_inequality.csv salvato con", len(df), "righe.")
    print("Colonne finali:", df.columns.tolist())


if __name__ == "__main__":
    main()
