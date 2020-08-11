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
        if mt == 'haystack':
            return redirect('templater.haystack.create_equipment_template')
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

    def post(self, request, model_type):
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

    def post(self, request, model_type):
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
