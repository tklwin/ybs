# Yangon Bus Service (YBS) Data

This repository contains data about Yangon Bus Service (YBS) bus stops and routes.

## Files

- **ybs_clean_with_id.csv**: CSV file containing bus stop information with direction data
  - `name`: Bus stop name (in Burmese)
  - `geometry`: Geographic coordinates (POINT format)
  - `@id`: OpenStreetMap node ID
  - `direction`: Geographic cardinal direction (North, South, East, West) indicating the bus stop's location relative to other stops with the same name

- **ybs_route.geojson**: GeoJSON file containing bus route geometries and relationships
  - Contains route information
  - Contains node (bus stop) information with their associated routes

- **add_direction.py**: Python script to add direction column to the CSV file

- **example_rename_stops.py**: Example script demonstrating how to use the direction data to rename bus stops

## Understanding the Data

The same bus stop name can appear multiple times in the CSV file because:
- Each instance represents a bus stop on a different side of the road/street
- Each instance serves different route directions
- The `direction` column helps distinguish which side of the road/street the bus stop is located

### Example

```csv
( ၁ ) နံပါတ် မှတ်တိုင်,POINT (96.124055 16.9749017),node/4841337261,West
( ၁ ) နံပါတ် မှတ်တိုင်,POINT (96.124309 16.974721),node/4841337262,East
```

In this example, the same bus stop "( ၁ ) နံပါတ် မှတ်တိုင်" appears twice with:
- Different coordinates (different sides of the road)
- Different node IDs
- Different geographic directions (West vs East) based on their relative positions

## How the Script Works

The `add_direction.py` script:
1. Loads bus stop data from `ybs_clean_with_id.csv`
2. Groups bus stops by name
3. For bus stops with the same name (indicating multiple stops on different sides of the street):
   - Calculates the centroid (average position) of all stops with that name
   - Determines each stop's cardinal direction (North, South, East, West) relative to the centroid
   - Assigns geographic direction labels to distinguish them
4. Adds a `direction` column to the CSV file with these cardinal directions

### Geographic Direction Calculation

The script calculates cardinal directions based on actual geographic coordinates:
- **North**: Bus stop is north of the centroid of stops with the same name
- **South**: Bus stop is south of the centroid
- **East**: Bus stop is east of the centroid
- **West**: Bus stop is west of the centroid
- **North-East**, **North-West**, **South-East**, **South-West**: Diagonal positions

This helps identify which side of the street or intersection a bus stop is located on.

### Running the Script

```bash
python3 add_direction.py
```

This will read `ybs_clean_with_id.csv`, calculate geographic directions, and create an updated CSV file with direction information.

### Using the Direction Data

An example script `example_rename_stops.py` demonstrates how to use the direction data to rename bus stops:

```bash
python3 example_rename_stops.py
```

This example shows how to append cardinal directions to bus stop names (e.g., "Main Stop (North)" vs "Main Stop (South)") to distinguish stops on different sides of the street.

## Data Statistics

- Total bus stops: 2,106
- Unique bus stop names: 889
- Bus stops with multiple locations (same name, different coordinates): 796
- Bus stops with calculated directions: 1,313 (62%)
- Bus stops without directions: 793 (38% - these are unique names with only one location)

## Data Quality Notes

The direction data is calculated from the geographic coordinates of bus stops:
- Cardinal directions (North, South, East, West) are based on relative positions
- Stops very close to the centroid (within ~11 meters) may not have a direction assigned
- The direction helps distinguish bus stops on different sides of a street or at different corners of an intersection

## Use Cases

The geographic direction information is useful for:
- Renaming bus stops to include their location (e.g., "Main Street (North side)" vs "Main Street (South side)")
- Navigation and wayfinding applications
- Distinguishing which side of the street a bus stop is on
- Identifying the correct bus stop when multiple stops share the same name

## Data Source

The data is sourced from OpenStreetMap (OSM) and represents the Yangon Regional Transport Authority (YRTA) bus network operated by YBS.
