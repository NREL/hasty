from uuid import uuid4
from generate import models
import re
import os
import json
from lib.helpers import Shadowfax, json_dump_tags_from_string


def handle_haystack(data):
    data = data['rows']
    site = find_sites(data)
    ahus = find_ahus(data)
    terminal_units = find_cavs(data)
    terminal_units += find_vavs(data)
    components = find_components(data)
    thermal_zones = find_tagset(data, tags=['hvac', 'zone', 'space'])
    reheat = find_tagset(data, tags=['reheats', 'equipRef'])
    points = find_tagset(data, tags=['point', 'equipRef'])
    print(reheat)

    site_id = save_site(site)
    save_ahus(ahus, site_id, terminal_units,
              components, thermal_zones, reheat, points)
    return site_id


def handle_brick(data):
    print(data)


def handle_osm(data):
    print(data)


def find_sites(entities):
    sites = find_tagset(entities, tags=['site'])
    return sites


def find_equips(entities):
    equips = find_tagset(entities, tags=['equip'])
    return equips


def find_ahus(entities):
    ahus = find_tagset(entities, tags=['ahu'])
    return ahus


def find_cavs(entities):
    cavs = find_tagset(entities, tags=['cav'])
    return cavs


def find_vavs(entities):
    vavs = find_tagset(entities, tags=['vav'])
    return vavs


def find_components(entities):
    s = Shadowfax()
    ignore_tags = set(['id', 'dis', 'equipRef', 'airRef'])
    valid_tagsets = [set(tagset.split(' '))
                     for tagset in s.df_components['Final Tagset']]
    components = [e for e in entities if set(
        e.keys()) - ignore_tags in valid_tagsets]
    return components


def find_tagset(entities, tags):
    tags = set(tags)
    matches = [e for e in entities if tags.issubset(e.keys())]
    return matches


def save_site(site):
    site = site[0]
    strip_prefix = re.compile("([a-z]\\:)?(.*)")
    site_id = strip_prefix.match(str(site.get('id')))[2]  # remove leading r:
    site_name = site.get('dis')
    geo_city = site.get('geoCity')
    # remove leading *:
    geo_state = strip_prefix.match(site.get('geoState'))[
        2] if site.get('geoState') else None

    try:
        models.Site.objects.get(id=site_id)
    except BaseException:
        id = uuid4()
        imported_site = models.Site.objects.create(
            id=id, name=site_name, city=geo_city, state=geo_state, zip=0)
        imported_site.save()
        return id


def save_ahus(ahus, site_id, terminal_units, components, thermal_zones, reheat, points):
    ignore_tags = set(['id', 'dis', 'equipRef', 'airRef'])
    s = Shadowfax()
    site = models.Site.objects.get(id=site_id)
    for ahu in ahus:
        ahu_id = uuid4()
        ahu_name = ahu.get('dis')
        if ahu_name is None:
            ahu_name = ahu.get('id')

        imported_ahu = models.AirHandler.objects.create(id=ahu_id, name=ahu_name,
                                                        site_id=site, tagset=None, brick_class=None)
        imported_ahu.save()

        def add_component(entity, component_lookup_id, component_class):
            temp = s.df_components[s.df_components['id']
                                   == component_lookup_id]
            name = entity.get('dis')
            dis = temp['Description'].values[0]
            tags = temp['Final Tagset'].values[0]
            tagset = json_dump_tags_from_string(tags)
            brick = temp['Brick Concept'].values[0]
            c = component_class(
                name=name,
                lookup_id=component_lookup_id,
                short_description=dis,
                is_part_of=imported_ahu,
                tagset=tagset,
                brick_class=brick
            )
            c.save()
        for point in points:
            if ahu.get('id') == point.get('equipRef'):
                tags = ' '.join(list(set(point.keys()) - ignore_tags))
                imported_point = models.Point(
                    name=point.get('dis').replace(' ', '_'),
                    is_point_of=imported_ahu,
                    tagset=json_dump_tags_from_string(tags)
                )
                imported_point.save()
        for terminal_unit in terminal_units:
            if ahu.get('id') == terminal_unit.get('airRef'):
                name = terminal_unit.get('dis')
                name = name.replace(" ", "_")
                imported_terminal_unit = models.TerminalUnit(
                    name=name,
                    lookup_id=models.TerminalUnit.tu_choices[0][0],
                    is_fed_by=imported_ahu
                )
                for component in reheat:
                    if component.get('equipRef') == terminal_unit.get('id'):
                        imported_terminal_unit.lookup_id = models.TerminalUnit.tu_choices[2][0]

                imported_terminal_unit.save()
                for thermal_zone in thermal_zones:
                    if terminal_unit.get('id') != thermal_zone.get('airRef'):
                        continue
                    new_tz = models.ThermalZone(
                        name=thermal_zone.get('dis').replace(" ", "_"),
                        brick_class="HVAC_Zone",
                        is_fed_by=imported_terminal_unit
                    )
                    new_tz.save()

        component_class_tagsets = [{'df': s.df_hc, 'class': models.HeatingCoil},
                                   {'df': s.df_cc, 'class': models.CoolingCoil},
                                   {'df': s.df_dis_fan, 'class': models.DischargeFan},
                                   {'df': s.df_exh_fan, 'class': models.ExhaustFan},
                                   {'df': s.df_ret_fan, 'class': models.ReturnFan}
                                   ]
        component_class_tagsets = [{'df': item['df'], 'class': item['class'], 'tagset': [set(
            tagset.split(' ')) for tagset in item['df']['Final Tagset']]} for item in component_class_tagsets]
        for component in components:
            if ahu.get('id') == component.get('equipRef'):
                name = component.get('dis').replace(" ", "_")
                tags = set(component.keys()) - ignore_tags
                for component_class_tagset in component_class_tagsets:
                    tagset = component_class_tagset['tagset']
                    if tags in tagset:
                        component_lookup_id = list(component_class_tagset['df']['id'])[
                            tagset.index(tags)]
                        add_component(component, component_lookup_id,
                                      component_class_tagset['class'])


def handle_template(path):
    p = os.path.dirname(os.path.abspath(__file__))
    f_path = os.path.join(p, path)
    with open(f_path) as json_file:
        data = json.loads(json_file.read())
        site_id = handle_haystack(data)

    return site_id


def file_processing(file):
    """
    - get file extension
    - if file ext is json
        - if uuid4 id already exists
            - just load the file as a copy with a new uuid4
        - else we need to create a whole new model instance
            - unserialize(file)?
              what styles of haystack json are there
    - elif file ext is osm
        - unserialize(file)?
    - elif file ext is idf
        - unserialize(file)?
    """

    data = json.load(file)
    handle_haystack(data)
