# Colombian Public Investment Projects — what the registry can and cannot tell us

*[Leer en español](#español)*

Analysis of **530,732 public-investment projects** from Colombia's national planning department (DNP, *Banco de Proyectos*). The main finding is as much about data quality as about investment: several "obvious" conclusions you can draw from this dataset are artifacts.

## Key findings

| # | Finding | Evidence |
|---|---|---|
| 1 | **Status is not comparable across funding sources.** "Finished" exists only for SGR (royalties), so "% of projects finished" over the whole file is meaningless. | `outputs/04_pipeline_by_source.png` |
| 2 | **Value is extremely concentrated.** The top 1% of valued projects hold ~75% of total value; the median project is ~423 M COP vs a mean of ~12,900 M COP. | `outputs/02_value_distribution.png` |
| 3 | **55% of projects have no value recorded** (zero ≠ free). They are treated as missing. | notebook 01 |
| 4 | **Within SGR, longer planned projects finish *more* often** (51% for 1–3 yrs, 87% for 4–10, 91% for >10, cohort started ≤2021). Counting only finished projects would suggest the opposite (survivorship bias). | `outputs/05_sgr_finished_by_duration.png` |
| 5 | **Cost per beneficiary can't support an efficiency ranking:** the column contains impossible values (up to 48 billion in a country of ~52 million) and spans ~6 orders of magnitude even after cleaning. | notebook 01 §5, notebook 02 §7 |

## What changed from version 1
Version 1 ranked sectors by "efficiency" = beneficiaries per peso and concluded that short projects are the most successful. Checking the raw data showed both were artifacts (typos in beneficiaries, a unit error, and survivorship bias). Version 2 documents each issue and fixes it.

## Structure
```
notebooks/01_data_cleaning.ipynb   data understanding, quality issues, documented decisions
notebooks/02_analysis.ipynb        question → method → result → limit, for each analysis
notebooks/03_sql_duckdb.ipynb      key results reproduced in SQL (CTEs, window functions)
src/dnp_utils.py                   loading + cleaning helpers
scripts/download_data.py           downloads the dataset from datos.gov.co
outputs/                           figures
```

## Reproduce
```bash
pip install -r requirements.txt
python scripts/download_data.py        # ~320 MB, saved with today's date
jupyter lab                            # run notebooks 01 → 02 → 03
```

## Limitations
Values are undocumented in currency/units (assumed nominal COP, not inflation-adjusted); the meaning of *Total* vs *Vigente* value is not documented; analyses are descriptive associations, not causal claims.

**Data:** [DNP-proyectos_datos_basicos, datos.gov.co](https://www.datos.gov.co/en/Econom-a-y-Finanzas/DNP-proyectos_datos_basicos/cf9k-55fw), CC BY-SA 4.0, snapshot 2026-11-25. **Tools:** Python, pandas, DuckDB/SQL, matplotlib.

---

## Español

Análisis de **530.732 proyectos de inversión pública** del Departamento Nacional de Planeación (DNP). El hallazgo principal trata tanto de calidad de datos como de inversión: varias conclusiones "obvias" de este dataset son artefactos.

**Hallazgos:** (1) el estado "Terminado" solo existe en SGR, así que "% finalizados" global no significa nada; (2) el 1% de proyectos con valor concentra ~75% del valor total; (3) el 55% de proyectos no tiene valor registrado; (4) en SGR los proyectos de mayor duración planeada se terminan *más* (51% / 87% / 91%), lo contrario de lo que sugiere mirar solo los terminados; (5) la columna de beneficiarios tiene valores imposibles, por lo que no sirve para un ranking de eficiencia.

**Cómo reproducir:** `pip install -r requirements.txt`, `python scripts/download_data.py` y ejecutar los notebooks 01 → 02 → 03.
