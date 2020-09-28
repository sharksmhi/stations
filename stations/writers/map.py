# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-28 10:44

@author: a002028

"""
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon


class Map:
    """
    """
    def __init__(self):

        self.map = folium.Map(location=[61.75, 19.45],
                              zoom_start=5,
                              # tiles='cartodbdark_matter'
                              tiles='cartodbpositron'
                              # tiles='openstreetmap'
                              )

    def activate_layercontrol(self):
        """
        :return:
        """
        folium.LayerControl().add_to(self.map)

    def add_point_labels(self, label_dict):
        """
        :param label_dict:
        :return:
        """
        for key in label_dict:
            marker = folium.map.Marker(label_dict[key].get('position'),
                                       icon=DivIcon(icon_size=(150, 36),
                                                    icon_anchor=(0, 0),
                                                    html='<div style="font-size: 24pt">%s</div>' % label_dict[key].get('text')
                                                    )
                                       )
            marker.add_to(self.map)

    def add_markers(self, df, group_name=None):
        """

        :param df:
        :param group_name:
        :return:
        """
        self.check_data_content(df, group_name)
        fg = self.get_group(group_name, add_to_map=False, return_group=True)
        for i, row in df.iterrows():
            html_obj = self.get_html_object(row, i)
            popup = self.get_popup(html_obj)
            marker = self.get_marker(row, popup)
            marker.add_to(fg)
        fg.add_to(self.map)

    def add_markers_as_cluster(self, df, group_name=None):
        """

        :param df:
        :param group_name:
        :return:
        """
        self.check_data_content(df, group_name)
        fg = self.get_group(group_name, add_to_map=True, return_group=True)
        mc = MarkerCluster()
        for i, row in df.iterrows():
            html_obj = self.get_stnreg_html_object(row)
            popup = self.get_popup(html_obj)
            marker = self.get_marker(row, popup)
            marker.add_to(mc)
        mc.add_to(fg)

    def get_group(self, name, show=False, add_to_map=False, return_group=True):
        """
        :return:
        """
        fg = folium.FeatureGroup(name=name, show=show)
        if add_to_map:
            fg.add_to(self.map)
        if return_group:
            return fg

    def get_stnreg_html_object(self, data):
        """
        :param data:
        :param i:
        :return:
        """
        synonym_string = 'Synonyms: <br>- ' + '<br>- '.join(data[self.reg_synonym_key].split('<or>'))

        html_string = '<b>Station_reg_name: %s<br>' % data[self.reg_name_key] + synonym_string + \
                      '<br><br>Latitude: %f<br>' \
                      'Longitude: %f<br>' \
                      'Radius: %s<br>' \
                      'MRPOG: %s<br>' \
                      'DTYPE: %s<br>' % (data[self.lat_key], data[self.lon_key], data[self.reg_radius_key],
                                         data[self.reg_mprog_key], data[self.reg_dtype_key])
        return folium.Html(html_string, script=True)

    def get_html_object(self, data, i):
        """
        :param data:
        :param i:
        :return:
        """
        synonym_string = '<br>Synonyms: <br>- ' + '<br>- '.join(data[self.synonym_key].split(';'))
        html_string = '<b>Name: %s<br>' % (data[self.name_key] + synonym_string) + \
                      'Datatype: %s<br>' \
                      'Latitude: %f<br>' \
                      'Longitude: %f<br>' \
                      'Project: %s<br>' \
                      'Sampling Start: %s<br>' \
                      'Sampling End: %s<br>' \
                      'Nr visits: %s<br>' \
                      'Comment: %s<br><br>' \
                      'Distance to reg: %s m<br>' \
                      'Station_reg_name: %s</b>' % (data[self.dtype_key], data[self.lat_key], data[self.lon_key], data[self.proj_key],
                                                    data[self.smp_start_key], data[self.smp_end_key], str(data[self.nr_vis_key]), data[self.user_comnt_key],
                                                    str(data[self.dist_key]), data[self.regname_key])
        return folium.Html(html_string, script=True)

    def get_html_object_missing_names(self, data, i):
        """
        :param data:
        :param i:
        :return:
        """
        html_string = '<b>Serie: %s<br>' \
                      'List index: %i<br>' \
                      'Latitude: %s<br>' \
                      'Longitude: %s<br>' \
                      'Distance to reg: %i m<br>' \
                      'Station_reg_name: %s</b>' % (data['KEY'], i+2, data[self.lat_dm_key], data[self.lon_dm_key],
                                                    data['DISTANCE_TO_STNREG'], data['NAME_SUGGESTION'])
        return folium.Html(html_string, script=True)

    def get_marker(self, row, popup):
        """
        :return:
        """
        return folium.Marker(
                            [row[self.lat_key], row[self.lon_key]],
                            popup=popup,
                            icon=folium.Icon(color=row['color_tag'], icon=row['icon_tag']),
                            tooltip='Click me!'
        )

    @staticmethod
    def get_popup(html_obj):
        """
        :param html_obj:
        :return:
        """
        return folium.Popup(html_obj, max_width=500)

    def save_map(self, name='map.html'):
        """
        :return:
        """
        self.map.save(name)


if __name__ == '__main__':

    m = Map()
    m.save_map()
