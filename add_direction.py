#!/usr/bin/env python3
"""
Script to add direction column to bus stops CSV file.
Calculates geographic cardinal directions (North, South, East, West) based on 
the actual coordinates of bus stops to help distinguish bus stops on different 
sides of the street.
"""

import json
import csv
from collections import defaultdict

def parse_coordinates(geometry_str):
    """Parse coordinates from POINT geometry string."""
    # Format: "POINT (longitude latitude)"
    coords = geometry_str.replace('POINT (', '').replace(')', '')
    lon, lat = map(float, coords.split())
    return lat, lon

def calculate_cardinal_direction(lat, lon, centroid_lat, centroid_lon):
    """
    Calculate cardinal direction of a point relative to a centroid.
    Returns combination of N/S and E/W based on position.
    """
    # Threshold for considering a direction (in degrees)
    # About 0.0001 degrees ~ 11 meters
    threshold = 0.0001
    
    directions = []
    
    # Calculate North/South
    lat_diff = lat - centroid_lat
    if abs(lat_diff) > threshold:
        if lat_diff > 0:
            directions.append('North')
        else:
            directions.append('South')
    
    # Calculate East/West
    lon_diff = lon - centroid_lon
    if abs(lon_diff) > threshold:
        if lon_diff > 0:
            directions.append('East')
        else:
            directions.append('West')
    
    # Combine directions (e.g., "North-East")
    if directions:
        return '-'.join(directions)
    else:
        return ''

def calculate_geographic_directions(csv_input):
    """
    Calculate geographic cardinal directions for bus stops.
    For bus stops with the same name, determine their relative position
    (North, South, East, West) based on coordinates.
    """
    # First pass: group bus stops by name and collect their coordinates
    stops_by_name = defaultdict(list)
    
    with open(csv_input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat, lon = parse_coordinates(row['geometry'])
            stops_by_name[row['name']].append({
                'node_id': row['@id'],
                'lat': lat,
                'lon': lon,
                'geometry': row['geometry']
            })
    
    # Calculate directions for each stop
    directions_dict = {}
    
    for name, stops in stops_by_name.items():
        if len(stops) == 1:
            # Single stop with this name - no direction needed
            directions_dict[stops[0]['node_id']] = ''
        else:
            # Multiple stops with same name - calculate centroid and directions
            centroid_lat = sum(s['lat'] for s in stops) / len(stops)
            centroid_lon = sum(s['lon'] for s in stops) / len(stops)
            
            for stop in stops:
                direction = calculate_cardinal_direction(
                    stop['lat'], stop['lon'], 
                    centroid_lat, centroid_lon
                )
                directions_dict[stop['node_id']] = direction
    
    return directions_dict

def add_direction_to_csv(csv_input, csv_output, directions_dict):
    """Add direction column to CSV file based on calculated geographic directions."""
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
                # Add direction from directions_dict, or empty string if not found
                row['direction'] = directions_dict.get(node_id, '')
                writer.writerow(row)

def main():
    csv_input = 'ybs_clean_with_id.csv'
    csv_output = 'ybs_clean_with_id_and_direction.csv'
    
    print(f"Calculating geographic directions for bus stops in {csv_input}...")
    directions_dict = calculate_geographic_directions(csv_input)
    
    # Count stops with directions
    stops_with_direction = sum(1 for d in directions_dict.values() if d)
    print(f"Calculated directions for {stops_with_direction} bus stops (out of {len(directions_dict)} total)")
    
    print(f"Adding direction column to CSV...")
    add_direction_to_csv(csv_input, csv_output, directions_dict)
    print(f"Created {csv_output} with geographic direction column")
    
    # Show some sample output - focus on stops with same name
    print("\nSample output showing bus stops with same name but different locations:")
    stops_by_name = defaultdict(list)
    with open(csv_output, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stops_by_name[row['name']].append(row)
    
    # Show a few examples with multiple locations
    count = 0
    for name, stops in stops_by_name.items():
        if len(stops) > 1 and count < 3:
            print(f"\n'{name}':")
            for stop in stops:
                coords = stop['geometry'].replace('POINT (', '').replace(')', '')
                direction = stop['direction'] if stop['direction'] else '(center/single)'
                print(f"  {direction}: {coords}")
            count += 1

if __name__ == '__main__':
    main()
