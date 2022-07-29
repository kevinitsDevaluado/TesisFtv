import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.clinic.models import Mascots, BreedPet
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class MascotsReportView(ModuleMixin, FormView):
    template_name = 'mascots_report/report.html'
    form_class = ReportForm

    def get_form(self, form_class=None):
        form = ReportForm()
        list_BreedPet = [('', '---------')]
        for b in BreedPet.objects.all():
            list_BreedPet.append((b.id, b.format_name()))
        form.fields['breedpet'].choices = list_BreedPet
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        data = {}
        try:
            if action == 'search_report':
                data = []
                term = self.request.POST['term']
                breedpet = self.request.POST['breedpet']
                search = Mascots.objects.filter()
                if len(term):
                    search = search.filter(name__icontains=term)
                if len(breedpet):
                    search = search.filter(breed_id=breedpet)
                for i in search:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Mascotas'
        return context
