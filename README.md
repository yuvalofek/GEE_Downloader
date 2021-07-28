# GEE_Downloader
A simple CL tool to download Google Earth Engine imagery and group images by dates. 

## Requirements:
```
earthengine-api
geemap
datetime
dateutil
```

## Usage:
```
geedownloader.py [-h] [--collections COLLECTIONS] [--out_dir OUT_DIR]
                      [--start_date START_DATE] [--end_date END_DATE]
                      [--aoi_path AOI_PATH] [--scale SCALE] [--crs CRS]
```
* collections (str)-  json file of the GEE collections to download ('name': 'collection id' format)
* out_dir (str)-      output directory
* start_date (str)-   date to start downloading
* end_date (str)-     date to end download
* aoi_path (str)-     path to area-of-interest file (json/geojson)
* scale (int)-        desired scale
* crs (str)-          desired crs (will only accept strings that are valid for Google Earth Engine)

