from uuid import uuid4
from generate import models


def handle_haystack(data):

    data = data['rows']
    site = find_sites(data)
    site = site[0]

    equips = find_equips(data)
    print(equips)

    site_id = str(site.get('id')[2:])  # remove "r:" from UUID
    site_name = site.get('dis')
    geo_city = site.get('geoCity')
    geo_state = site.get('geoState')

    try:
        exists = models.Site.objects.get(id=site_id)
    except:
        id = uuid4()
        new_site = models.Site.objects.create(id=id, name=site_name, city=geo_city, state=geo_state, zip=0)
        new_site.save()


def handle_brick(data):
    pass


def handle_osm(data):
    pass


def find_sites(entities):
    sites = find_tagset(entities, tags=['site'])
    return sites


def find_equips(entities):
    equips = find_tagset(entities, tags=['equip'])
    return equips


def find_tagset(entities, tags):
    tags = set(tags)
    matches = [e for e in entities if tags.issubset(e.keys())]
    return matches



