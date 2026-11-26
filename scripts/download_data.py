"""Download the DNP "proyectos_datos_basicos" open dataset from datos.gov.co.

Dataset: https://www.datos.gov.co/en/Econom-a-y-Finanzas/DNP-proyectos_datos_basicos/cf9k-55fw
Publisher: Departamento Nacional de Planeación (DNP). License: CC BY-SA 4.0.

The file is large (~320 MB) and the portal updates it periodically, so the script
saves it with today's date in the file name. Use that date when citing results.

Usage:  python scripts/download_data.py
"""
import datetime as dt
from pathlib import Path

import requests

URL = "https://www.datos.gov.co/api/views/cf9k-55fw/rows.csv?accessType=DOWNLOAD"
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
target = RAW / f"DNP-proyectos_datos_basicos_{dt.date.today():%Y%m%d}.csv"

with requests.get(URL, stream=True, timeout=120) as r:
    r.raise_for_status()
    with open(target, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 20):
            f.write(chunk)
print("Saved", target, f"({target.stat().st_size / 1e6:.0f} MB)")
