-- =====================================================================
-- 00_usuarios.sql  ·  Lo ejecuta Miguel UNA vez, conectado como root.
--   & "C:\Program Files\MySQL\MySQL Server 26.10\bin\mysql.exe" -u root -p
--   mysql> SOURCE C:/Users/migue/Desktop/Agente1/agente.BD/sql/00_usuarios.sql
-- Antes, cambia las dos contraseñas de abajo y cópialas a .env.
-- =====================================================================

-- 1) Usuario de los agentes: SOLO puede leer (SELECT).
--    Por qué: es la línea roja nº 1. Aunque el código tuviera un fallo,
--    MySQL rechazaría cualquier UPDATE/DELETE/INSERT. La seguridad no
--    depende de que el programa "se porte bien", sino del servidor.
--    '@localhost' = solo puede conectarse desde este ordenador.
CREATE USER IF NOT EXISTS 'agente_spd'@'localhost' IDENTIFIED BY 'CAMBIA_ESTA_CONTRASENA_1';
GRANT SELECT ON spd_trazabilidad.*      TO 'agente_spd'@'localhost';

-- 2) Base de pruebas separada (casos sembrados para cada rama de cada nodo).
--    Los agentes también la leen solo con SELECT.
CREATE DATABASE IF NOT EXISTS spd_trazabilidad_test
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
GRANT SELECT ON spd_trazabilidad_test.* TO 'agente_spd'@'localhost';

-- 3) Usuario que prepara los datos de prueba: puede escribir, pero
--    ÚNICAMENTE en spd_trazabilidad_test. No tiene ningún permiso
--    sobre la base principal.
CREATE USER IF NOT EXISTS 'spd_test_admin'@'localhost' IDENTIFIED BY 'CAMBIA_ESTA_CONTRASENA_2';
GRANT ALL PRIVILEGES ON spd_trazabilidad_test.* TO 'spd_test_admin'@'localhost';

-- Comprobación: debe salir solo USAGE + SELECT en las dos bases.
SHOW GRANTS FOR 'agente_spd'@'localhost';
