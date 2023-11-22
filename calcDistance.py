import csv
import math

# Funktion zur Berechnung der Entfernung zwischen zwei Punkten
def calculate_distance(x1, y1, x2, y2):
    return int((math.sqrt((y2 - y1)**2 + (x2 - x1)**2))/10)

# Lese die Knoten und Kanten aus den CSV-Dateien
nodes_file = 'nodes.csv'
edges_file = 'edges.csv'

nodes = {}
edges = []

with open(nodes_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        name, x, y = map(str, row)
        nodes[name] = {'x': float(x), 'y': float(y)}

with open(edges_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        start, end, road_type = row
        start_coords = nodes[start]
        end_coords = nodes[end]
        distance = calculate_distance(start_coords['x'], start_coords['y'], end_coords['x'], end_coords['y'])
        edges.append((start, end, distance, road_type))

# Aktualisiere die Edge-CSV-Datei mit den berechneten Längen
with open(edges_file, 'w', newline='') as csvfile:
    fieldnames = ['start', 'end', 'length', 'road_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Corrected line

    for edge in edges:
        writer.writerow({'start': edge[0], 'end': edge[1], 'length': edge[2], 'road_type': edge[3]})
