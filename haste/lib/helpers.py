import pandas as pd
from uuid import uuid4

def generate_cooling_coils():
    cc = [
        {
            "id": 1,
            "description": "Cooling Coil 1",
            "tags": ["tag1", "tag2"]
        },
        {
            "id": 2,
            "description": "Cooling Coil 2",
            "tags": ["tag1", "tag2"]
        }
    ]
    return cc

def generate_heating_coils():
    hc = [
        {
            "id": 1,
            "description": "Heating Coil 1",
            "tags": ["tag1", "tag2"]
        },
        {
            "id": 2,
            "description": "Heating Coil 2",
            "tags": ["tag3", "tag4"]
        }
    ]
    return hc

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
