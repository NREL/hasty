import os
import yaml

from django.db.models import Count

from mapp.models import HaystackVersion, HaystackPointType, HaystackEquipmentType
from templater.models import HaystackEquipmentTemplate


def add_equipment_templates_migration(apps, schema_editor):
    add_equipment_templates()


def add_equipment_templates():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "equip-templates")
    template_files = [os.path.join(p, f) for f in os.listdir(p) if f.endswith("-templates.yaml")]
    for f in template_files:
        with open(f, 'r') as fp:
            templates = yaml.load(fp, Loader=yaml.FullLoader)
        for t in templates:
            d = t['template']
            if valid_template(d):
                print(f"Processing template: {d['name']}")
                if d['type'] == 'Haystack':
                    v = HaystackVersion.objects.filter(version=d['version'])
                    if len(v) == 1:
                        v = v[0]
                        et = HaystackEquipmentType.objects.filter(haystack_tagset=d['equipment_type'], version=v)
                        if len(et) == 1:
                            et = et[0]
                            equip_template = HaystackEquipmentTemplate(name=d['name'], version=v,
                                                                       description=d.get('description', ""),
                                                                       equipment_type=et)
                            equip_template.save()
                            points = d.get('points', False)
                            if points:
                                add_points(points, equip_template, HaystackPointType)
                            else:
                                print(f"No points to add for {d['name']}")
                        else:
                            print(f"No template created for: {d['name']}")

                    else:
                        print(f"No template created for: {d['name']}")
                else:
                    print(f"Invalid type: {d['type']}")
            else:
                print(f"Invalid template: {t}")


def valid_template(template):
    t = template.get('type', None)
    v = template.get('version', None)
    n = template.get('name', None)
    et = template.get('equipment_type', None)
    p = template.get('points', None)
    if None in [t, v, n, et, p]:
        return False
    else:
        return True


def add_points(points, equip_template, hpt):
    for p in points:
        tags = p.split("-")
        if len(tags) == len(set(tags)):
            candidates = hpt.objects.annotate(c=Count('marker_tags')).filter(c=len(tags))
            for tag in tags:
                candidates = candidates.filter(marker_tags__tag=tag)
            if len(candidates) == 1:
                equip_template.points.add(candidates[0])
                print(f"Point added: {p}")
            elif len(candidates) == 0:
                print(f"Point not saved. No point type matching: {p}.")
            else:
                print(f"Point not saved.  Multiple candidates matching: {p} - not unique.")
        else:
            print(f"Point not saved.  Duplicate tags in: {p}.")
