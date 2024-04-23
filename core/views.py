from datetime import datetime
from gettext import gettext

from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from core.models import Staff, GetIn


def index(request):
    return render(request, 'lock_screen.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('hasabat')
        else:
            messages.info(request, gettext('Maglumatlaryňyzy ýalnyş girizdiňiz!'))
            return redirect('login')
    else:
        return render(request, 'login.html')


def admin_logout(request):
    auth.logout(request)
    return redirect('/')


class StaffMembers(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'tables-data.html'
    context_object_name = 'staffs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@login_required(login_url='login')
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        profession = request.POST['profession']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        person_user = Staff.objects.create(fullname=name, profession=profession,
                                           mail=email, phone_number=phone_number)
        person_user.save()
        return redirect('staff_members')
    else:
        return render(request, 'forms-advanced.html')


class PersonView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'ui-cards.html'
    context_object_name = 'staffs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        _id = str(self.kwargs.get('slug'))
        staff = get_object_or_404(Staff, slug=_id)
        get_in = GetIn.objects.filter(person_id=staff)
        context['get_in'] = get_in
        return context


class PersonDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'tables-data.html'
    success_message = gettext('ulgamdan aýryldy')
    success_url = reverse_lazy('staff_members')

    def get_object(self, queryset=None):
        _id = str(self.kwargs.get('slug'))
        address = get_object_or_404(Staff, slug=_id)
        return address


class PersonUpdateView(UpdateView,LoginRequiredMixin):
    template_name = 'update.html'
    success_url = reverse_lazy('staff_members')
    success_message = gettext('ulgamda maglumaty üýtgedildi')
    fields = ['fullname', 'profession',  'mail', 'phone_number']

    def get_object(self, queryset=None):
        _id = str(self.kwargs.get('slug'))
        address = get_object_or_404(Staff, slug=_id)
        return address


@login_required(login_url='login')
def get_in_work(request):
    staff = Staff.objects.all()
    if request.method == 'POST':
        in_work = request.POST.getlist('in_work')
        for i in staff:
            if i.slug in in_work:
                df = GetIn.objects.filter(get_in_date=datetime.today().date(),person_id=i)
                if len(df) == 0:
                    get_in = GetIn.objects.create(person_id=i, in_work=True)
                    get_in.save()
            else:
                df = GetIn.objects.filter(get_in_date=datetime.today().date(),person_id=i)
                if len(df) == 0:
                    get_in = GetIn.objects.create(person_id=i, in_work=False)
                    get_in.save()
        df = GetIn.objects.filter(get_in_date=datetime.today().date())
        if df.__len__()==Staff.objects.all().__len__():
            messages.info(request,'Şu gün üçin maglumatlary girizdiňiz!')
        return redirect('hasabat')
    return render(request, 'giris_statistika.html', {'staff':staff})


@login_required(login_url='login')
def hasabat(request):
    getin = GetIn.objects.values_list('get_in_date',flat=True).distinct()
    geti = getin.order_by('get_in_date')
    staff = Staff.objects.all()
    return render(request, 'hasabat.html', {'staff':staff, 'geti': geti})


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(exception):
    data = {}
    return render('500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, '403.html', data)


def error_400(request, exception):
    data = {}
    return render(request, '400.html', data)


