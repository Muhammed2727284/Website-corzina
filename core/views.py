from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from .models import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *


# list dog

# Create your views here.
@login_required
def core(request):
    return render(request, 'core.html')


class CreateDolg(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Dolg
    form_class = DolgForm
    template_name = 'create/create-dolg.html'
    success_url = reverse_lazy('list-dolg')

class ListDolg(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')  # URL to redirect to for login

    def get(self, request):
        object_list = Dolg.objects.filter(is_history=False)
        return render(request, 'list/list-dolg.html', {'object_list': object_list})



class DetailDolg(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Dolg
    template_name = 'detail/detail-dolg.html'
    context_object_name = 'object'
    pk_url_kwarg = 'id'


class UpdateDolg(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Dolg
    form_class = DolgForm
    template_name = 'update/update-dolg.html'
    success_url = reverse_lazy('list-dolg')
    pk_url_kwarg = 'id'


class DeleteDolg(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Dolg
    template_name = 'delete/delete-dolg.html'
    success_url = reverse_lazy('list-dolg')
    pk_url_kwarg = 'id'


# def successPay(request, id):
#     dolg = Dolg.objects.get(id=id)
#     dolg.is_history = True
#     dolg.save()
#
#     if dolg.is_history == True:
#         HttpResponse("клиент уже оплатил(а)")
#     return HttpResponse("оплата")

@login_required
def successPay(request, id):
    try:
        dolg = Dolg.objects.get(id=id)
    except Dolg.DoesNotExist:
        return HttpResponse("Запись не найдена", status=404)
    if dolg.is_history:
        return HttpResponse("Клиент уже оплатил(а)")
    dolg.is_history = True
    dolg.save()
    link = 'list-dolg'
    return HttpResponse("Оплата успешно произведена")


# history
@login_required
def history_list(request):
    history = Dolg.objects.filter(is_history=True)
    return render(request, 'list/history-list.html', {'history': history})

@login_required
def history_detail(request, id):
    hist = Dolg.objects.get(id=id)
    return render(request, 'detail/history-detail.html', {'object': hist})

@login_required
def recovery_history(request, id):
    try:
        history = Dolg.objects.get(id=id)
    except Dolg.DoesNotExist:
        return HttpResponse("Запись не найдена", status=404)

    history.is_history = False
    history.save()
    if history.is_history:
        return HttpResponse("Клиент Находится в история")
    link = 'history-list'
    return HttpResponse("Данные успешно востоновлено")




