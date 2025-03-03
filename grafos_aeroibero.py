import networkx as nx
import matplotlib.pyplot as plt

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





# Crear el grafo dirigido
G = nx.DiGraph()

# Agregar nodos
for nodo in nodos:
    G.add_node(nodo, **nodos[nodo])

for arista in aristas:
    G.add_edge(arista["origen"], arista["destino"], 
               distancia=arista["distancia"], 
               tiempo=arista["tiempo"], 
               costo=arista["costo"])

def dibujar_grafo(criterio="distancia"):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, k=2)  

    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=8)
    
    etiquetas = nx.get_edge_attributes(G, criterio)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_size=8)
    
    plt.title(f"Grafo con pesos por {criterio.capitalize()}")
    plt.show()

#dibujar_grafo("distancia") 

#dibujar_grafo("tiempo")

dibujar_grafo("costo") 
