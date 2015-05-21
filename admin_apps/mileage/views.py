# mileage/views.py
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import detail
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from mileage.models import Trip, PayPeriod
#from mileage.models import User

from braces import views

from mileage.forms import TripStartForm, PayPeriodAddForm

class PayPeriodDisplay(generic.ListView):
    model = PayPeriod
    def get_context_data(self, **kwargs):
        context = super(PayPeriodDisplay, self).get_context_data(**kwargs)
        context['payperiods']=PayPeriod.objects.all()
        context['current']=PayPeriod.get_current_pay_period()
        context['form']=PayPeriodAdmin
        return context

    def get_queryset(self):
        queryset = super(PayPeriodDisplay, self).get_queryset()
        queryset = queryset.order_by('-due')
        return queryset


class PayPeriodAdd(generic.CreateView):

    model = PayPeriod
    fields = ('due')

    
    def get_success_url(self):
        #redirects to edit to add trip end
        return reverse('mileage:payperiod', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PayPeriodAdd, self).form_valid(form)


class TripDisplay(
    generic.ListView):
    """
    Handles get() for the TripList View.
    """
    model = Trip
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TripDisplay, self).get_context_data(**kwargs)
        context['form'] = TripStartForm
        return context

    def get_queryset(self):
        queryset = super(TripDisplay, self).get_queryset()
        queryset = queryset.order_by('-created')
        return queryset

class TripAdd(
    generic.CreateView):
    """
    Handles post() in for the TripList View. Allows addition of trips.
    """

    template_name = 'mileage/trip_list.html'
    model = Trip
    fields = ('trip_begin', 'description')
    def get_success_url(self):
        #redirects to edit to add trip end
        return reverse('mileage:edit', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TripAdd, self).form_valid(form)

class TripList(generic.View):
    """
    View that is sent to URLConf to split the class into two CBV
    """
    Trip.objects.order_by('-create')
    def get(self, request, *args, **kwargs):
        view = TripDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TripAdd.as_view()
        return view(request, *args, **kwargs)

class PayPeriodList(generic.View):
    """
    View that is sent to URLConf to split the class into two CBV
    """
    PayPeriod.objects.order_by('-due')
    def get(self, request, *args, **kwargs):
        view = PayPeriodDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PayPeriodAdd.as_view()
        return view(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mileage:payperiodlist')


class TripEdit(generic.UpdateView):
    template_name = 'mileage/trip_edit.html'
    model = Trip
    fields = ['trip_end']
    def get_success_url(self):
        return reverse('mileage:list')
        

