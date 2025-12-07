# Crime & Inequality Analysis (1990–2020)

Questo progetto analizza la relazione tra:
- tasso di omicidi,
- disuguaglianza (indice di Gini),
- povertà assoluta,
- quota di giovani maschi 15–24 anni,

per 8 paesi: Italia, Spagna, Francia, Germania, Regno Unito, USA, Messico, Brasile.

I dati provengono dalla **World Bank API** e i grafici sono generati con Python (Pandas + Matplotlib).

---

## 📁 Contenuto del repository

### `download_data.py`
Script che scarica automaticamente gli indicatori dai database della World Bank e crea un file unico:

- homicide_rate (omicidi per 100.000)
- gini_index (indice di disuguaglianza)
- poverty_rate (% popolazione sotto la soglia LMIC)
- youth_male_15_24 (% uomini 15–24 nella forza lavoro)

Output finale:  
➡️ `crime_inequality.csv` (dataset pronto all'uso)

### `analyze_crime_inequality.py`
Script di analisi e visualizzazione. Include:

#### 1) Scatter plot riassuntivo  
Ogni paese è rappresentato da un punto (media omicidi vs media Gini).

#### 2) Serie storiche per singolo paese  
- Gini (asse sinistro, blu)  
- Omicidi (asse destro, rosso)  
- Linee verticali con eventi storici rilevanti (es. “Crime Bill 1994”, “Crisi 2008”, “COVID-19”)  

#### 3) Analisi povertà e omicidi  
Grafico della povertà assoluta con linea degli omicidi sovrapposta.

#### 4) Analisi demografica  
Grafico dell’evoluzione della quota di giovani maschi (15–24 anni).

#### 5) Matrici di correlazione  
Per ogni paese viene calcolata la correlazione tra:

- homicide_rate  
- gini_index  
- poverty_rate  
- youth_male_15_24 (se disponibile)

---

## ▶️ Come eseguire il progetto

### 1. Installazione dipendenze

2. Scaricare i dati (opzionale se hai già il CSV)
python download_data.py

Genera il file:

crime_inequality.csv

3. Avviare l’analisi
python analyze_crime_inequality.py

Verranno generati automaticamente:
scatter complessivo
grafici temporali per ciascun paese
grafici su povertà
grafici su demografia giovanile
matrici di correlazione stampate in console

Output principali
🔹 1) Relazione Gini–Omicidi

Scatter che mostra se i paesi con più disuguaglianza hanno anche più omicidi.

🔹 2) Andamento storico (Gini + Omicidi)

Valorizzato da eventi storici (es. crisi, riforme politiche, shock economici).

🔹 3) Povertà vs Omicidi

Permette di verificare se la criminalità si muove insieme alla povertà.

🔹 4) Giovani maschi 15–24

Analisi della componente demografica spesso associata ai fenomeni criminali.

🔹 5) Matrici di correlazione

Utile per confronti rapidi tra paesi.

Logica generale del progetto:
Scarico dei dati dalla World Bank via API.
Standardizzazione delle colonne e merge in un unico dataset.
Ordinamento per anno/paese.
Analisi statistica (correlazioni).
Visualizzazioni grafiche tematiche.
Collegamento tra cambiamenti socioeconomici e dinamiche criminali.
```bash
pip install pandas matplotlib requests
