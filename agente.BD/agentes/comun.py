"""Piezas compartidas por todos los agentes.

- Conexión a MySQL que SOLO acepta un usuario de solo lectura (nodo O2).
- Códigos de resultado comunes y su prioridad.
- Carga de umbrales desde config/umbrales.yaml.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import mysql.connector
import yaml
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

# --- Códigos de resultado -------------------------------------------------
ROJO = "ROJO"                      # bloqueo
AMBAR = "AMBAR"                    # revisar
NO_COMPROBABLE = "NO_COMPROBABLE"  # falta un dato: nunca se da por bueno
VERDE = "VERDE"                    # apto (aun así decide y firma el farmacéutico)
LISTA = "LISTA"                    # lista de trabajo / ruta

# Orden para "lo más grave primero"
PRIORIDAD = {ROJO: 0, AMBAR: 1, NO_COMPROBABLE: 2, LISTA: 3, VERDE: 4}

ETIQUETA = "Propuesta, no decisión. Decide y firma el farmacéutico."

# Privilegios que admitimos en el usuario de los agentes. Cualquier otro
# (INSERT, UPDATE, DELETE, ALL, roles...) hace que el programa se niegue a seguir.
PRIVILEGIOS_PERMITIDOS = {"USAGE", "SELECT"}


class ConexionNoSegura(RuntimeError):
    """El usuario de MySQL tiene más permisos que SELECT."""


def comprobar_solo_lectura(con) -> list[str]:
    """Lee SHOW GRANTS del usuario conectado y falla si puede escribir.

    Falla "cerrado": si aparece una línea que no sabemos interpretar,
    también se rechaza.
    """
    cur = con.cursor()
    cur.execute("SHOW GRANTS FOR CURRENT_USER()")
    lineas = [fila[0] for fila in cur.fetchall()]
    cur.close()
    for linea in lineas:
        m = re.match(r"GRANT (.+?) ON ", linea)
        if not m:
            raise ConexionNoSegura(f"Permiso no reconocido: {linea}")
        privilegios = {p.strip().upper() for p in m.group(1).split(",")}
        if not privilegios <= PRIVILEGIOS_PERMITIDOS:
            raise ConexionNoSegura(
                f"El usuario tiene permisos de escritura ({', '.join(sorted(privilegios))}). "
                "Los agentes solo pueden usar un usuario con SELECT."
            )
    return lineas


def conectar(base: str | None = None):
    """Abre una conexión de solo lectura (doble cerrojo: permisos + sesión READ ONLY)."""
    con = mysql.connector.connect(
        host=os.getenv("SPD_DB_HOST", "localhost"),
        port=int(os.getenv("SPD_DB_PORT", "3306")),
        user=os.environ["SPD_DB_USER"],
        password=os.environ["SPD_DB_PASSWORD"],
        database=base or os.getenv("SPD_DB_NAME", "spd_trazabilidad"),
    )
    try:
        comprobar_solo_lectura(con)
        cur = con.cursor()
        cur.execute("SET SESSION TRANSACTION READ ONLY")
        cur.close()
    except Exception:
        con.close()
        raise
    return con


def cargar_umbrales() -> dict:
    with open(RAIZ / "config" / "umbrales.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)
