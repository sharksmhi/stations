import logging
import pathlib

logger = logging.getLogger(__name__)

DEFAULT_STATION_FILE_PATH = pathlib.Path(__file__).parent / 'station.txt'


class StationFile:
    """Class to handle the official station list att SMHI"""

    def __init__(self, path: pathlib.Path, **kwargs):
        self._path = pathlib.Path(path)
        self._encoding = kwargs.get('encoding', 'cp1252')

        self._header = []
        self._data = dict()
        self._synonyms = dict()

        self._load_file()

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def header(self) -> list[str]:
        return self._header

    @property
    def keys_not_as_synonyms(self) -> list[str]:
        """Returns a list of column names that can not be used as synonyms"""
        return ['synonym_names', 'lat_dm', 'long_dm', 'latitude_wgs84_sweref99_dd', 'longitude_wgs84_sweref99_dd',
                'latitude_sweref99tm', 'longitude_sweref99tm', 'out_of_bounds_radius', 'wadep', 'media', 'comnt']

    @staticmethod
    def _convert_synonym(synonym: str) -> str:
        """Converts a synonym (in list or given by user) to a more comparable string"""
        return synonym.lower().replace(' ', '')

    @staticmethod
    def _convert_station_name(station_name: str) -> str:
        """Converts a public value (in list or given by user) to a more comparable string"""
        return station_name.upper()

    @staticmethod
    def _convert_header_col(header_col: str) -> str:
        """Converts a header column (in station file or given by user) to a more comparable string"""
        return header_col.strip().lower()

    def _load_file(self) -> None:
        with open(self.path, encoding=self._encoding) as fid:
            for r, line in enumerate(fid):
                if not line.strip():
                    continue
                split_line = [item.strip() for item in line.split('\t')]
                if r == 0:
                    header = split_line
                    self._header = [self._convert_header_col(item) for item in header]
                    continue
                line_dict = dict(zip(self._header, split_line))
                # Fix synonyms
                synonym_string = line_dict['synonym_names']
                line_dict['synonym_names'] = set()
                for item in synonym_string.split('<or>'):
                    syn = self._convert_synonym(item)
                    if not syn:
                        continue
                    line_dict['synonym_names'].add(syn)
                for col in self.header:
                    if col in self.keys_not_as_synonyms:
                        continue
                    item = self._convert_synonym(line_dict[col])
                    if not item:
                        continue
                    line_dict['synonym_names'].add(item)
                # Store synonyms
                for syn in line_dict['synonym_names']:
                    self._synonyms[syn] = line_dict['station_name']

                # Store date
                self._data[self._convert_station_name(line_dict['station_name'])] = line_dict

    def get_station_name_list(self) -> list[str]:
        return sorted(self._data)

    def get_station_name(self, synonym: str = None) -> set | None:
        """Takes a synonym of a station and returns the corresponding station name. Returns None if no match for the
        synonym is found"""
        return self._synonyms.get(self._convert_synonym(synonym), None)

    def get_station_info(self, synonym: str) -> dict:
        """Returns all station information corresponding to the given synonym.
        Returns None if synonym dont match any station"""
        station = self.get_station_name(synonym)
        if not synonym:
            return None
        return self._data[station]

    def get_translation(self, synonym: str = None, translate_to: str = None) -> str | None:
        """Takes a synonym and translates it to the list specified in 'translate_to'. Returns None if not found"""
        translate_to = self._convert_header_col(translate_to)
        if translate_to not in self.header:
            msg = f'Not able to translate to "{translate_to}". Nu such mapping available'
            logger.warning(msg)
            raise KeyError(msg)
        station_name = self.get_station_name(synonym)
        if not station_name:
            logger.warning(f'Could not find station_name matching "{synonym}"."')
            return None
        return self._data[station_name][translate_to]

    def get_pos_dm(self, synonym: str) -> tuple[str, str] | None:
        station_data = self._data.get(self.get_station_name(synonym))
        if not station_data:
            return None
        return station_data[self._convert_header_col('LAT_DM')], station_data[self._convert_header_col('LON_DM')]

    def get_pos_wgs84_sweref99_dd(self, synonym: str) -> tuple[str, str] | None:
        station_data = self._data.get(self.get_station_name(synonym))
        if not station_data:
            return None
        return station_data[self._convert_header_col('LATITUDE_WGS84_SWEREF99_DD')], \
            station_data[self._convert_header_col('LONGITUDE_WGS84_SWEREF99_DD')]

    def get_pos_sweref99tm(self, synonym: str) -> tuple[str, str] | None:
        station_data = self._data.get(self.get_station_name(synonym))
        if not station_data:
            return None
        return station_data[self._convert_header_col('LATITUDE_SWEREF99TM')], \
            station_data[self._convert_header_col('LONGITUDE_SWEREF99TM')]

    def list_synonyms(self, station_name: str) -> list[str]:
        station_name = self._convert_station_name(station_name)
        return self._data[station_name]['synonym_names']


def get_station_object(path: pathlib.Path = DEFAULT_STATION_FILE_PATH) -> "StationFile":
    return StationFile(path)


