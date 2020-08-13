from django.shortcuts import render, redirect
from django.views.generic import CreateView

from . import models as tm
from . import forms


# Create your views here.
class Index(CreateView):
    template_name = 'templater_index.html'

    def get(self, request):
        haystack_equip_templates = tm.HaystackEquipmentTemplate.objects.all()

        args = {
            'haystack_equipment_templates': haystack_equip_templates
        }
        return render(request, self.template_name, args)

    def post(self, request):
        mt = request.POST.get('model_type')
        if 'delete_haystack_equipment' in request.POST:
            if request.POST.get('id'):
                to_delete = tm.HaystackEquipmentTemplate.objects.get(id=request.POST.get('id'))
                to_delete.delete()
            return redirect('templater.index')
        elif 'delete_brick_equipment' in request.POST:
            return redirect('templater.index')
        elif 'create_equipment' in request.POST:
            return redirect(f"templater.{mt}.create_equipment_template")

        elif 'create_fault' in request.POST:
            # TODO
            print("create_fault not yet handled")

        print(mt)


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
        form = forms.HaystackEquipmentTemplateForm()

        args = {
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = forms.HaystackEquipmentTemplateForm(request.POST)
        if form.is_valid():
            form.save()

# class SelectPointsView(CreateView):
#     template_name = 'templater_select_points.html'
#
#     def get(self, request):
#         args = {
#
#         }
#         return render(request, self.template_name, args)
