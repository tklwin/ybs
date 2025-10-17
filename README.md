# Yangon Bus Service (YBS) Data

This repository contains data about Yangon Bus Service (YBS) bus stops and routes.

## Files

- **ybs_clean_with_id.csv**: CSV file containing bus stop information with direction data
  - `name`: Bus stop name (in Burmese)
  - `geometry`: Geographic coordinates (POINT format)
  - `@id`: OpenStreetMap node ID
  - `direction`: Route directions served by this bus stop (semicolon-separated)

- **ybs_route.geojson**: GeoJSON file containing bus route geometries and relationships
  - Contains route information with directions
  - Contains node (bus stop) information with their associated routes

- **add_direction.py**: Python script to add direction column to the CSV file

## Understanding the Data

The same bus stop name can appear multiple times in the CSV file because:
- Each instance represents a bus stop on a different side of the road/street
- Each instance serves different route directions
- The `direction` column helps distinguish which side of the road/street the bus stop is located

### Example

```csv
( ၁ ) ဈေး ကွေ့ မှတ်တိုင်,POINT (96.1952103 16.7961857),node/4841300197,E; east; forward; inbound
( ၁ ) ဈေး ကွေ့ မှတ်တိုင်,POINT (96.1954986 16.7964999),node/4841300198,E; east; outbound; southeast
```

In this example, the same bus stop "( ၁ ) ဈေး ကွေ့ မှတ်တိုင်" appears twice with:
- Different coordinates (different sides of the road)
- Different node IDs
- Different directions (inbound vs outbound)

## How the Script Works

The `add_direction.py` script:
1. Loads bus route data from `ybs_route.geojson`
2. Extracts direction information from each route that includes a bus stop
3. Maps each bus stop node ID to its associated directions
4. Adds a `direction` column to the CSV file

### Running the Script

```bash
python3 add_direction.py
```

This will read `ybs_clean_with_id.csv` and `ybs_route.geojson`, then update the CSV file with direction information.

## Data Statistics

- Total bus stops: 2,106
- Bus stops with direction information: 1,956 (93%)
- Bus stops without direction information: 150 (7%)

## Data Quality Notes

The direction data is sourced directly from OpenStreetMap and may contain:
- Mixed capitalization (e.g., "Outbound" vs "outbound")
- Inconsistent formatting
- Some misspellings from the original OSM data (e.g., "norhtwest" instead of "northwest")

These values are preserved as-is from the source data. If data normalization is needed for your use case, consider implementing a post-processing step to standardize direction values.

## Data Source

The data is sourced from OpenStreetMap (OSM) and represents the Yangon Regional Transport Authority (YRTA) bus network operated by YBS.
