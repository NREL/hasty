import os
import yaml

from django.db.models import Count

from mapp.models import HaystackVersion, HaystackPointType, HaystackEquipmentType, BrickVersion, BrickPointType, \
    BrickEquipmentType
from templater.models import HaystackEquipmentTemplate, BrickEquipmentTemplate, HaystackFaultTemplate, \
    BrickFaultTemplate


def add_equipment_templates_migration(apps, schema_editor):
    add_templates('equip-templates', 'equipment')


def add_fault_templates_migration(apps, schema_editor):
    add_templates('fault-templates', 'fault')


def add_templates(template_dir, template_type):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{template_dir}")
    template_files = [os.path.join(p, f) for f in os.listdir(p) if f.endswith("-templates.yaml")]
    for f in template_files:
        with open(f, 'r') as fp:
            templates = yaml.load(fp, Loader=yaml.FullLoader)
        for t in templates:
            d = t['template']
            if valid_template(d):
                print(f"Processing template: {d['name']}")
                if d['type'] == 'Haystack':
                    version = check_single_version(HaystackVersion, d)
                    if not version:
                        continue
                    equipment_type = HaystackEquipmentType.objects.filter(haystack_tagset=d['equipment_type'],
                                                                          version=version)
                    if len(equipment_type) != 1:
                        print(
                            f"{len(equipment_type)} HaystackEquipmentType's found.  Template not added for {[d['name']]}")
                        continue
                    if template_type == 'equipment':
                        template = create_equipment_template(HaystackEquipmentTemplate, d, version,
                                                             equipment_type)
                    elif template_type == 'fault':
                        template = create_fault_template(HaystackFaultTemplate, d, version, equipment_type)
                    add_points('Haystack', d, template, HaystackPointType.objects.filter(version=version))
                elif d['type'] == 'Brick':
                    version = check_single_version(BrickVersion, d)
                    if not version:
                        continue
                    equipment_type = BrickEquipmentType.objects.filter(brick_class=d['equipment_type'], version=version)
                    if len(equipment_type) != 1:
                        print(
                            f"{len(equipment_type)} BrickEquipmentType's found.  Template not added for {[d['name']]}")
                        continue
                    if template_type == 'equipment':
                        template = create_equipment_template(BrickEquipmentTemplate, d, version, equipment_type)
                    elif template_type == 'fault':
                        template = create_fault_template(HaystackFaultTemplate, d, version, equipment_type)
                    add_points('Brick', d, template, BrickPointType.objects.filter(version=version))
                else:
                    print(f"Invalid type: {d['type']}")
            else:
                print(f"Invalid template: {t}")


def create_fault_template(template_object, data, version, equipment_type):
    equipment_type = equipment_type[0]
    fault_template = template_object(name=data['name'], version=version,
                                     description=data.get('description', ''),
                                     equipment_type=equipment_type,
                                     logic=data.get('logic', ''))
    fault_template.save()
    return fault_template


def create_equipment_template(template_object, data, version, equipment_type):
    equipment_type = equipment_type[0]
    equipment_template = template_object(name=data['name'], version=version,
                                         description=data.get('description', ""),
                                         equipment_type=equipment_type)
    equipment_template.save()
    return equipment_template


def valid_template(template, ):
    t = template.get('type', None)
    v = template.get('version', None)
    n = template.get('name', None)
    et = template.get('equipment_type', None)
    p = template.get('points', None)
    to_check = [t, v, n, et, p]
    if None in to_check:
        return False
    else:
        return True


def check_single_version(version_object, data):
    v = version_object.objects.filter(version=data['version'])
    if len(v) == 1:
        return v[0]
    else:
        print(f"{len(v)} {version_object}'s found.  Template not added for {data['name']}")
        return False


def add_points(model_type, data, template, point_type):
    points = data.get('points', False)
    if points and model_type == 'Haystack':
        add_haystack_points(points, template, point_type)
    elif points and model_type == 'Brick':
        add_brick_points(points, template, point_type)
    else:
        print(f"No points to add for {data['name']}")


def add_haystack_points(points, equip_template, hpt):
    for p in points:
        tags = p.split("-")
        if len(tags) == len(set(tags)):
            candidates = hpt.annotate(c=Count('marker_tags')).filter(c=len(tags))
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


def add_brick_points(points, equip_template, bpt):
    for p in points:
        candidates = bpt.filter(brick_class=p)
        if len(candidates) == 1:
            equip_template.points.add(candidates[0])
            print(f"Point added: {p}")
        elif len(candidates) == 0:
            print(f"Point not saved. No point type matching: {p}.")
        else:
            print(f"Point not saved.  Multiple candidates matching: {p} - not unique.")
