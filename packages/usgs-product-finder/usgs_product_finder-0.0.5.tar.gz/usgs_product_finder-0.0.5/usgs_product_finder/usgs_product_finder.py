import logging

logger = logging.getLogger("usgs_product_finder")
logger.setLevel(logging.DEBUG)

import os
import pandas
import geopandas
import shapely
import requests

from typing import List, Dict


class UsgsProductFinder:

    def __init__(self, path_for_usgs_data: str = None, max_age_of_usgs_data: int = 1):
        """
        Initialize the UsgsProductFinder class.

        If the path_for_usgs_data parameter is filled, the library will obtain csv's and auxiliary files to that path.
        If the files already exist, they will not be obtained again unless they are older than one day or the
        max_age_of_usgs_data parameter specified.

        :param path_for_usgs_data: Path where the library will obtain csv's and auxiliary files
        :param max_age_of_usgs_data: Maximum age of the obtained files in days
        """
        logger.debug("Initializing UsgsProductFinder")
        self.max_age_of_usgs_data = max_age_of_usgs_data
        if path_for_usgs_data is not None:
            if not os.path.exists(path_for_usgs_data):
                os.makedirs(path_for_usgs_data)
            self.path_for_usgs_data = path_for_usgs_data
        else:
            self.path_for_usgs_data = os.path.join(os.path.dirname(__file__), "data")
        self._load_in_wrs2()

    def _find_products_via_filtered_geodataframe(self, filtered_geodataframe: geopandas.GeoDataFrame,
                                                 satellite: int, minimal_output=True) -> List[str] or pandas.DataFrame:
        """
        Find products that intersect with a geodataframe.
        :param filtered_geodataframe: AOI-Filtered geodataframe
        :param satellite: Number for the satellite
        :param minimal_output: If True, returns a list of dicts with display_id, ordering_id and landsat_product_id,
         if False, returns a pandas dataframe from usgs csv
        :return: List of dicts or pandas dataframe
        """

        if satellite in [4, 5]:
            satellite_csv_path = self._obtain_l4_l5_csv()
        elif satellite == 7:
            satellite_csv_path = self._obtain_l7_csv()
        elif satellite in [8, 9]:
            satellite_csv_path = self._obtain_l8_l9_csv()
        else:
            raise ValueError("Satellite must be 4, 5, 7, 8 or 9, other satellites from landsat \
                mission are not supported")

        logger.debug(f"As the satellite is {satellite}, the CSV file {satellite_csv_path} will be used")
        logger.debug(f"Loading in CSV file {satellite_csv_path}")
        total_count_of_matching_products = 0
        if minimal_output:
            output = []
        else:
            output_dataframe = pandas.DataFrame()
        # TODO: Check if this can be threaded or multiprocessed
        for dataframe_chunk in pandas.read_csv(satellite_csv_path, chunksize=100000, low_memory=False):
            # if satellite is 7,8 or 9 convert Satellite column to str
            if satellite in [7, 8, 9]:
                dataframe_chunk["Satellite"] = dataframe_chunk["Satellite"].astype(str)

            filtered_dataframe_current_chunk = dataframe_chunk[
                (dataframe_chunk["Satellite"].str.contains(str(satellite)))
                & (dataframe_chunk["WRS Path"].isin(filtered_geodataframe["PATH"]))
                & (dataframe_chunk["WRS Row"].isin(filtered_geodataframe["ROW"]))
                ]
            total_count_of_matching_products += len(filtered_dataframe_current_chunk)
            if minimal_output:
                for index, row in filtered_dataframe_current_chunk.iterrows():
                    output.append({
                        "display_id": row["Display ID"],
                        "ordering_id": row["Ordering ID"],
                        "landsat_product_id": row["Landsat Product Identifier L2"]
                    })
            else:
                output_dataframe = pandas.concat([output_dataframe, filtered_dataframe_current_chunk])

        logger.debug(f"Found {total_count_of_matching_products} products")
        if minimal_output:
            return output
        else:
            return output_dataframe

    def find_products_via_shapely_object(self, shapely_multipolygon_object: shapely.geometry.multipolygon.MultiPolygon,
                                         satellite: int,
                                         minimal_output: bool = True) -> List[Dict[str, str]] or pandas.DataFrame:
        """
        Find products that intersect with a shapely object.
        :param shapely_multipolygon_object: Shapely multipolygon object that represents the AOI
        :param satellite: Number for the satellite [4, 5, 7, 8, 9]
        :param minimal_output: If True, returns a list of dicts with display_id, ordering_id and landsat_product_id,
         if False, returns a pandas dataframe from usgs csv
        :return: List of dicts or pandas dataframe
        """
        filtered_geodataframe: geopandas.GeoDataFrame = self.geodataframe_wrs2[
            self.geodataframe_wrs2.intersects(shapely_multipolygon_object)]
        return self._find_products_via_filtered_geodataframe(filtered_geodataframe, satellite, minimal_output)

    def find_products_via_wkt(self, wkt: str, satellite: int, minimal_output=True) -> List[Dict[
        str, str]] or pandas.DataFrame:
        """
        Find products that intersect with a wkt string.
        :param wkt: WKT string that represents the AOI
        :param satellite: Number for the satellite [4, 5, 7, 8, 9]
        :param minimal_output: If True, returns a list of dicts with display_id, ordering_id and landsat_product_id,
         if False, returns a pandas dataframe from usgs csv
        :return: List of dicts or pandas dataframe
        """
        shapely_multipolygon_object = shapely.wkt.loads(wkt)
        return self.find_products_via_shapely_object(shapely_multipolygon_object, satellite, minimal_output)

    def _obtain_file(self, url: str) -> str:
        """
        obtain a file from specified url into the path specified in the constructor.

        Skips the obtain if the file already exists and is newer than self.max_age_of_usgs_data.
        :param url: URL of a file to obtain
        :return:  Newly obtained file's path
        """
        local_filepath = os.path.join(self.path_for_usgs_data, os.path.basename(url))
        logger.debug(f"Checking if {local_filepath} exists and is less than {self.max_age_of_usgs_data} days old")
        if not os.path.exists(local_filepath) or (
                (
                        os.path.exists(local_filepath)
                        and (
                            os.path.getmtime(local_filepath)
                            < (pandas.Timestamp.now() - pandas.Timedelta(days=self.max_age_of_usgs_data)).timestamp()
                        )
                )
        ):
            logger.debug(f"obtaining CSV file from {url} into {local_filepath}")
            r = requests.get(url, stream=True)
            # make folder if it doesn't exist
            if not os.path.exists(os.path.dirname(local_filepath)):
                os.makedirs(os.path.dirname(local_filepath))
            with open(local_filepath, "wb") as f:
                f.write(r.content)
            logger.debug("obtain complete")
        else:
            logger.debug(
                "CSV file already exists and is less than 7 days old, not obtaining again"
            )
        logger.debug(f"Returning {local_filepath}")
        return local_filepath

    def _obtain_l4_l5_csv(self) -> str:
        """
        Obtain the csv's for Landsat 4 and 5, downloading if necessary.
        :return: FIle location
        """
        l4_l5_csv_url = "https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/LANDSAT_TM_C2_L2.csv.gz"
        return self._obtain_file(l4_l5_csv_url)

    def _obtain_l7_csv(self) -> str:
        """
        Obtain the csv for Landsat 7, downloading if necessary.
        :return: FIle location
        """
        l7_url = "https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/LANDSAT_ETM_C2_L2.csv.gz"
        return self._obtain_file(l7_url)

    def _obtain_l8_l9_csv(self) -> str:
        """
        Obtain the csv's for Landsat 8 and 9, downloading if necessary.
        :return: FIle location
        """
        l8_l9_url = "https://landsat.usgs.gov/landsat/metadata_service/bulk_metadata_files/LANDSAT_OT_C2_L2.csv.gz"
        return self._obtain_file(l8_l9_url)

    def _load_in_wrs2(self) -> None:
        """
        Load in the WRS2 shapefile
        """
        wrs2_filepath = os.path.join(os.path.dirname(__file__), "files", "WRS2_descending.geojson")
        logger.debug(f"Loading in WRS2 shapefile from {wrs2_filepath}")
        self.geodataframe_wrs2 = geopandas.read_file(wrs2_filepath)
        logger.debug("WRS2 shapefile loaded in")
