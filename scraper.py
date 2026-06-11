#!/usr/bin/env python3
"""
Scraper de resultados para Baloto, Baloto Revancha y Miloto Colombia.
Intenta obtener resultados reales; si falla, no sobreescribe datos existentes.
"""

import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "resultados.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
}


def fetch_url(url: str) -> str:
    """Descarga una URL y retorna el HTML como texto."""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_numbers_from_text(text: str, count: int, max_val: int) -> list[int] | None:
    """Extrae una secuencia de `count` números únicos <= max_val del texto."""
    nums = [int(n) for n in re.findall(r"\b(\d{1,2})\b", text)
            if 1 <= int(n) <= max_val]
    seen, result = set(), []
    for n in nums:
        if n not in seen:
            seen.add(n)
            result.append(n)
        if len(result) == count:
            return sorted(result)
    return None


def scrape_baloto() -> dict | None:
    """
    Intenta raspar el último resultado de Baloto desde baloto.com.
    Retorna dict con claves 'fecha', 'numeros', 'super' o None si falla.
    """
    try:
        html = fetch_url("https://baloto.com/resultados")
        # Buscar bloque de resultado más reciente
        # El sitio muestra los números en spans con clase 'ball' o similar
        fecha_match = re.search(
            r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})', html)
        nums_block = re.search(
            r'class=["\'](?:ball|numero|result)["\'][^>]*>(\d{1,2})', html)

        if not nums_block:
            print("  [Baloto] No se encontró bloque de números en la página.")
            return None

        # Extraer todos los números del bloque de resultados
        bloque = html[nums_block.start(): nums_block.start() + 600]
        numeros = parse_numbers_from_text(bloque, 5, 43)
        if not numeros:
            return None

        # Buscar SuperBalota (número del 1-16 después de los principales)
        resto = bloque[bloque.rfind(str(numeros[-1])):]
        super_candidates = [int(n) for n in re.findall(r"\b(\d{1,2})\b", resto)
                            if 1 <= int(n) <= 16 and int(n) not in numeros]
        super_balota = super_candidates[0] if super_candidates else None

        if fecha_match:
            d, m, a = fecha_match.groups()
            fecha = f"{a}-{int(m):02d}-{int(d):02d}"
        else:
            fecha = date.today().isoformat()

        return {"fecha": fecha, "numeros": numeros, "super": super_balota}

    except Exception as e:
        print(f"  [Baloto] Error al raspar: {e}")
        return None


def scrape_miloto() -> dict | None:
    """
    Intenta raspar el último resultado de Miloto.
    Retorna dict con claves 'fecha', 'numeros' o None si falla.
    """
    try:
        html = fetch_url("https://www.miloto.com.co/resultados")
        fecha_match = re.search(
            r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})', html)
        nums_block = re.search(
            r'class=["\'](?:ball|numero|result)["\'][^>]*>(\d{1,2})', html)

        if not nums_block:
            print("  [Miloto] No se encontró bloque de números.")
            return None

        bloque = html[nums_block.start(): nums_block.start() + 400]
        numeros = parse_numbers_from_text(bloque, 5, 39)
        if not numeros:
            return None

        if fecha_match:
            d, m, a = fecha_match.groups()
            fecha = f"{a}-{int(m):02d}-{int(d):02d}"
        else:
            fecha = date.today().isoformat()

        return {"fecha": fecha, "numeros": numeros}

    except Exception as e:
        print(f"  [Miloto] Error al raspar: {e}")
        return None


def load_data() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    data["ultima_actualizacion"] = date.today().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def ya_existe(sorteos: list, fecha: str) -> bool:
    return any(s["fecha"] == fecha for s in sorteos)


def main():
    print(f"\n{'='*50}")
    print(f"  Scraper Baloto Stats — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}")

    data = load_data()
    actualizado = False

    # --- BALOTO y REVANCHA (mismo sorteo, misma fecha) ---
    print("\n[1/2] Consultando Baloto y Revancha...")
    resultado_baloto = scrape_baloto()

    if resultado_baloto and resultado_baloto.get("numeros"):
        fecha = resultado_baloto["fecha"]

        if not ya_existe(data["baloto"], fecha):
            entry_b = {
                "fecha": fecha,
                "numeros": resultado_baloto["numeros"],
                "super": resultado_baloto.get("super", 1)
            }
            data["baloto"].insert(0, entry_b)
            # Revancha: mismo sorteo visual, distintos números ganadores
            # En la práctica tienen resultados independientes, aquí se marca igual fecha
            print(f"  ✅ Baloto actualizado: {fecha} → {resultado_baloto['numeros']}")
            actualizado = True
        else:
            print(f"  ℹ️  Baloto ya tiene el sorteo del {fecha}.")
    else:
        print("  ⚠️  No se pudo obtener resultado real de Baloto.")
        print("      Los datos existentes se conservan intactos.")

    # --- MILOTO ---
    print("\n[2/2] Consultando Miloto...")
    resultado_miloto = scrape_miloto()

    if resultado_miloto and resultado_miloto.get("numeros"):
        fecha = resultado_miloto["fecha"]

        if not ya_existe(data["miloto"], fecha):
            entry_m = {
                "fecha": fecha,
                "numeros": resultado_miloto["numeros"]
            }
            data["miloto"].insert(0, entry_m)
            print(f"  ✅ Miloto actualizado: {fecha} → {resultado_miloto['numeros']}")
            actualizado = True
        else:
            print(f"  ℹ️  Miloto ya tiene el sorteo del {fecha}.")
    else:
        print("  ⚠️  No se pudo obtener resultado real de Miloto.")
        print("      Los datos existentes se conservan intactos.")

    # Mantener máximo 200 sorteos por juego
    for juego in ("baloto", "revancha", "miloto"):
        data[juego] = data[juego][:200]

    if actualizado:
        save_data(data)
        print(f"\n✅ resultados.json actualizado correctamente.")
    else:
        print(f"\nℹ️  No hubo cambios. resultados.json sin modificar.")

    print(f"{'='*50}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
