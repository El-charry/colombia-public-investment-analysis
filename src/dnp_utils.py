"""Shared helpers for the DNP public-investment projects analysis."""
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

# Colombia has roughly 52 million inhabitants. A single project cannot have more
# beneficiaries than that, so anything above this (generous) cap is a data-entry error.
MAX_PLAUSIBLE_BENEFICIARIES = 60_000_000
# Planned end year after which a horizon is treated as implausible.
MAX_PLAUSIBLE_END_YEAR = 2040

STATE_GROUP = {
    "Formulación": "Pre-execution", "Viable": "Pre-execution", "Aprobado": "Pre-execution",
    "No Viable": "Rejected", "Desaprobado": "Rejected", "No Aprobado": "Rejected",
    "En Ejecución": "In execution", "Terminado": "Finished",
}
TYPE_CLEAN = {"Pgn": "PGN", "PGN": "PGN", "Sgr": "SGR", "Territorial": "Territorial"}


def latest_raw_file() -> Path:
    files = sorted(RAW.glob("DNP-proyectos_datos_basicos*.csv"))
    if not files:
        raise FileNotFoundError("No CSV found in data/raw. Run: python scripts/download_data.py")
    return files[-1]


def load_raw() -> pd.DataFrame:
    """Read the raw CSV with DuckDB (fast) and return a pandas DataFrame.

    ObjetivoGeneral (long free text) is left out: it is not used in the analysis.
    """
    path = latest_raw_file().as_posix()
    con = duckdb.connect()
    return con.execute(
        f"SELECT * EXCLUDE (ObjetivoGeneral) FROM read_csv('{path}', header=true, sample_size=-1)"
    ).df()


def add_clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add normalised columns and quality flags. Original columns are never overwritten."""
    d = df.copy()
    d["TypeClean"] = d["TipoProyecto"].map(TYPE_CLEAN).fillna(d["TipoProyecto"])
    d["StateGroup"] = d["EstadoProyecto"].map(STATE_GROUP).fillna("Other")
    d["Plan"] = d["PlanDesarrolloNacional"].fillna("No plan recorded")

    years = d["Horizonte"].str.split("-", n=1, expand=True)
    d["StartYear"] = pd.to_numeric(years[0], errors="coerce")
    d["EndYear"] = pd.to_numeric(years[1], errors="coerce")
    d["HorizonYears"] = d["EndYear"] - d["StartYear"] + 1

    # Quality flags
    d["has_value"] = d["ValorTotalProyecto"] > 0
    d["horizon_suspect"] = d["EndYear"] > MAX_PLAUSIBLE_END_YEAR
    d["benef_valid"] = d["TotalBeneficiario"].between(1, MAX_PLAUSIBLE_BENEFICIARIES)
    return d
