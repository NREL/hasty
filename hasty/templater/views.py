from django.shortcuts import render, redirect
from django.views.generic import CreateView

from . import models as tm
from . import forms


# Create your views here.
class Index(CreateView):
    template_name = 'templater_index.html'

    def get(self, request):
        haystack_equip_templates = tm.HaystackEquipmentTemplate.objects.all()
        haystack_fault_templates = tm.HaystackFaultTemplate.objects.all()
        map = equipment_fault_template_mapper(
            haystack_fault_templates, haystack_equip_templates)
        brick_equipment_templates = tm.BrickEquipmentTemplate.objects.all()
        brick_fault_templates = tm.BrickFaultTemplate.objects.all()
        map.update(
            equipment_fault_template_mapper(
                brick_fault_templates,
                brick_equipment_templates))

        args = {
            'haystack_equipment_templates': haystack_equip_templates,
            'brick_equipment_templates': brick_equipment_templates,
            'haystack_fault_templates': haystack_fault_templates,
            'brick_fault_templates': brick_fault_templates,
            'map': map
        }
        return render(request, self.template_name, args)

    def post(self, request):
        return handle_index_post(request)


class HaystackCreateEquipmentTemplateView(CreateView):
    template_name = 'templater_create_equipment.html'

    def get(self, request):
        form = forms.HaystackEquipmentTemplateForm()

        args = {
            'mt': "Haystack",
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = forms.HaystackEquipmentTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('templater.index')


class BrickCreateEquipmentTemplateView(CreateView):
    template_name = 'templater_create_equipment.html'

    def get(self, request):
        form = forms.BrickEquipmentTemplateForm()

        args = {
            'mt': "Brick",
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = forms.BrickEquipmentTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('templater.index')


class HaystackCreateFaultTemplateView(CreateView):
    template_name = 'templater_create_fault.html'

    def get(self, request):
        form = forms.HaystackFaultTemplateForm()

        args = {
            'mt': "Haystack",
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = forms.HaystackFaultTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('templater.index')


class BrickCreateFaultTemplateView(CreateView):
    template_name = 'templater_create_fault.html'

    def get(self, request):
        form = forms.BrickFaultTemplateForm()

        args = {
            'mt': "Brick",
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = forms.BrickFaultTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('templater.index')


def handle_index_post(request):
    mt = request.POST.get('model_type')
    if 'delete_haystack_equipment' in request.POST:
        return index_delete(tm.HaystackEquipmentTemplate, request)
    elif 'delete_brick_equipment' in request.POST:
        return index_delete(tm.BrickEquipmentTemplate, request)
    elif 'delete_haystack_fault' in request.POST:
        return index_delete(tm.HaystackFaultTemplate, request)
    elif 'delete_brick_fault' in request.POST:
        return index_delete(tm.BrickFaultTemplate, request)
    elif 'create_equipment' in request.POST:
        return redirect(f"templater.{mt}.create_equipment_template")
    elif 'create_fault' in request.POST:
        return redirect(f"templater.{mt}.create_fault_template")


def index_delete(template, request):
    if request.POST.get('id'):
        to_delete = template.objects.get(id=request.POST.get('id'))
        to_delete.delete()
    return redirect('templater.index')


def equipment_fault_template_mapper(fault_templates, equipment_templates):
    mapping = {}
    for ft in fault_templates:
        ets = equipment_templates.filter(
            version=ft.version, equipment_type=ft.equipment_type)
        matches = []
        for et in ets:
            et_point_set = set(et.points.all())
            ft_point_set = set(ft.points.all())
            if ft_point_set.issubset(et_point_set):
                matches.append(et)
        if len(matches) > 0:
            mapping[ft] = matches
    return mapping
