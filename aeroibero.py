import sys
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import datetime  # Para las validaciones de fecha
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ---------------------------
# 1. CREACIÓN DEL GRAFO
# ---------------------------
nodos = {
    "La Comarca": {"país": "Tierra Media", "aeropuerto": "Bilbo Bolsón", "tipo": "Ordinaria"},
    "Rivendel": {"país": "Tierra Media", "aeropuerto": "Altos Elfos", "tipo": "Importante"},
    "Rohan": {"país": "Tierra Media", "aeropuerto": "Caballo Verde", "tipo": "Ordinaria"},
    "Reino del Bosque": {"país": "Tierra Media", "aeropuerto": "Elfos Silvanos", "tipo": "Ordinaria"},
    "Erebor": {"país": "Tierra Media", "aeropuerto": "Durin", "tipo": "Ordinaria"},
    "Gondor": {"país": "Tierra Media", "aeropuerto": "Isildur", "tipo": "Capital"},
    "Moria": {"país": "Tierra Media", "aeropuerto": "Khazad Dum", "tipo": "Ordinaria"},
    "Isengard": {"país": "Tierra Media", "aeropuerto": "Mago Blanco", "tipo": "Ordinaria"},
    "Mordor": {"país": "Tierra Media", "aeropuerto": "Ojo de Sauron", "tipo": "Importante"},
    "Narnia": {"país": "Narnia", "aeropuerto": "León Real", "tipo": "Capital"},
    "Telmar": {"país": "Narnia", "aeropuerto": "Príncipe Caspian", "tipo": "Importante"},
    "Charn": {"país": "Narnia", "aeropuerto": "Bruja Blanca", "tipo": "Importante"},
    "Ciudad Esmeralda": {"país": "Oz", "aeropuerto": "Mago de Oz", "tipo": "Capital"},
    "Winkie": {"país": "Oz", "aeropuerto": "Bruja del Oeste", "tipo": "Importante"},
    "Munchkin": {"país": "Oz", "aeropuerto": "Dorita", "tipo": "Ordinaria"},
}

# Definir las aristas (rutas) con sus atributos
aristas = [
    {"origen": "La Comarca", "destino": "Rivendel", "tipo": "N", "distancia": 500.00, "tiempo": 1.5, "costo": 1550.00},
    {"origen": "Rivendel", "destino": "La Comarca", "tipo": "N", "distancia": 500.00, "tiempo": 1.5, "costo": 1850.00},
    {"origen": "Rivendel", "destino": "Reino del Bosque", "tipo": "N", "distancia": 950.00, "tiempo": 2.4, "costo": 2400.00},
    {"origen": "Rivendel", "destino": "Rohan", "tipo": "N", "distancia": 550.00, "tiempo": 1.6, "costo": 1975.00},
    {"origen": "Rivendel", "destino": "Telmar", "tipo": "I", "distancia": 1100.00, "tiempo": 5.2, "costo": 3750.00},
    {"origen": "Rohan", "destino": "Rivendel", "tipo": "N", "distancia": 550.00, "tiempo": 1.6, "costo": 1675.00},
    {"origen": "Rohan", "destino": "Isengard", "tipo": "N", "distancia": 400.00, "tiempo": 1.3, "costo": 1300.00},
    {"origen": "Rohan", "destino": "Gondor", "tipo": "N", "distancia": 600.00, "tiempo": 1.7, "costo": 1550.00},
    {"origen": "Gondor", "destino": "Rohan", "tipo": "N", "distancia": 600.00, "tiempo": 1.7, "costo": 2350.00},
    {"origen": "Gondor", "destino": "Erebor", "tipo": "N", "distancia": 1250.00, "tiempo": 3.0, "costo": 4225.00},
    {"origen": "Gondor", "destino": "Mordor", "tipo": "N", "distancia": 450.00, "tiempo": 3.4, "costo": 3125.00},
    {"origen": "Gondor", "destino": "Narnia", "tipo": "I", "distancia": 550.00, "tiempo": 4.1, "costo": 1975.00},
    {"origen": "Gondor", "destino": "Ciudad Esmeralda", "tipo": "I", "distancia": 1100.00, "tiempo": 5.2, "costo": 4250.00},
    {"origen": "Mordor", "destino": "Isengard", "tipo": "N", "distancia": 550.00, "tiempo": 1.6, "costo": 1375.00},
    {"origen": "Mordor", "destino": "Winkie", "tipo": "I", "distancia": 600.00, "tiempo": 3.2, "costo": 1500.00},
    {"origen": "Isengard", "destino": "Rohan", "tipo": "N", "distancia": 400.00, "tiempo": 1.3, "costo": 1300.00},
    {"origen": "Isengard", "destino": "Moria", "tipo": "N", "distancia": 400.00, "tiempo": 1.3, "costo": 1100.00},
    {"origen": "Moria", "destino": "Isengard", "tipo": "N", "distancia": 400.00, "tiempo": 1.3, "costo": 1300.00},
    {"origen": "Moria", "destino": "Erebor", "tipo": "N", "distancia": 900.00, "tiempo": 2.3, "costo": 2225.00},
    {"origen": "Erebor", "destino": "Moria", "tipo": "N", "distancia": 900.00, "tiempo": 2.3, "costo": 2000.00},
    {"origen": "Erebor", "destino": "Gondor", "tipo": "N", "distancia": 1250.00, "tiempo": 3.0, "costo": 3525.00},
    {"origen": "Reino del Bosque", "destino": "Erebor", "tipo": "N", "distancia": 500.00, "tiempo": 4.5, "costo": 2450.00},
    {"origen": "Reino del Bosque", "destino": "Rivendel", "tipo": "N", "distancia": 950.00, "tiempo": 2.4, "costo": 2100.00},
    {"origen": "Narnia", "destino": "Telmar", "tipo": "N", "distancia": 400.00, "tiempo": 1.3, "costo": 1800.00},
    {"origen": "Narnia", "destino": "Charn", "tipo": "N", "distancia": 450.00, "tiempo": 3.4, "costo": 3125.00},
    {"origen": "Narnia", "destino": "Gondor", "tipo": "I", "distancia": 550.00, "tiempo": 4.1, "costo": 2875.00},
    {"origen": "Narnia", "destino": "Ciudad Esmeralda", "tipo": "I", "distancia": 1300.00, "tiempo": 5.6, "costo": 4750.00},
    {"origen": "Telmar", "destino": "Narnia", "tipo": "N", "distancia": 400.00, "tiempo": 1.3, "costo": 1500.00},
    {"origen": "Telmar", "destino": "Rivendel", "tipo": "I", "distancia": 1100.00, "tiempo": 5.2, "costo": 3750.00},
    {"origen": "Charn", "destino": "Narnia", "tipo": "N", "distancia": 450.00, "tiempo": 3.4, "costo": 1225.00},
    {"origen": "Charn", "destino": "Winkie", "tipo": "I", "distancia": 700.00, "tiempo": 3.4, "costo": 875.00},
    {"origen": "Ciudad Esmeralda", "destino": "Munchkin", "tipo": "N", "distancia": 200.00, "tiempo": 3.4, "costo": 875.00},
    {"origen": "Ciudad Esmeralda", "destino": "Winkie", "tipo": "N", "distancia": 300.00, "tiempo": 3.1, "costo": 2250.00},
    {"origen": "Ciudad Esmeralda", "destino": "Gondor", "tipo": "I", "distancia": 1100.00, "tiempo": 5.2, "costo": 4250.00},
    {"origen": "Ciudad Esmeralda", "destino": "Narnia", "tipo": "I", "distancia": 1300.00, "tiempo": 5.6, "costo": 4750.00},
    {"origen": "Winkie", "destino": "Mordor", "tipo": "I", "distancia": 600.00, "tiempo": 3.2, "costo": 750.00},
    {"origen": "Winkie", "destino": "Charn", "tipo": "I", "distancia": 700.00, "tiempo": 3.4, "costo": 875.00},
]



grafo = nx.DiGraph()
for ciudad, atributos in nodos.items():
    grafo.add_node(ciudad, **atributos)
for ruta in aristas:
    origen, destino = ruta["origen"], ruta["destino"]
    grafo.add_edge(origen, destino, **ruta)

for origen, destino in list(grafo.edges()):
    if grafo.has_edge(destino, origen):
        grafo[origen][destino]["flecha"] = "doble"
        grafo[destino][origen]["flecha"] = "doble"

colores_nodos = {'Capital': 'gold', 'Importante': 'skyblue', 'Ordinaria': 'lightgreen'}
tamaños_nodos = {'Capital': 1000, 'Importante': 700, 'Ordinaria': 500}
pos = nx.spring_layout(grafo, seed=42)

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('#1e1e1e')
ax.set_facecolor('#1e1e1e')

for tipo, color in colores_nodos.items():
    nodos_tipo = [nodo for nodo, datos in grafo.nodes(data=True) if datos['tipo'] == tipo]
    nx.draw_networkx_nodes(grafo, pos, nodelist=nodos_tipo,
                           node_color=color,
                           node_size=[tamaños_nodos[tipo]] * len(nodos_tipo),
                           alpha=0.8, ax=ax)
nx.draw_networkx_labels(grafo, pos, font_size=10, font_color='white', ax=ax)

dibujadas = set()
for origen, destino, datos in grafo.edges(data=True):
    if (origen, destino) in dibujadas or (destino, origen) in dibujadas:
        continue
    if "flecha" in datos and datos["flecha"] == "doble":
        nx.draw_networkx_edges(grafo, pos, edgelist=[(origen, destino)],
                               arrowstyle='-|>', arrowsize=20,
                               connectionstyle='arc3,rad=0.1', edge_color='white', alpha=0.6, ax=ax)
        nx.draw_networkx_edges(grafo, pos, edgelist=[(destino, origen)],
                               arrowstyle='-|>', arrowsize=20,
                               connectionstyle='arc3,rad=0.1', edge_color='white', alpha=0.6, ax=ax)
    else:
        nx.draw_networkx_edges(grafo, pos, edgelist=[(origen, destino)],
                               arrowstyle='-|>', arrowsize=20,
                               connectionstyle='arc3,rad=0.1', edge_color='white', alpha=0.6, ax=ax)
    dibujadas.add((origen, destino))

ax.set_title("✈ Mapa de Rutas entre Ciudades de Mundos Fantásticos ✈", fontsize=14, color='white')
ax.axis('off')

# ---------------------------
# 2. INTERFAZ TKINTER
# ---------------------------
root = tk.Tk()
root.title("Sistema de Registro de Vuelos")
root.state("zoomed")

def on_closing():
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

frame_izquierda = tk.Frame(root, width=800)
frame_izquierda.grid(row=0, column=0, sticky="nsew")
frame_derecha = tk.Frame(root)
frame_derecha.grid(row=0, column=1, sticky="nsew")
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

canvas_grafo = FigureCanvasTkAgg(fig, master=frame_izquierda)
canvas_grafo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_grafo.draw()

toolbar = NavigationToolbar2Tk(canvas_grafo, frame_izquierda)
toolbar.update()
canvas_grafo.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ---------------------------
# 3. BASE DE DATOS: NUEVA ESTRUCTURA
# ---------------------------
def conectar_bd():
    conn = sqlite3.connect("vuelos.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pasaporte TEXT UNIQUE,
        nombre TEXT NOT NULL,
        ap_paterno TEXT NOT NULL,
        ap_materno TEXT NOT NULL,
        fecha_nacimiento DATE NOT NULL,
        nacionalidad TEXT NOT NULL,
        raza TEXT NOT NULL,
        telefono TEXT NOT NULL,
        correo TEXT NOT NULL
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vuelos (
        vuelo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        origen TEXT NOT NULL,
        destino TEXT NOT NULL,
        fecha DATE NOT NULL,
        ruta TEXT NOT NULL,
        distancia_total REAL NOT NULL,
        tiempo_total REAL NOT NULL,
        costo_total REAL NOT NULL,
        capacidad INTEGER NOT NULL,
        ocupacion INTEGER NOT NULL DEFAULT 0,
        UNIQUE(origen, destino, fecha, ruta)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuarios_Vuelos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    vuelo_id INTEGER NOT NULL,
    asiento TEXT,
    UNIQUE(vuelo_id, asiento),
    UNIQUE(usuario_id, vuelo_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
    FOREIGN KEY (vuelo_id) REFERENCES Vuelos(vuelo_id)
    )''')
    
    conn.commit()
    return conn, cursor

# Función para insertar o recuperar un usuario (se usa pasaporte para evitar duplicados)
def insertar_usuario(cursor, conn, pasaporte, nombre, ap_paterno, ap_materno, fecha_nacimiento, nacionalidad, raza, telefono, correo):
    cursor.execute("SELECT id FROM Usuarios WHERE pasaporte=?", (pasaporte,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute('''
        INSERT INTO Usuarios (pasaporte, nombre, ap_paterno, ap_materno, fecha_nacimiento, nacionalidad, raza, telefono, correo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (pasaporte, nombre, ap_paterno, ap_materno, fecha_nacimiento, nacionalidad, raza, telefono, correo))
        conn.commit()
        return cursor.lastrowid
def obtener_asientos_reservados(vuelo_id):
    cursor.execute("SELECT asiento FROM Usuarios_Vuelos WHERE vuelo_id = ? AND asiento IS NOT NULL", (vuelo_id,))
    return [row[0] for row in cursor.fetchall()]

def obtener_vuelo_existente(cursor, origen, destino, fecha, ruta_str):
    cursor.execute("SELECT vuelo_id, ocupacion, capacidad FROM Vuelos WHERE origen=? AND destino=? AND fecha=? AND ruta=?", 
                   (origen, destino, fecha, ruta_str))
    return cursor.fetchone()

def insertar_vuelo_grupal(cursor, conn, origen, destino, fecha, ruta_seleccionada, distancia_total, tiempo_total, costo_total, capacidad):
    ruta_str = ",".join(ruta_seleccionada)
    cursor.execute('''
    INSERT INTO Vuelos (origen, destino, fecha, ruta, distancia_total, tiempo_total, costo_total, capacidad, ocupacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)''', (origen, destino, fecha, ruta_str, distancia_total, tiempo_total, costo_total, capacidad))
    conn.commit()
    return cursor.lastrowid

def actualizar_ocupacion(cursor, conn, vuelo_id, incremento):
    cursor.execute("UPDATE Vuelos SET ocupacion = ocupacion + ? WHERE vuelo_id=?", (incremento, vuelo_id))
    conn.commit()

def asociar_usuario_vuelo(cursor, conn, usuario_id, vuelo_id, asiento):
    try:
        cursor.execute("INSERT INTO Usuarios_Vuelos (usuario_id, vuelo_id, asiento) VALUES (?, ?, ?)", (usuario_id, vuelo_id, asiento))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

def obtener_capacidad_por_ruta(ruta):
    if any(grafo[u][v]['tipo'] == 'I' for u, v in zip(ruta[:-1], ruta[1:])):
        return 30
    elif len(ruta) > 3:
        return 25
    else:
        return 20

def calcular_ruta(ruta):
    distancia_total = sum(grafo[u][v]['distancia'] for u, v in zip(ruta[:-1], ruta[1:]))
    tiempo_total = sum(grafo[u][v]['tiempo'] for u, v in zip(ruta[:-1], ruta[1:]))
    costo_total = sum(grafo[u][v]['costo'] for u, v in zip(ruta[:-1], ruta[1:]))
    return distancia_total, tiempo_total, costo_total

# ---------------------------
# SELECCIÓN DE ASIENTOS
# ---------------------------
def seleccionar_asientos(num_asientos, vuelo_id):
    seat_window = tk.Toplevel(root)
    seat_window.title("Selección de Asientos")
    rows = 5
    cols = 6
    selected_seats = []
    
    # Consultar asientos reservados en la base de datos para este vuelo
    reserved_seats = obtener_asientos_reservados(vuelo_id)
    
    def toggle_seat(row, col, btn):
        seat_id = f"{chr(65+row)}{col+1}"
        # Si el asiento ya está reservado en la DB, no se permite seleccionar
        if seat_id in reserved_seats:
            messagebox.showinfo("Información", f"El asiento {seat_id} ya está ocupado.")
            return
        if seat_id in selected_seats:
            selected_seats.remove(seat_id)
            btn.config(bg="green", text=f"🛫 {seat_id}")  # Emoji de avión para asientos disponibles
        else:
            if len(selected_seats) >= num_asientos:
                messagebox.showwarning("Límite alcanzado", f"Solo puedes seleccionar {num_asientos} asientos.")
            else:
                selected_seats.append(seat_id)
                btn.config(bg="yellow", text=f"✅ {seat_id}")  # Emoji de check para asientos seleccionados
        print("Asientos seleccionados:", selected_seats)
    
    # Crear la grilla de asientos
    for i in range(rows):
        for j in range(cols):
            seat_id = f"{chr(65+i)}{j+1}"
            btn = tk.Button(seat_window, text=f"🛫 {seat_id}", width=4)
            
            # Si el asiento ya está reservado, se marca en rojo, se deshabilita y se agrega un sticker
            if seat_id in reserved_seats:
                btn.config(bg="red", state="disabled", text=f"❌ {seat_id}")  # Emoji de cruz para ocupado
            else:
                btn.config(bg="green", command=lambda btn=btn, row=i, col=j: toggle_seat(row, col, btn))
            
            btn.grid(row=i, column=j, padx=5, pady=5)
    
    def guardar_asientos():
        if len(selected_seats) != num_asientos:
            messagebox.showwarning("Selección incompleta", f"Debes seleccionar exactamente {num_asientos} asientos.")
            return
        
        # Validación final antes de guardar: reconsultar la base de datos
        actuales = obtener_asientos_reservados(vuelo_id)
        for seat in selected_seats:
            if seat in actuales:
                messagebox.showerror("Error", f"El asiento {seat} ya fue reservado. Por favor, selecciona otro asiento.")
                return
        
        global asientos_seleccionados
        asientos_seleccionados = selected_seats.copy()
        messagebox.showinfo("Asientos seleccionados", f"Has seleccionado: {', '.join(asientos_seleccionados)}")
        seat_window.destroy()
    
    tk.Button(seat_window, text="Guardar Asientos", command=guardar_asientos).grid(row=rows, column=0, columnspan=cols, pady=10)
    seat_window.wait_window()
    
    
    
def confirmar_asientos(vuelo_id, asientos_seleccionados, registered_users):
    # Se asigna cada asiento al usuario correspondiente
    for seat, user_id in zip(asientos_seleccionados, registered_users):
        try:
            cursor.execute("UPDATE Usuarios_Vuelos SET asiento = ? WHERE vuelo_id = ? AND usuario_id = ?", (seat, vuelo_id, user_id))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"El asiento {seat} ya está asignado. Intente nuevamente.")
            return False
    return True


# ---------------------------
# REGISTRO DE USUARIOS
# ---------------------------
registered_users = []
registered_passports = []  # Para evitar duplicados en la sesión

def registrar_usuarios_multiples(total, current=1):
    def guardar_usuario():
        pasaporte = entry_pasaporte.get().strip()
        nombre = entry_nombre.get().strip()
        ap_paterno = entry_ap_paterno.get().strip()
        ap_materno = entry_ap_materno.get().strip()
        fecha_nacimiento = cal_fecha_nacimiento.get_date()
        nacionalidad = combo_nacionalidad.get().strip()
        raza = combo_raza.get().strip()
        telefono = entry_telefono.get().strip()
        correo = entry_correo.get().strip()

        if not pasaporte or not nombre or not ap_paterno or not telefono or not correo:
            messagebox.showwarning("Advertencia", "El pasaporte, nombre, apellido, teléfono y correo son obligatorios.")
            return

        if not pasaporte.isdigit() or len(pasaporte) != 9:
            messagebox.showwarning("Error", "El pasaporte debe tener 9 dígitos numéricos.")
            return

        if pasaporte in registered_passports:
            messagebox.showinfo("Info", f"El usuario con pasaporte {pasaporte} ya está registrado en esta sesión.")
            return

        try:
            fecha_obj = datetime.datetime.strptime(fecha_nacimiento, "%m/%d/%y").date()
        except ValueError:
            messagebox.showwarning("Error", "Formato de fecha incorrecto. Use mm/dd/yy.")
            return

        # Validar que la fecha de nacimiento no sea mayor a hoy ni supere los 150 años
        hoy = datetime.date.today()
        if fecha_obj > hoy:
            messagebox.showwarning("Fecha inválida", "La fecha de nacimiento no puede ser mayor que hoy.")
            return
        if (hoy.year - fecha_obj.year) > 150:
            messagebox.showwarning("Fecha inválida", "La fecha de nacimiento excede el límite permitido.")
            return

        if not telefono.isdigit() or len(telefono) < 10:
            messagebox.showwarning("Error", "El teléfono debe contener al menos 10 dígitos numéricos.")
            return

        if "@" not in correo or "." not in correo.split("@")[-1]:
            messagebox.showwarning("Error", "Ingrese un correo electrónico válido.")
            return

        user_id = insertar_usuario(cursor, conn, pasaporte, nombre, ap_paterno, ap_materno, fecha_nacimiento, nacionalidad, raza, telefono, correo)
        registered_users.append(user_id)
        registered_passports.append(pasaporte)
        messagebox.showinfo("Éxito", f"Usuario {current} registrado correctamente")

        if current < total:
            registrar_usuarios_multiples(total, current + 1)
        else:
            registrar_vuelo_grupal()


    for widget in frame_derecha.winfo_children():
        widget.destroy()
    
    ttk.Label(frame_derecha, text=f"Registro Persona {current} de {total}", font=("Arial", 14)).pack(pady=10)
    
    ttk.Label(frame_derecha, text="Pasaporte:").pack(pady=2)
    entry_pasaporte = ttk.Entry(frame_derecha, width=30)
    entry_pasaporte.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Nombre:").pack(pady=2)
    entry_nombre = ttk.Entry(frame_derecha, width=30)
    entry_nombre.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Apellido Paterno:").pack(pady=2)
    entry_ap_paterno = ttk.Entry(frame_derecha, width=30)
    entry_ap_paterno.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Apellido Materno:").pack(pady=2)
    entry_ap_materno = ttk.Entry(frame_derecha, width=30)
    entry_ap_materno.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Fecha de Nacimiento (mm/dd/yy):").pack(pady=2)
    cal_fecha_nacimiento = Calendar(frame_derecha, selectmode='day', date_pattern="mm/dd/yy")
    cal_fecha_nacimiento.config(maxdate=datetime.date.today())
    cal_fecha_nacimiento.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Nacionalidad:").pack(pady=2)
    combo_nacionalidad = ttk.Combobox(frame_derecha, values=["Mediaterrano", "Narniano", "Ozniano"], state="readonly", width=27)
    combo_nacionalidad.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Raza:").pack(pady=2)
    combo_raza = ttk.Combobox(frame_derecha, values=["Humano", "Elfo", "Enano", "Orco", "Duende", "Mago/Bruja", "Centauro", "Fauno", "Mono Alado", "Otro"], state="readonly", width=27)
    combo_raza.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Teléfono:").pack(pady=2)
    entry_telefono = ttk.Entry(frame_derecha, width=30)
    entry_telefono.pack(pady=5)
    
    ttk.Label(frame_derecha, text="Correo Electrónico:").pack(pady=2)
    entry_correo = ttk.Entry(frame_derecha, width=30)
    entry_correo.pack(pady=5)
    
    ttk.Button(frame_derecha, text="Guardar Usuario ✅", command=guardar_usuario).pack(pady=10)
# ---------------------------
# REGISTRO DE VUELO GRUPAL
# ---------------------------
def registrar_vuelo_grupal():
    def buscar_ruta_grupal():
        origen = combo_origen.get().strip()
        destino = combo_destino.get().strip()
        criterio = combo_prioridad.get().strip()
        if not origen or not destino or not criterio:
            messagebox.showwarning("Advertencia", "Debe seleccionar origen, destino y prioridad.")
            return
        peso = {"Distancia": "distancia", "Tiempo": "tiempo", "Costo": "costo"}[criterio]
        rutas_optimas = list(nx.all_shortest_paths(grafo, source=origen, target=destino, weight=peso))
        rutas_mostrar = rutas_optimas[:3] if len(rutas_optimas) > 3 else rutas_optimas
        for widget in frame_rutas.winfo_children():
            widget.destroy()
        ttk.Label(frame_rutas, text=f"Se encontraron {len(rutas_mostrar)} rutas entre {origen} y {destino} (ordenadas por {criterio.lower()}):").pack(pady=10)
        for i, ruta in enumerate(rutas_mostrar, 1):
            distancia, tiempo, costo = calcular_ruta(ruta)
            ruta_texto = f"Ruta {i}: {ruta}\nDistancia: {distancia}, Tiempo: {tiempo}, Costo: {costo}"
            rb = ttk.Radiobutton(frame_rutas, text=ruta_texto, variable=var_ruta, value=",".join(ruta), command=actualizar_asientos_disponibles)
            rb.pack(anchor="w")
        frame_rutas.pack(pady=10)
        if rutas_mostrar and not var_ruta.get():
            var_ruta.set(",".join(rutas_mostrar[0]))
            actualizar_asientos_disponibles()

    def actualizar_asientos_disponibles():
        if var_ruta.get():
            ruta_seleccionada = var_ruta.get().split(",")
            capacidad = obtener_capacidad_por_ruta(ruta_seleccionada)
            fecha = cal_fecha.get_date()
            vuelo_existente = obtener_vuelo_existente(cursor, combo_origen.get(), combo_destino.get(), fecha, ",".join(ruta_seleccionada))
            if vuelo_existente:
                ocupacion = vuelo_existente[1]
            else:
                ocupacion = 0
            asientos_disponibles = capacidad - ocupacion
            label_asientos.config(text=f"Asientos disponibles: {asientos_disponibles} (Capacidad: {capacidad}, Ocupados: {ocupacion})")

    def guardar_vuelo_reg():
        ruta_str = var_ruta.get()
        fecha = cal_fecha.get_date()
        if not ruta_str:
            messagebox.showwarning("Advertencia", "Debe seleccionar una ruta antes de guardar.")
            return
        ruta_seleccionada = ruta_str.split(",")
        capacidad = obtener_capacidad_por_ruta(ruta_seleccionada)
        distancia_total, tiempo_total, costo_total = calcular_ruta(ruta_seleccionada)
        ruta_str = ",".join(ruta_seleccionada)
        vuelo = obtener_vuelo_existente(cursor, combo_origen.get(), combo_destino.get(), fecha, ruta_str)
        if vuelo:
            vuelo_id, ocupacion, cap_existente = vuelo
            asientos_disponibles = cap_existente - ocupacion
            if len(registered_users) > asientos_disponibles:
                messagebox.showwarning("Advertencia", f"No hay asientos suficientes. Solo quedan {asientos_disponibles} asientos disponibles para esta ruta en la fecha {fecha}.")
                return
            # Inserta las asociaciones si aún no existen, dejando asiento en NULL
            for user_id in registered_users:
                cursor.execute("SELECT id FROM Usuarios_Vuelos WHERE vuelo_id=? AND usuario_id=?", (vuelo_id, user_id))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO Usuarios_Vuelos (usuario_id, vuelo_id, asiento) VALUES (?, ?, ?)", (user_id, vuelo_id, None))
            actualizar_ocupacion(cursor, conn, vuelo_id, len(registered_users))
        else:
            vuelo_id = insertar_vuelo_grupal(cursor, conn, combo_origen.get(), combo_destino.get(), fecha, ruta_seleccionada, distancia_total, tiempo_total, costo_total, capacidad)
            if len(registered_users) > capacidad:
                messagebox.showwarning("Advertencia", f"No hay asientos suficientes. La capacidad es {capacidad} y se requieren {len(registered_users)} asientos.")
                return
            for user_id in registered_users:
                cursor.execute("INSERT INTO Usuarios_Vuelos (usuario_id, vuelo_id, asiento) VALUES (?, ?, ?)", (user_id, vuelo_id, None))
            actualizar_ocupacion(cursor, conn, vuelo_id, len(registered_users))
        
        total_cost = costo_total * len(registered_users)
        
        # Llamar a la selección de asientos (ahora se pasa el vuelo_id)
        seleccionar_asientos(len(registered_users), vuelo_id)
        
        # Una vez seleccionados los asientos, se actualizan en la BDD:
        if confirmar_asientos(vuelo_id, asientos_seleccionados, registered_users):
            messagebox.showinfo("Asientos confirmados", "Los asientos han sido asignados correctamente.")
        else:
            messagebox.showerror("Error", "Hubo un error al asignar los asientos.")
        
        # Mostrar resultados en la interfaz
        for widget in frame_derecha.winfo_children():
            widget.destroy()
        ttk.Label(frame_derecha, text="Resultados del Vuelo", font=("Arial", 16)).pack(pady=10)
        ttk.Label(frame_derecha, text=f"Total a Pagar: ${total_cost:.2f}").pack(pady=5)
        ttk.Label(frame_derecha, text=f"Tiempo de viaje: {tiempo_total} horas").pack(pady=5)
        ttk.Label(frame_derecha, text=f"Distancia total: {distancia_total} km").pack(pady=5)
        ttk.Label(frame_derecha, text=f"Asientos seleccionados: {', '.join(asientos_seleccionados)}").pack(pady=5)
        # Mostrar los pases de abordar para cada usuario
        mostrar_pases_abordar(vuelo_id, registered_users)
        generar_y_mostrar_pdf_pases(vuelo_id, registered_users)

    for widget in frame_derecha.winfo_children():
        widget.destroy()
    
    ttk.Label(frame_derecha, text="Registro de Vuelo para Todos los Usuarios", font=("Arial", 14)).pack(pady=10)
    ttk.Label(frame_derecha, text="Origen:").pack(pady=2)
    combo_origen = ttk.Combobox(frame_derecha, values=ciudades, state="readonly", width=30)
    combo_origen.pack(pady=5)
    ttk.Label(frame_derecha, text="Destino:").pack(pady=2)
    combo_destino = ttk.Combobox(frame_derecha, values=ciudades, state="readonly", width=30)
    combo_destino.pack(pady=5)
    ttk.Label(frame_derecha, text="Fecha:").pack(pady=2)
    cal_fecha = Calendar(frame_derecha, selectmode='day', date_pattern="mm/dd/yy")
    cal_fecha.pack(pady=5)
    ttk.Label(frame_derecha, text="Prioridad:").pack(pady=2)
    combo_prioridad = ttk.Combobox(frame_derecha, values=prioridad, state="readonly", width=30)
    combo_prioridad.pack(pady=5)
    
    ttk.Button(frame_derecha, text="Buscar Ruta", command=buscar_ruta_grupal).pack(pady=10)
    
    frame_rutas = tk.Frame(frame_derecha)
    frame_rutas.pack(pady=10)
    var_ruta = tk.StringVar()
    
    label_asientos = ttk.Label(frame_derecha, text="Asientos disponibles: ")
    label_asientos.pack(pady=5)
    
    ttk.Button(frame_derecha, text="Guardar Vuelo", command=guardar_vuelo_reg).pack(pady=10)
    

# Lista para selección de ciudades y prioridades
ciudades = [
    "La Comarca", "Rivendel", "Rohan", "Reino del Bosque", "Erebor", "Gondor",
    "Moria", "Isengard", "Mordor", "Narnia", "Telmar", "Charn",
    "Ciudad Esmeralda", "Winkie", "Munchkin"
]
prioridad = ["Distancia", "Tiempo", "Costo"]

import random

def asignar_sala_y_puerta(tipo):
    # Para aeropuertos ordinarios se asigna sala y puerta fijas;
    # para Importantes/Capitales se elige entre 3 opciones
    if tipo == "Ordinaria":
        sala = "Sala 1"
        puerta = "Puerta 1"
    else:
        sala = f"Sala {random.choice([1, 2, 3])}"
        puerta = f"Puerta {random.choice([1, 2, 3])}"
    return sala, puerta

def generar_pase_abordar(vuelo_id, usuario_id):
    # Recuperar la información del vuelo
    cursor.execute("SELECT origen, destino, fecha, ruta FROM Vuelos WHERE vuelo_id = ?", (vuelo_id,))
    flight = cursor.fetchone()
    if not flight:
        return None
    origen, destino, fecha, ruta = flight

    # Recuperar la información del usuario
    cursor.execute("SELECT nombre, ap_paterno, ap_materno, fecha_nacimiento, raza, correo FROM Usuarios WHERE id = ?", (usuario_id,))
    user_info = cursor.fetchone()
    if user_info:
        nombre, ap_paterno, ap_materno, fecha_nac, raza, correo = user_info
        full_name = f"{nombre} {ap_paterno} {ap_materno}"
        # Calcular la edad a partir de la fecha de nacimiento (se asume formato "mm/dd/yy")
        try:
            birth_date = datetime.datetime.strptime(fecha_nac, "%m/%d/%y").date()
        except Exception as e:
            birth_date = datetime.date(1900, 1, 1)
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    else:
        full_name = "Desconocido"
        age = "Desconocido"
        raza = "Desconocido"
        correo = "Desconocido"

    # Usar el grafo para obtener la información de los aeropuertos
    origen_info = grafo.nodes[origen]
    destino_info = grafo.nodes[destino]
    aeropuerto_origen = origen_info.get("aeropuerto", "Desconocido")
    aeropuerto_destino = destino_info.get("aeropuerto", "Desconocido")
    tipo_origen = origen_info.get("tipo", "Ordinaria")
    
    # Definir un horario basado en la fecha (por ejemplo, agregando 08:00 AM)
    schedule = f"{fecha} 08:00 AM"
    
    # Identificador fijo para el avión (puedes modificarlo según tus necesidades)
    airplane = "Avión A123"
    
    # Asignar sala de espera y puerta de embarque según el tipo de aeropuerto
    sala, puerta = asignar_sala_y_puerta(tipo_origen)
    
    # Armar el pase de abordar con los datos del vuelo y del usuario
    pase = (
        f"PASE DE ABORDAR\n"
        f"-----------------------------\n"
        f"Nombre: {full_name}\n"
        f"Edad: {age}\n"
        f"Raza: {raza}\n"
        f"Correo: {correo}\n"
        f"Usuario ID: {usuario_id}\n"
        f"Vuelo ID: {vuelo_id}\n"
        f"Origen: {origen} ({aeropuerto_origen})\n"
        f"Destino: {destino} ({aeropuerto_destino})\n"
        f"Fecha y Hora: {schedule}\n"
        f"Avión: {airplane}\n"
        f"Sala de espera: {sala}\n"
        f"Puerta de embarque: {puerta}\n"
        f"Ruta: {ruta}\n"
        f"-----------------------------\n"
    )
    return pase

def mostrar_pases_abordar(vuelo_id, usuarios):
    # Genera un pase para cada usuario y los muestra en una ventana nueva
    pases = []
    for user_id in usuarios:
        pase = generar_pase_abordar(vuelo_id, user_id)
        if pase:
            pases.append(pase)
    
    pase_window = tk.Toplevel(root)
    pase_window.title("Pases de Abordar")
    
    for pase in pases:
        text = tk.Text(pase_window, height=12, width=50)
        text.insert(tk.END, pase)
        text.config(state="disabled")  # Para evitar modificaciones
        text.pack(pady=5)

def generar_pdf_pases(pases, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50  # margen superior
    for pase in pases:
        textobject = c.beginText(50, y)
        textobject.setFont("Helvetica", 12)
        for line in pase.split('\n'):
            textobject.textLine(line)
        c.drawText(textobject)
        y -= 250  # espacio entre pases; ajusta según necesites
        if y < 50:  # si se acaba el espacio, se agrega una nueva página
            c.showPage()
            y = height - 50
    c.save()

def generar_y_mostrar_pdf_pases(vuelo_id, usuarios):
    pases = []
    for user_id in usuarios:
        pase = generar_pase_abordar(vuelo_id, user_id)
        if pase:
            pases.append(pase)
    
    # Si solo hay un usuario, obtenemos su nombre y pasaporte desde la BD y lo usamos
    if len(usuarios) == 1:
        cursor.execute("SELECT nombre, pasaporte FROM Usuarios WHERE id = ?", (usuarios[0],))
        result = cursor.fetchone()
        if result:
            nombre_usuario = result[0].replace(" ", "_")  # Reemplazar espacios en el nombre
            pasaporte = result[1].replace(" ", "_")  # Asegurar que no haya espacios en el pasaporte
        else:
            nombre_usuario = "usuario"
            pasaporte = "desconocido"
        filename = f"pase_{nombre_usuario}_{pasaporte}.pdf"
    
    else:
        # Para múltiples usuarios, usamos solo el primer usuario registrado como referencia
        cursor.execute("SELECT nombre, pasaporte FROM Usuarios WHERE id = ?", (usuarios[0],))
        result = cursor.fetchone()
        if result:
            nombre_usuario = result[0].replace(" ", "_")  # Quitar espacios en el nombre
            pasaporte = result[1].replace(" ", "_")  # Quitar espacios en el pasaporte
        else:
            nombre_usuario = "usuario"
            pasaporte = "desconocido"
        filename = f"pase_{nombre_usuario}_{pasaporte}.pdf"
    
    generar_pdf_pases(pases, filename)
    messagebox.showinfo("PDF generado", f"Se ha generado el PDF: {filename}")

    # Opcional: Abrir el PDF automáticamente (ajusta según tu sistema operativo)
    import os
    if os.name == 'nt':  # Windows
        os.system(f"start {filename}")
    else:  # macOS o Linux
        os.system(f"open {filename}")

# ---------------------------
# INICIO DEL PROGRAMA
# ---------------------------
conn, cursor = conectar_bd()

if messagebox.askyesno("Acompañantes", "¿Viaja con más personas?"):
    num_acompanantes = simpledialog.askinteger("Número de Acompañantes", "¿Cuántas personas viajan con usted?", minvalue=1)
else:
    num_acompanantes = 0

total_registrations = 1 + num_acompanantes
registrar_usuarios_multiples(total_registrations, 1)

root.mainloop()