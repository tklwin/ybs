#!/usr/bin/env python3
"""
Example script demonstrating how to use the direction data to rename bus stops.
This shows how the geographic direction can be appended to bus stop names to
distinguish stops on different sides of the street.
"""

import csv
from collections import defaultdict

def rename_stops_with_direction(csv_input):
    """
    Example function showing how to rename bus stops with their direction.
    For bus stops with the same name but different locations, appends the
    cardinal direction to the name.
    """
    # Read the CSV and group by name
    stops_by_name = defaultdict(list)
    
    with open(csv_input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stops_by_name[row['name']].append(row)
    
    # Generate new names with directions
    renamed_stops = []
    
    for name, stops in stops_by_name.items():
        if len(stops) == 1:
            # Single stop - no need for direction
            stop = stops[0]
            renamed_stops.append({
                'original_name': name,
                'new_name': name,
                'coordinates': stop['geometry'],
                'direction': stop['direction'],
                'node_id': stop['@id']
            })
        else:
            # Multiple stops - add direction to name
            for stop in stops:
                direction = stop['direction']
                if direction:
                    # Append direction to name (you can customize the format)
                    new_name = f"{name} ({direction})"
                else:
                    # Stop is at centroid, just keep original name
                    new_name = name
                
                renamed_stops.append({
                    'original_name': name,
                    'new_name': new_name,
                    'coordinates': stop['geometry'],
                    'direction': direction,
                    'node_id': stop['@id']
                })
    
    return renamed_stops

def main():
    csv_input = 'ybs_clean_with_id_and_direction.csv'
    
    print("Renaming bus stops with geographic directions...\n")
    renamed_stops = rename_stops_with_direction(csv_input)
    
    # Show examples where renaming occurred
    print("Examples of renamed bus stops:\n")
    
    # Group by original name to show name variations
    by_original = defaultdict(list)
    for stop in renamed_stops:
        by_original[stop['original_name']].append(stop)
    
    # Show first 5 examples with multiple stops
    count = 0
    for original_name, stops in by_original.items():
        if len(stops) > 1 and count < 5:
            print(f"Original name: '{original_name}'")
            print(f"Number of locations: {len(stops)}")
            for i, stop in enumerate(stops, 1):
                print(f"  {i}. New name: '{stop['new_name']}'")
                print(f"     Coordinates: {stop['coordinates']}")
            print()
            count += 1
    
    # Statistics
    total_renamed = sum(1 for s in renamed_stops if s['original_name'] != s['new_name'])
    print(f"\nStatistics:")
    print(f"Total bus stops: {len(renamed_stops)}")
    print(f"Stops renamed with direction: {total_renamed}")
    print(f"Stops keeping original name: {len(renamed_stops) - total_renamed}")

if __name__ == '__main__':
    main()
