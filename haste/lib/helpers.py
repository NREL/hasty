import os
import pandas as pd
from uuid import uuid4
from generate import models


class Shadowfax:
    """
    The Lord of All Horses, and Gandalf's friend through many dangers.
    He knows how to show the meaning of Haste.
    """
    def __init__(self):
        p = os.path.dirname(os.path.abspath(__file__))
        f_path = os.path.join(p, 'Components.csv')
        self.df_components = pd.read_csv(f_path)
        self.df_components = self.df_components[self.df_components['Haste Choice'] == True]
        self.df_components['id'] = self.df_components['id'].astype(str)
        self.df_cc = self.df_components[self.df_components['Category'] == 'Cooling coil']
        self.df_hc = self.df_components[self.df_components['Category'] == 'Heating coil']
        self.df_dis_fan = self.df_components[self.df_components['Category'] == 'Discharge fan']
        self.df_ret_fan = self.df_components[self.df_components['Category'] == 'Return fan']
        self.df_exh_fan = self.df_components[self.df_components['Category'] == 'Exhaust fan']

        # Read in and generate terminal units
        f_path_tu = os.path.join(p, 'TerminalUnits.csv')
        self.df_terminal_units = pd.read_csv(f_path_tu)
        self.df_terminal_units = self.df_terminal_units[self.df_terminal_units['Haste Choice'] == True]
        cast_to_str = ['id', 'damperComponentID', 'heatingComponentID', 'coolingComponentID']
        self.df_terminal_units[cast_to_str] = self.df_terminal_units[cast_to_str].astype(str).applymap(lambda x: x.split('.')[0])
        self.df_terminal_units[cast_to_str] = self.df_terminal_units[cast_to_str].applymap(lambda x: "None" if x == "nan" else x)


    def generate_cooling_coils(self):
        """
        Generate a list of dicts for the different types of potential cooling coils.
        :return:
        """
        return self.df_cc.to_dict('records')

    def generate_heating_coils(self):
        """
        Generate a list of dicts for the different types of potential heating coils.
        :return:
        """
        return self.df_hc.to_dict('records')

    def generate_discharge_fans(self):
        """
        Generate a list of dicts for the different types of potential heating coils.
        :return:
        """
        return self.df_dis_fan.to_dict('records')

    def generate_return_fans(self):
        """
        Generate a list of dicts for the different types of potential heating coils.
        :return:
        """
        return self.df_ret_fan.to_dict('records')

    def generate_exhaust_fans(self):
        """
        Generate a list of dicts for the different types of potential heating coils.
        :return:
        """
        return self.df_exh_fan.to_dict('records')

    def generate_terminal_unit_types(self):
        """
        Generate a list of dicts for the different types of potential terminal units.
        :return:
        """
        return self.df_terminal_units.to_dict('records')

    def ahu_summary_info(self, ahu_model):
        """
        Return summary info for the AirHandler for displaying in the 'all_air_handlers.html' page
        :param ahu_model: A single AirHandler model
        :return: dict
        """
        tus = models.TerminalUnit.objects.filter(ahu_id=ahu_model.id)
        num_tus = tus.count()
        data = {
            'id': ahu_model.id,
            'name': ahu_model.name,
            'hc_name': self.hc_name_given_id(ahu_model.heating_coil_type),
            'cc_name': self.cc_name_given_id(ahu_model.cooling_coil_type),
            'num_terminal_units': num_tus,
            'df_name': self.df_name_given_id(ahu_model.discharge_fan_type)
        }
        return data

    def terminal_unit_summary_info(self, terminal_unit_model):
        """
        Return summary info for the TerminalUnit for displaying in the 'all_terminal_units.html' page
        :param terminal_unit_model: A single TerminalUnit model
        :return: dict
        """
        data = {
            'id': terminal_unit_model.id,
            'name': terminal_unit_model.name,
            'zone_name': terminal_unit_model.thermal_zone.name,
            'type': self.tu_name_given_id(terminal_unit_model.terminal_unit_type)
        }
        return data

    def tu_name_given_id(self, tu_id):
        tus = self.generate_terminal_unit_types()
        for tu in tus:
            if tu_id == tu['id']:
                return tu['Description']
        return None

    def hc_name_given_id(self, hc_id):
        """
        Return the human readable version of the heating coil given its id.
        :param hc_id: The id of the heating coil as returned by generate_heating_coils()
        :return: str
        """
        hcs = self.generate_heating_coils()
        for hc in hcs:
            if hc_id == hc['id']:
                return hc['Description']
        return None

    def cc_name_given_id(self, cc_id):
        """
        Return the human readable version of the cooling coil given its id.
        :param cc_id: The id of the heating coil as returned by generate_cooling_coils()
        :return: str
        """
        ccs = self.generate_cooling_coils()
        for cc in ccs:
            if cc_id == cc['id']:
                return cc['Description']
        return None

    def df_name_given_id(self, df_id):
        """
        Return the human readable version of the cooling coil given its id.
        :param cc_id: The id of the heating coil as returned by generate_cooling_coils()
        :return: str
        """
        dfs = self.generate_discharge_fans()
        for df in dfs:
            if df_id == df['id']:
                return df['Description']
        return None

class HaystackBuilder:

    def __init__(self, site, ahus):
        """

        :param site: a single models.Site entity
        :param ahus: list() all models.AirHandler entities contained in the above site
        """
        self.site = site
        self.ahus = ahus
        self.sf = Shadowfax()
        self.site_hay_id = uuid4()
        self.hay_json = []
        self.id_mapper = {}  # haystack_uuid : f"haystack_uuid database_id",

    def gen_site_record(self):
        """
        Generate a site record and add it to self.hay_json
        :return:
        """
        self.hay_json.append({
            "id": f"r:{self.site_hay_id}",
            "dis": f"s:{self.site.name}",
            "site": "m:",
            "geoCity": f"s:{self.site.city}",
            "geoState": f"s:{self.site.state}",
            "geoCountry": "United States"  # could infer this from state selection
        })
        self.id_mapper[self.site_hay_id] = f"{self.site_hay_id} {self.site.id}"

    def gen_ahu_records(self):
        """
        Generate all ahu records and add them to self.hay_json
        :return:
        """
        for ahu in self.ahus:
            hay_id = uuid4()
            self.hay_json.append({
                "id": f"r:{hay_id}",
                "dis": f"s:{ahu.name}",
                "siteRef": f"r:{self.site_hay_id}",
                "equip": "m:",
                "ahu": "m:"
            })
            self.id_mapper[hay_id] = f"{hay_id} {ahu.id}"
            self.add_ahu_components(ahu, hay_id)
            self.gen_terminal_unit_records(ahu, hay_id)

    def gen_terminal_unit_records(self, ahu, ahu_hay_id):
        """
        Generate all terminal unit records for a given air handler.
        :param ahu:
        :param ahu_hay_id:
        :return:
        """
        tus = models.TerminalUnit.objects.filter(ahu_id = ahu.id)
        for tu in tus:
            hay_id = uuid4()
            temp = {
                "id": f"r:{hay_id}",
                "dis": f"s:{tu.name}",
                "ahuRef": f"r:{ahu_hay_id}",
            }
            tu_type = self.sf.df_terminal_units[self.sf.df_terminal_units['id'] == tu.terminal_unit_type]
            if tu_type.empty:
                raise TerminalUnitNotFoundError(tu.terminal_unit_type)
            tags = tu_type['Final Tagset'].values[0]
            tags = tags.split(" ")
            for tag in tags:
                temp[tag] = "m:"
            self.hay_json.append(temp)
            self.add_terminal_unit_components(tu, hay_id)

    def add_terminal_unit_components(self, tu, tu_hay_id):
        """
        Given a models.TerminalUnit, generate records for all of the defined terminal unit components.
        components for a given terminal unit type are defined by the TerminalUnits.csv file.
        :param tu: A models.TerminalUnit
        :param tu_hay_id: The UUID of the terminal unit
        :return:
        """
        tu_type = self.sf.df_terminal_units[self.sf.df_terminal_units['id'] == tu.terminal_unit_type]
        damper = tu_type['damperComponentID'].values[0]
        hc = tu_type['heatingComponentID'].values[0]
        cc = tu_type['coolingComponentID'].values[0]

        self.gen_component_record(tu, damper, tu_hay_id, "Damper")
        self.gen_component_record(tu, hc, tu_hay_id, "Heating Coil")
        self.gen_component_record(tu, cc, tu_hay_id, "Cooling Coil")

    def add_ahu_components(self, ahu, ahu_hay_id):
        """
        Given a models.AirHandler, generate records for all of the defined ahu components.
        components with 'None' do not get generated.
        :param ahu: A models.AirHandler for which components should be added
        :type ahu: models.AirHandler
        :param ahu_hay_id: The UUID of the ahu.
        :return:
        """
        self.gen_component_record(ahu, ahu.pre_heat_coil, ahu_hay_id, "Preheat Coil")
        self.gen_component_record(ahu, ahu.supp_heat_coil, ahu_hay_id, "Supp Heating Coil")
        self.gen_component_record(ahu, ahu.heating_coil_type, ahu_hay_id, "Heating Coil")
        self.gen_component_record(ahu, ahu.cooling_coil_type, ahu_hay_id, "Cooling Coil")
        self.gen_component_record(ahu, ahu.discharge_fan_type, ahu_hay_id, "Discharge Fan")
        self.gen_component_record(ahu, ahu.return_fan_type, ahu_hay_id, "Return Fan")
        self.gen_component_record(ahu, ahu.exhaust_fan_type, ahu_hay_id, "Exhaust Fan")

    def gen_component_record(self, equip, component, equip_ref, component_type):
        """
        Generate a record for a given component as a sub-equip of the defined equip_ref.
        The 'typing' tags for the component record
        are generated via the 'Final Tagset' specified in Components.csv.
        :param equip: The model of the parent equip.
        :type equip: models.AirHandler or models.TerminalUnit
        :param str component: The id of the component to look up in Components.csv
        :param str equip_ref: A UUID to use as the equipRef for the component
        :param str component_type: A generic component description, for use in the 'dis' field
        :return:
        """
        if component and component != "None":
            hay_id = uuid4()
            temp = {
                "id": f"r:{hay_id}",
                "dis": f"s:{equip.name} {component_type}",
                "equipRef": f"r:{equip_ref}",
            }
            comp_def = self.sf.df_components[self.sf.df_components['id'] == component]
            if comp_def.empty:
                raise ComponentNotFoundError(component)
            tags = comp_def['Final Tagset'].values[0]
            tags = tags.split(" ")
            for tag in tags:
                if ":" in tag:
                    t = tag.split(":")
                    if self.is_number(t[1]):
                        temp[t[0]] = f"n:{t[1]}"
                    else:
                        temp[t[0]] = f"s:{t[1]}"
                else:
                    temp[tag] = "m:"
            self.hay_json.append(temp)

    def is_number(self, n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    def build(self):
        self.gen_site_record()
        self.gen_ahu_records()

    # def build_ahu(self, ahu, equip_ref):
    #     hay_json = []
    #     id = uuid4()
    #     hay_json.append({
    #         "id": f"r:{id}",
    #         "dis": ahu.name,
    #         "equip": "m:",
    #         "ahu": "m:",
    #         "equipRef": f"r:{equip_ref}"
    #     })
    #     return hay_json


# class Builder:
#     def __init__(self):
#         self.df = pd.ExcelFile('Templating-003.xlsx')
#         self.df_components = pd.read_excel(self.df, 'Components')
#         self.df_ahus = pd.read_excel(self.df, 'AHUs')
#         self.df_points = pd.read_excel(self.df, 'Points')
#         self.components = {}
#         # self.df_components['id'] = self.df_components['id'].map(lambda x: int(x))
#         # self.df_ahus['id'] = self.df_ahus['id'].map(lambda x: int(x))
#         # self.df_points['id'] = self.df_points['id'].map(lambda x: int(x))
#         self.haystack_json = []
#
#     def build_ahu(self, ahu_lookup_id):
#         test = self.df_ahus[self.df_ahus.id == ahu_lookup_id]
#         ahu_id = uuid4()
#         self.haystack_json.append({
#             "id": f"r:{ahu_id}",
#             "dis": f"BLAH BLAH",
#             "equip": "m:",
#             "ahu": "m:"
#         })
#         self.heating_coil_id = test['heatingCoilID'][0]
#         self.cooling_coil_id = test['coolingCoilID'][0]
#         self.discharge_fan_id = test['dischargeFanComponentID'][0]
#
#         self.component_ids = [
#             int(self.heating_coil_id),
#             int(self.cooling_coil_id),
#             int(self.discharge_fan_id)
#         ]
#
#         for component_id in self.component_ids:
#             self.add_component_to_ahu(component_id, ahu_id)
#
#         self.add_points_to_components()
#
#     def add_component_to_ahu(self, component_id, ahu_id):
#         id = f"r:{uuid4()}"
#         entity = {
#             "id": id,
#             "dis": f"s:Component {component_id}",
#             "equipRef": f"r:{ahu_id}"
#         }
#         comp = self.df_components[self.df_components.id == component_id]
#         tagset = comp['Final Tagset'].iloc[0].split(" ")
#         self.components[id] = set(tagset)
#         for t in tagset:
#             entity[t] = "m:"
#         self.haystack_json.append(entity)
#
#     def add_points_to_components(self):
#         fan_set = set(['fan', 'motor', 'equip'])
#         heating_coil_set = set(['heatingCoil', 'equip'])
#         cooling_coil_set = set(['coolingCoil', 'equip'])
#         for entity_id, entity_tagset in self.components.items():
#             if fan_set.issubset(entity_tagset):
#                 self.add_fan_points(entity_id, entity_tagset)
#             elif heating_coil_set.issubset(entity_tagset):
#                 self.add_heating_coil_points(entity_id, entity_tagset)
#             elif cooling_coil_set.issubset(entity_tagset):
#                 self.add_cooling_coil_points(entity_id, entity_tagset)

    # def add_fan_points(self, component_id, tagset):

class ComponentNotFoundError(Exception):
    def __init__(self, component_id):
        self.component_id = component_id
        self.message = f"Component with ID = {self.component_id} not found in df_components as imported from Components.csv.  Make sure 'Haste Choice' == True is specified."

    def __str__(self):
        return self.message


class TerminalUnitNotFoundError(Exception):
    def __init__(self, terminal_unit_id):
        self.terminal_unit_id = terminal_unit_id
        self.message = f"Terminal Unit with ID = {self.terminal_unit_id} not found in df_terminal_units as imported from TerminalUnits.csv."

    def __str__(self):
        return self.message
