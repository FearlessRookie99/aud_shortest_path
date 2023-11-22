import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import heapq

def read_graph_data(nodes_file, edges_file):
    nodes_df = pd.read_csv(nodes_file)
    edges_df = pd.read_csv(edges_file)
    
    edges_df['zeit'] = edges_df['length'] / edges_df['speed']
    edges_df['verbrauch'] = edges_df['consumption'] / 100 * edges_df['length']
    
    G = nx.Graph()

    for index, row in nodes_df.iterrows():
        G.add_node(row['city'], pos=(row['x'], row['y']))
        
    for index, row in edges_df.iterrows():
        G.add_edge(row['node1'], row['node2'], type=row['type'], length=row['length'], speed=row['speed'], consumption=row['consumption'], zeit=row['zeit'], verbrauch=row['verbrauch'])

    return G

def dijkstra_algorithm(graph, source, target, weight='length'):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[source] = 0
    predecessors = {node: None for node in graph.nodes}
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == target:
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = predecessors[current_node]
            return path

        for neighbor in graph.neighbors(current_node):
            distance = current_distance + graph[current_node][neighbor][weight]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return []

def calculate_path_stats(G, path, weight):
    length = sum(G[path[i]][path[i + 1]][weight] for i in range(len(path) - 1))
    time = sum(G[path[i]][path[i + 1]]['zeit'] for i in range(len(path) - 1))
    consumption = round(sum(G[path[i]][path[i + 1]]['verbrauch'] for i in range(len(path) - 1)), 2)

    return length, time, consumption

def format_time(hours):
    total_minutes = int(hours * 60)
    if total_minutes < 60 :
       return f"{total_minutes % 60} Minuten" 
    else :
        return f"{total_minutes // 60} Stunden {total_minutes % 60} Minuten"
    

def visualize_graph(G, *paths, background_image=None, figure_size=(12, 8)):
    pos = nx.get_node_attributes(G, 'pos')
    
    fig, ax = plt.subplots(figsize=figure_size)

    if background_image:
        img = plt.imread(background_image)
        ax.imshow(img, extent=[-2000, 2000, -2000, 2000], aspect='auto', alpha=0.9)

    edge_colors = []
    edge_widths = []

    for edge in G.edges():
        edge_type = G[edge[0]][edge[1]]['type']
        if edge_type == 'normal':
            edge_colors.append('yellow')
            edge_widths.append(1)
        else:
            edge_colors.append('blue')
            edge_widths.append(1)

    nx.draw(G, pos, ax=ax, with_labels=True, font_weight='bold', node_size=50, font_size=8, edge_color=edge_colors, width=edge_widths)

    for i, path in enumerate(paths):
        edges = [(path[j], path[j + 1]) for j in range(len(path) - 1)]
        edge_color = 'red' if i == 0 else 'green' if i == 1 else 'purple' if i == 2 else 'black'
        nx.draw_networkx_edges(G, pos, edgelist=edges, ax=ax, edge_color=edge_color, width=2)

    plt.show()

# Schritt 1: Daten einlesen und Graphen erstellen
Graph_data = read_graph_data('nodes2.csv', 'edges2.csv')

source = input(str('bitte Start Ort eingeben: '))
target = input(str('bitte Ziel Ort eingeben: '))

# Schritt 2: Verwende Dijkstra-Algorithmus für den kürzesten Weg
shortest_path = dijkstra_algorithm(Graph_data, source=source, target=target, weight='length')
shortest_length, shortest_time, shortest_consumption = calculate_path_stats(Graph_data, shortest_path, 'length')
print("Kürzester Weg:")
print("Pfad:", shortest_path)
print("Strecke:", shortest_length, "km")
print("Zeit:", format_time(shortest_time))
print("Verbrauch:", shortest_consumption, "Einheiten")

# Schritt 3: Schnellster Weg
fastest_path = dijkstra_algorithm(Graph_data, source=source, target=target, weight='zeit')
fastest_length, fastest_time, fastest_consumption = calculate_path_stats(Graph_data, fastest_path, 'length')
print("\nSchnellster Weg:")
print("Pfad:", fastest_path)
print("Strecke:", fastest_length, "km")
print("Zeit:", format_time(fastest_time))
print("Verbrauch:", fastest_consumption, "Einheiten")

# Schritt 4: Energieeffizientester Weg
efficient_path = dijkstra_algorithm(Graph_data, source=source, target=target, weight='verbrauch')
efficient_length, efficient_time, efficient_consumption = calculate_path_stats(Graph_data, efficient_path, 'length')
print("\nEnergieeffizientester Weg:")
print("Pfad:", efficient_path)
print("Strecke:", efficient_length, "km")
print("Zeit:", format_time(efficient_time))
print("Verbrauch:", efficient_consumption, "Einheiten")

# Schritt 5: Visualisierung mit Hintergrundbild
background_image_path = 'Screenshot 2023-11-20 234021.png'
visualize_graph(Graph_data, shortest_path, fastest_path, efficient_path, background_image=background_image_path)
