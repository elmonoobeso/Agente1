"""Fase 1: lee el esquema REAL de la base y lo guarda en sql/01_schema.sql.

Solo usa consultas de lectura de metadatos (SHOW TABLES, SHOW CREATE TABLE,
COUNT(*)). También compara el número de filas con el documento de traspaso,
porque si no coincide "manda la base de datos" y hay que avisar.
"""
from __future__ import annotations

import re
from datetime import datetime

from .comun import RAIZ, conectar

# Volúmenes según CONTEXTO_AGENTES_SPD.md (medico: "pocos", no se compara)
FILAS_ESPERADAS = {
    "medicamento": 27,
    "paciente": 16,
    "test_adherencia": 82,
    "prescription": 95,
    "spd": 125,
    "spd_linea": 729,
}


def volcar_esquema() -> None:
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT DATABASE()")
    base = cur.fetchone()[0]

    # Solo tablas base (no vistas)
    cur.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
    tablas = [fila[0] for fila in cur.fetchall()]

    partes = [
        f"-- Esquema REAL de `{base}`, leído con SHOW CREATE TABLE",
        f"-- Generado: {datetime.now():%Y-%m-%d %H:%M} por `python -m agentes esquema`",
        "-- No editar a mano: regenerar si cambia la base.",
        "",
    ]
    print(f"Base: {base}\n")
    for t in tablas:
        cur.execute(f"SHOW CREATE TABLE `{t}`")
        ddl = cur.fetchone()[1]
        ddl = re.sub(r" AUTO_INCREMENT=\d+", "", ddl)  # el contador cambia con los datos
        partes += [ddl + ";", ""]

        cur.execute(f"SELECT COUNT(*) FROM `{t}`")
        n = cur.fetchone()[0]
        esperado = FILAS_ESPERADAS.get(t)
        marca = "" if esperado in (None, n) else f"  <-- el documento dice {esperado}"
        print(f"{t:<18}{n:>6} filas{marca}")

        cur.execute(f"DESCRIBE `{t}`")
        for campo, tipo, nulo, clave, defecto, _extra in cur.fetchall():
            tipo = tipo.decode() if isinstance(tipo, bytes) else tipo
            print(f"    {campo:<30}{tipo:<16}{'NULL' if nulo == 'YES' else 'NOT NULL':<10}{clave}")
        print()

    faltan = set(FILAS_ESPERADAS) - set(tablas)
    if faltan:
        print("AVISO: faltan tablas del documento:", ", ".join(sorted(faltan)))

    destino = RAIZ / "sql" / "01_schema.sql"
    destino.write_text("\n".join(partes), encoding="utf-8")
    print(f"Guardado en {destino}")
    cur.close()
    con.close()
