"""Punto de entrada: python -m agentes <orden>

Todo se ejecuta solo cuando el usuario lo lanza: nada corre en segundo plano.
"""
from __future__ import annotations

import argparse
import sys

from .comun import ConexionNoSegura, conectar


def cmd_conexion(_args) -> int:
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT CURRENT_USER(), DATABASE(), @@transaction_read_only")
    usuario, base, solo_lectura = cur.fetchone()
    print(f"Conectado como {usuario} a {base}. Permisos: solo SELECT. Sesión READ ONLY: {bool(solo_lectura)}")
    con.close()
    return 0


def cmd_esquema(_args) -> int:
    from .esquema import volcar_esquema
    volcar_esquema()
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m agentes")
    sub = p.add_subparsers(dest="orden", required=True)
    sub.add_parser("conexion", help="Comprueba la conexión de solo lectura").set_defaults(func=cmd_conexion)
    sub.add_parser("esquema", help="Guarda el esquema real en sql/01_schema.sql").set_defaults(func=cmd_esquema)
    # Próximas fases: verificar (A), lote (B), semanal (C), todo (organizador)
    args = p.parse_args(argv)
    try:
        return args.func(args)
    except ConexionNoSegura as e:
        print(f"ABORTADO (nodo O2): {e}", file=sys.stderr)
        return 2
    except KeyError as e:
        print(f"Falta la variable {e} en .env (copia .env.example)", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
