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
        self.df_hc_cc = self.df_components[self.df_components['Category'] == 'Heating cooling coil']
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

    def generate_heating_cooling_coils(self):
        """
        Generate a list of dicts for the different types of potential heating / cooling coils.
        :return:
        """
        return self.df_hc_cc.to_dict('records')

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
            'coil_configurations': [
                self.hc_name_given_id(ahu_model.heating_coil_type),
                self.cc_name_given_id(ahu_model.cooling_coil_type),
                self.hc_cc_name_given_id(ahu_model.heating_cooling_coil_type)
            ],
            'fan_configurations': [
                self.df_name_given_id(ahu_model.discharge_fan_type),
                self.rf_name_given_id(ahu_model.return_fan_type),
                self.ef_name_given_id(ahu_model.exhaust_fan_type)
            ],
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
        :param hc_id: The id of the heating coil
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
        :param cc_id: The id of the cooling coil
        :return: str
        """
        ccs = self.generate_cooling_coils()
        for cc in ccs:
            if cc_id == cc['id']:
                return cc['Description']
        return None

    def hc_cc_name_given_id(self, hc_cc_id):
        """
        Return the human readable version of the heating cooling coil given its id.
        :param hc_cc_id: The id of the heating cooling coil
        :return: str
        """
        hc_ccs = self.generate_heating_cooling_coils()
        for hc_cc in hc_ccs:
            if hc_cc_id == hc_cc['id']:
                return hc_cc['Description']
        return None

    def df_name_given_id(self, df_id):
        """
        Return the human readable version of the discharge fan given its id.
        :param df_id: The id of the discharge fan
        :return: str
        """
        dfs = self.generate_discharge_fans()
        for df in dfs:
            if df_id == df['id']:
                return df['Description']
        return None

    def ef_name_given_id(self, ef_id):
        """
        Return the human readable version of the exhaust fan given its id.
        :param ef_id: The id of the exhaust fan
        :return: str
        """
        efs = self.generate_exhaust_fans()
        for ef in efs:
            if ef_id == ef['id']:
                return ef['Description']
        return None

    def rf_name_given_id(self, rf_id):
        """
        Return the human readable version of the cooling coil given its id.
        :param rf_id: The id of the return fan
        :return: str
        """
        rfs = self.generate_return_fans()
        for rf in rfs:
            if rf_id == rf['id']:
                return rf['Description']
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
        self.gen_component_record(ahu, ahu.heating_cooling_coil_type, ahu_hay_id, "Heating Cooling Coil")
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