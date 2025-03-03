"""sqlite3 vuelos.db
.tables
SELECT * FROM Usuarios;
SELECT * FROM Vuelos;
.exit
.exit
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect("vuelos.db")

# Cargar datos de la base de datos en DataFrames
usuarios_df = pd.read_sql_query("SELECT * FROM Usuarios", conn)
vuelos_df = pd.read_sql_query("SELECT * FROM Vuelos", conn)
usuarios_vuelos_df = pd.read_sql_query("SELECT * FROM Usuarios_Vuelos", conn)

# Guardar en CSV
usuarios_df.to_csv("usuarios.csv", index=False)
vuelos_df.to_csv("vuelos.csv", index=False)
usuarios_vuelos_df.to_csv("usuarios_vuelos.csv", index=False)

conn.close()

print("Datos exportados a usuarios.csv y vuelos.csv 📂")
