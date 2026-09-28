"""
ingest_bps.py — INGEST BPS: kemiskinan & IPM per kabupaten/kota.

Strategi (dari temuan verifikasi):
  · var_id BEDA per domain → cari var_id per provinsi lewat model/var,
    cocokkan dengan judul target, lalu tarik datacontent.
  · datacontent = dict {vervar+var+turvar+th : nilai}; kunci provinsi = *_99.
  · Iterasi 34 domain × 6 tahun × N variabel target.

Output: data/staging/bps_indicators.parquet
  kolom: domain_id, domain_name, var_id, variable, unit, wilayah_kode,
         wilayah_nama, year, value, level ('provinsi'|'kabupaten')
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config import (BPS_API_KEY, BPS_BASE, BPS_SUBJECTS, BPS_YEARS,
                    STAGING, TARGET_VARS)

H = {"User-Agent": "geo-access-atlas/1.0", "Accept": "application/json"}


def _get(path: str, retries: int = 3):
    url = f"{BPS_BASE}{path}"
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=H)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))
    return None


def fetch_domains() -> list[dict]:
    """Daftar 34 domain provinsi BPS."""
    j = _get(f"/domain/type/prov/key/{BPS_API_KEY}/")
    return j["data"][1]


def fetch_vars(domain: str) -> list[dict]:
    """Semua variabel untuk subjek target di satu domain."""
    out = []
    for sub_id in BPS_SUBJECTS:
        try:
            j = _get(f"/list/model/var/domain/{domain}/subject/{sub_id}/"
                     f"key/{BPS_API_KEY}/")
            out += j.get("data", [{}])[1] if len(j.get("data", [])) > 1 else []
        except Exception:
            continue
    return out


def match_vars(vars_: list[dict]) -> list[dict]:
    """
    Saring variabel yang cocok judul target.
    PENTING: hindari varian 'menurut Klasifikasi Desa/Kota' — kita hanya mau
    yang 'menurut Kabupaten/Kota' agar tidak duplikat per wilayah.
    """
    picks = []
    for v in vars_:
        title = v.get("title", "")
        if "klasifikasi desa" in title.lower():
            continue
        for t in TARGET_VARS:
            if t.lower() in title.lower():
                picks.append(v)
                break
    return picks


def fetch_data(domain: str, var_id: int, th: int):
    j = _get(f"/list/model/data/domain/{domain}/var/{var_id}/th/{th}/"
             f"key/{BPS_API_KEY}/")
    return j


def main() -> None:
    t0 = time.time()
    if not BPS_API_KEY:
        raise SystemExit("BPS_API_KEY kosong — isi .env")

    domains = fetch_domains()
    print(f"[bps] {len(domains)} domain provinsi")

    rows = []
    for di, dom in enumerate(domains, 1):
        domain_id = dom["domain_id"]
        domain_name = dom["domain_name"]

        vars_ = match_vars(fetch_vars(domain_id))
        if not vars_:
            print(f"  [{di}/{len(domains)}] {domain_name}: tidak ada var cocok")
            continue

        for v in vars_:
            var_id = v["var_id"]
            vtitle = v["title"]
            unit = v.get("unit", "")
            for th, year in BPS_YEARS.items():
                try:
                    j = fetch_data(domain_id, var_id, th)
                except Exception:
                    continue
                dc = j.get("datacontent") or {}
                if not dc:
                    continue
                # label vervar (kabupaten/kota + provinsi)
                vervar = {str(x["val"]): x["label"]
                          for x in j.get("vervar", [])}
                # kunci = vervar + var + turvar + th (string)
                for key, val in dc.items():
                    # vervar = 4 digit pertama
                    kode = key[:4]
                    nama = vervar.get(kode)
                    if nama is None:
                        continue
                    # PENTING: BPS memakai dua konvensi utk wilayah provinsi:
                    #   *99 (mis. 1199 PROVINSI ACEH) DAN *00 (mis. 3200).
                    # Kabupaten/kota = kode lain (mis. 1101, 1171).
                    is_prov = kode.endswith("99") or kode.endswith("00")
                    level = "provinsi" if is_prov else "kabupaten"
                    rows.append({
                        "domain_id": domain_id,
                        "domain_name": domain_name,
                        "var_id": var_id,
                        "variable": vtitle,
                        "unit": unit,
                        "wilayah_kode": kode,
                        "wilayah_nama": nama,
                        "year": year,
                        "value": val,
                        "level": level,
                    })
        print(f"  [{di}/{len(domains)}] {domain_name}: "
              f"{len([r for r in rows if r['domain_id']==domain_id])} baris")

    df = pd.DataFrame(rows)
    df.to_parquet(STAGING / "bps_indicators.parquet", index=False)
    meta = {
        "rows": int(len(df)),
        "domains": len(domains),
        "years": list(BPS_YEARS.values()),
        "levels": df["level"].value_counts().to_dict() if len(df) else {},
        "variables": df["variable"].nunique() if len(df) else 0,
        "duration_sec": round(time.time() - t0, 1),
    }
    (STAGING / "_bps_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[bps] selesai: {len(df)} baris dalam {meta['duration_sec']}s")
    print(f"[bps] level: {meta['levels']}")


if __name__ == "__main__":
    main()
