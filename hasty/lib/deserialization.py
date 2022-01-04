from uuid import uuid4
from generate import models
import re


def handle_haystack(data):
    data = data['rows']
    site = find_sites(data)
    ahus = find_ahus(data)
    vavs = find_vavs(data)

    site_id = save_site(site)
    save_ahus(ahus, site_id, vavs)
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


def find_vavs(entities):
    vavs = find_tagset(entities, tags=['vav'])
    return vavs


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
    geo_state = strip_prefix.match(site.get('geoState'))[2] if site.get('geoState') else None  # remove leading *:

    try:
        models.Site.objects.get(id=site_id)
    except BaseException:
        id = uuid4()
        imported_site = models.Site.objects.create(id=id, name=site_name, city=geo_city, state=geo_state, zip=0)
        imported_site.save()
        return id


def save_ahus(ahus, site_id, vavs):

    site = models.Site.objects.get(id=site_id)
    for ahu in ahus:
        ahu_id = uuid4()
        ahu_name = ahu.get('dis')
        if ahu_name is None:
            ahu_name = ahu.get('id')

        imported_ahu = models.AirHandler.objects.create(id=ahu_id, name=ahu_name,
                                                        site_id=site, tagset=None, brick_class=None)
        imported_ahu.save()

        for vav in vavs:
            if ahu.get('id') == vav.get('equipRef'):
                name = vav.get('dis')
                name = name.replace(" ", "_")
                imported_vav = models.TerminalUnit(
                    name=name,
                    lookup_id=vav.get('id'),
                    is_fed_by=imported_ahu
                )
                imported_vav.save()
                new_tz = models.ThermalZone(
                    name="Zone",
                    brick_class="HVAC_Zone",
                    is_fed_by=imported_vav
                )
                new_tz.save()
