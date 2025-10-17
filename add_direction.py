#!/usr/bin/env python3
"""
Script to add direction column to bus stops CSV file.
Uses the relationship between bus stops (nodes) in the CSV file and 
route directions in the GeoJSON file.
"""

import json
import csv

def load_geojson_nodes(geojson_file):
    """Load nodes with their associated directions from geojson file."""
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    nodes_dict = {}
    for feature in data['features']:
        if feature['geometry']['type'] == 'Point':
            node_id = feature['properties'].get('@id', '')
            if '@relations' in feature['properties']:
                # Collect all unique directions for this node from its relations
                directions = set()
                for rel in feature['properties']['@relations']:
                    if 'reltags' in rel and 'direction' in rel['reltags']:
                        directions.add(rel['reltags']['direction'])
                
                # Join all directions with semicolon separator
                nodes_dict[node_id] = '; '.join(sorted(directions)) if directions else ''
    
    return nodes_dict

def add_direction_to_csv(csv_input, csv_output, nodes_dict):
    """Add direction column to CSV file based on node directions from geojson."""
    with open(csv_input, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        
        if reader.fieldnames is None:
            raise ValueError(f"CSV file {csv_input} is empty or malformed")
        
        # Only add direction column if it doesn't already exist
        fieldnames = list(reader.fieldnames)
        if 'direction' not in fieldnames:
            fieldnames.append('direction')
        
        with open(csv_output, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                node_id = row['@id']
                # Add direction from nodes_dict, or empty string if not found
                row['direction'] = nodes_dict.get(node_id, '')
                writer.writerow(row)

def main():
    geojson_file = 'ybs_route.geojson'
    csv_input = 'ybs_clean_with_id.csv'
    csv_output = 'ybs_clean_with_id_and_direction.csv'
    
    print(f"Loading nodes from {geojson_file}...")
    nodes_dict = load_geojson_nodes(geojson_file)
    print(f"Loaded {len(nodes_dict)} nodes with direction information")
    
    print(f"Processing {csv_input}...")
    add_direction_to_csv(csv_input, csv_output, nodes_dict)
    print(f"Created {csv_output} with direction column")
    
    # Show some sample output
    print("\nSample output (first 10 rows):")
    with open(csv_output, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 10:
                break
            print(f"{row['name']}: {row['direction']}")

if __name__ == '__main__':
    main()
