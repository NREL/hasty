import pandas as pd
from uuid import uuid4
from generate import models


def generate_cooling_coils():
    """
    Generate a list of dicts for the different types of potential cooling coils.
    :return:
    """
    cc = [
        {
            "id": 'CC-001',
            "description": "Cooling Coil 1",
            "tags": ["tag1", "tag2"]
        },
        {
            "id": 'CC-002',
            "description": "Cooling Coil 2",
            "tags": ["tag1", "tag2"]
        }
    ]
    return cc


def generate_heating_coils():
    """
    Generate a list of dicts for the different types of potential heating coils.
    :return:
    """
    hc = [
        {
            "id": 'HC-001',
            "description": "Heating Coil 1",
            "tags": ["tag1", "tag2"]
        },
        {
            "id": 'HC-002',
            "description": "Heating Coil 2",
            "tags": ["tag3", "tag4"]
        }
    ]
    return hc


def generate_terminal_unit_types():
    """
    Generate a list of dicts for the different types of potential terminal units.
    :return:
    """
    tu = [
        {
            "id": 'TU-001',
            "category": "VAV",
            "description": "VAV Box Cooling Only",
            "tags": ["tag1", "tag2"]
        },
        {
            "id": 'TU-002',
            "category": "CAV",
            "description": "CAV Terminal Unit",
            "tags": ["tag1", "tag2"]
        }
    ]
    return tu


def ahu_summary_info(ahu_model):
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
        'hc_name': hc_name_given_id(ahu_model.heating_coil_type),
        'cc_name': cc_name_given_id(ahu_model.cooling_coil_type),
        'num_terminal_units': num_tus
    }
    return data


def terminal_unit_summary_info(terminal_unit_model):
    """
    Return summary info for the TerminalUnit for displaying in the 'all_terminal_units.html' page
    :param terminal_unit_model: A single TerminalUnit model
    :return: dict
    """
    data = {
        'id': terminal_unit_model.id,
        'name': terminal_unit_model.name,
        'type': tu_name_given_id(terminal_unit_model.terminal_unit_type)
    }
    return data


def tu_name_given_id(tu_id):
    tus = generate_terminal_unit_types()
    for tu in tus:
        if tu_id == tu['id']:
            return tu['description']
    return None


def hc_name_given_id(hc_id):
    """
    Return the human readable version of the heating coil given its id.
    :param hc_id: The id of the heating coil as returned by generate_heating_coils()
    :return: str
    """
    hcs = generate_heating_coils()
    for hc in hcs:
        if hc_id == hc['id']:
            return hc['description']
    return None


def cc_name_given_id(cc_id):
    """
    Return the human readable version of the cooling coil given its id.
    :param cc_id: The id of the heating coil as returned by generate_cooling_coils()
    :return: str
    """
    ccs = generate_cooling_coils()
    for cc in ccs:
        if cc_id == cc['id']:
            return cc['description']
    return None

class Test:
    def __init__(self):
        pass

    def return_data(self):
        data = [
            {"testers": 1},
            {"testersss": 2}
        ]
        return data

class Builder:
    def __init__(self):
        self.df = pd.ExcelFile('Templating-003.xlsx')
        self.df_components = pd.read_excel(self.df, 'Components')
        self.df_ahus = pd.read_excel(self.df, 'AHUs')
        self.df_points = pd.read_excel(self.df, 'Points')
        self.components = {}
        # self.df_components['id'] = self.df_components['id'].map(lambda x: int(x))
        # self.df_ahus['id'] = self.df_ahus['id'].map(lambda x: int(x))
        # self.df_points['id'] = self.df_points['id'].map(lambda x: int(x))
        self.haystack_json = []

    def build_ahu(self, ahu_lookup_id):
        test = self.df_ahus[self.df_ahus.id == ahu_lookup_id]
        ahu_id = uuid4()
        self.haystack_json.append({
            "id": f"r:{ahu_id}",
            "dis": f"BLAH BLAH",
            "equip": "m:",
            "ahu": "m:"
        })
        self.heating_coil_id = test['heatingCoilID'][0]
        self.cooling_coil_id = test['coolingCoilID'][0]
        self.discharge_fan_id = test['dischargeFanComponentID'][0]

        self.component_ids = [
            int(self.heating_coil_id),
            int(self.cooling_coil_id),
            int(self.discharge_fan_id)
        ]

        for component_id in self.component_ids:
            self.add_component_to_ahu(component_id, ahu_id)

        self.add_points_to_components()

    def add_component_to_ahu(self, component_id, ahu_id):
        id = f"r:{uuid4()}"
        entity = {
            "id": id,
            "dis": f"s:Component {component_id}",
            "equipRef": f"r:{ahu_id}"
        }
        comp = self.df_components[self.df_components.id == component_id]
        tagset = comp['Final Tagset'].iloc[0].split(" ")
        self.components[id] = set(tagset)
        for t in tagset:
            entity[t] = "m:"
        self.haystack_json.append(entity)

    def add_points_to_components(self):
        fan_set = set(['fan', 'motor', 'equip'])
        heating_coil_set = set(['heatingCoil', 'equip'])
        cooling_coil_set = set(['coolingCoil', 'equip'])
        for entity_id, entity_tagset in self.components.items():
            if fan_set.issubset(entity_tagset):
                self.add_fan_points(entity_id, entity_tagset)
            elif heating_coil_set.issubset(entity_tagset):
                self.add_heating_coil_points(entity_id, entity_tagset)
            elif cooling_coil_set.issubset(entity_tagset):
                self.add_cooling_coil_points(entity_id, entity_tagset)

    # def add_fan_points(self, component_id, tagset):


if __name__ == "__main__":
    b = Builder()
    b.build_ahu(1)
