"""El cerrojo de solo lectura (nodo O2) se prueba sin base de datos, con una conexión falsa."""
import pytest

from agentes.comun import ConexionNoSegura, comprobar_solo_lectura


class _Cursor:
    def __init__(self, filas):
        self._filas = filas
    def execute(self, _sql):
        pass
    def fetchall(self):
        return [(f,) for f in self._filas]
    def close(self):
        pass


class _Con:
    def __init__(self, filas):
        self._filas = filas
    def cursor(self):
        return _Cursor(self._filas)


def test_acepta_solo_select():
    comprobar_solo_lectura(_Con([
        "GRANT USAGE ON *.* TO `agente_spd`@`localhost`",
        "GRANT SELECT ON `spd_trazabilidad`.* TO `agente_spd`@`localhost`",
    ]))


@pytest.mark.parametrize("linea", [
    "GRANT SELECT, UPDATE ON `spd_trazabilidad`.* TO `x`@`localhost`",
    "GRANT ALL PRIVILEGES ON *.* TO `root`@`localhost` WITH GRANT OPTION",
    "GRANT `rol_admin`@`%` TO `x`@`localhost`",  # roles: no se interpretan -> se rechaza
])
def test_rechaza_cualquier_otro_permiso(linea):
    with pytest.raises(ConexionNoSegura):
        comprobar_solo_lectura(_Con([linea]))
