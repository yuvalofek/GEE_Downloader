# -*- coding: utf-8 -*-
import ee
ee.Initialize()

import geemap
import os
import datetime
from dateutil import parser
import json
import argparse

"""Main downloading function"""
def get_collections_by_dates(collections: dict,
                                start_date: datetime.date,
                                end_date: datetime.date,
                                aoi: ee.Geometry,
                                out_dir: str='./',
                                scale: int=30,
                                crs: str=None
                                ):
    """
    Download images for image collections in 'collections' from 'start_date' to 'end_date' in the area of interest
    specfied in 'aoi'.  Optional output directory ('out_dir'), scale, and crs.
    :param collections: dictionary of ics to download
    :param start_date: date to start downloading
    :param end_date: last date to download
    :param aoi: Area of interest
    :param out_dir: Output directory
    :param scale: Desired scale
    :param crs: Desired Coordinate reference system
    :return: None
    """

    # input check
    for ic in collections.values():
        if not isinstance(ic, ee.ImageCollection):
            print('Input is not an image collection')
            return

    # check if output path exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    delta = datetime.timedelta(days=1)
    # move in along time with a delta-long window
    while start_date <= end_date:
        date_dir = os.path.join(os.path.abspath(out_dir), str(start_date))

        if not os.path.exists(date_dir):
            os.mkdir(date_dir)

        for ic_name, ic_ in collections.items():
            # get the daily images, mosaic them, & clip to aoi
            img = ic_.filterDate(str(start_date), str(start_date+delta)).filterBounds(aoi).mosaic().clip(aoi)

            # output names and path
            name = ic_name+str(start_date)+'.tif'
            file_path = os.path.join(os.path.abspath(date_dir), name)

            # export
            geemap.ee_export_image(
                img,
                filename=file_path,
                scale=scale,
                crs=crs,
            )

        # increment the date
        start_date+= delta

def parse_args():
    """
    Parse flags
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('--collections', type=str, default='./collections.json', help='GEE collections to download (json)')
    parse.add_argument('--out_dir', type=str, default='./', help='output dir')
    parse.add_argument('--start_date', type=lambda s: parser.parse(s).date(), default=datetime.date(2020, 12, 25), help='date to start download')
    parse.add_argument('--end_date', type=lambda s: parser.parse(s).date(), default=datetime.date(2020,12,30), help='date to end download')
    parse.add_argument('--aoi_path', type=str, default='./geometry.json', help='path to area-of-interest file (json)')
    parse.add_argument('--scale', type=int, default=30, help='desired scale')
    parse.add_argument('--crs', type=str, default=None, help='desired crs')
    return parse.parse_args()

def get_geometry(filepath:str) -> ee.Geometry:
    """
    Reads a json file into a ee.Geometry object
    :param filepath: path to geojson file
    :return: ee.Geometry corresponding to the input geojson
    """
    with open(filepath, 'r') as f:
        fc = json.load(f)
    geometry = fc['features'][0]['geometry']
    return ee.Geometry(geometry)

def get_collections(filepath:str) -> dict:
    with open(filepath, 'r') as f:
        fc = json.load(f)
    return {name: ee.ImageCollection(ic) for name, ic in fc.items()}

def main():
    # get flags
    args = parse_args()

    # make aoi
    aoi = get_geometry(args.aoi_path)

    # set up the collections dict
    ics = get_collections(args.collections)


    get_collections_by_dates(collections=ics,
                             start_date=args.start_date,
                             end_date=args.end_date,
                             out_dir=args.out_dir,
                             aoi=aoi,
                             scale=args.scale,
                             crs=args.crs
    )

if __name__ == '__main__':
    main()
