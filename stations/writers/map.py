# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-28 10:44

@author: a002028

"""
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from stations.writers.writer import WriterBase


def get_html_string_format(*args):
    s = '<b>'
    for a in args:
        new_line = a + ': %s<br>'
        s += new_line
    s += '</b>'
    return s


class MapWriter(WriterBase):
    """
    """
    def __init__(self, **kwargs):
        super(MapWriter, self).__init__()

        for key, item in kwargs.items():
            setattr(self, key, item)

        self.map = folium.Map(**self.map_settings)

        self.html_fmt = get_html_string_format(*(self.marker_tag_attributes.get(key)
                                                 for key in self.marker_tag_attributes))

    def write(self, file_path, list_obj):
        """
        :param file_path:
        :param list_obj:
        :return:
        """
        self.add_markers_as_cluster(list_obj, group_name='Group_name')
        self._write(file_path)

    def _write(self, file_path):
        """
        :param file_path:
        :return:
        """
        self.map.save(file_path)

    def add_markers_as_cluster(self, list_obj, group_name=None):
        """

        :param df:
        :param group_name:
        :return:
        """
        fg = self.get_group(name=group_name,
                            add_to_map=True,
                            return_group=True)

        mc = MarkerCluster()

        for idx in range(list_obj.length):
            html_obj = self.get_html_object(list_obj.get(key)[idx].replace('<or>', '; ') for key in self.marker_tag_attributes)
            popup = self.get_popup(html_obj)
            marker = self.get_marker([list_obj.get('lat_dd')[idx],
                                      list_obj.get('lon_dd')[idx]],
                                     popup=popup,
                                     tooltip=list_obj.get('name')[idx] or 'Click me!')
            marker.add_to(mc)

        mc.add_to(fg)

    def get_group(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        fg = folium.FeatureGroup(**kwargs)

        if kwargs.get('add_to_map'):
            fg.add_to(self.map)

        if kwargs.get('return_group'):
            return fg

    def get_html_object(self, *args):
        """
        :param args:
        :return:
        """
        html_string = self.html_fmt % tuple(*args)
        return folium.Html(html_string, script=True)

    @staticmethod
    def get_marker(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        return folium.Marker(*args, **kwargs)

    @staticmethod
    def get_popup(html_obj):
        """
        :param html_obj:
        :return:
        """
        return folium.Popup(html_obj, max_width=500)


if __name__ == '__main__':

    m = MapWriter(map_settings={'location': [61.75, 19.45],
                                'zoom_start': 5},
                  marker_tag_attributes={'name': 'name',
                                         'id': 'id',
                                         'lat_dd': 'lat_dd',
                                         'lon_dd': 'lon_dd'})
    m._write('map.html')
