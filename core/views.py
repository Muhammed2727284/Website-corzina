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
from django.contrib.auth import logout
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404

def custom_404_view(request, exception):
    return render(request, '404/404.html', status=404)

# list dog
@login_required
def core(request):
    return render(request, 'core.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


class CreateDolg(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Dolg
    form_class = DolgForm
    template_name = 'create/create-dolg.html'
    success_url = reverse_lazy('list-dolg')

    def form_valid(self, form):
        # Получаем текущего пользователя
        user_index_magazine = self.request.user.userindexmagazine_set.first()

        # Устанавливаем пользователя для объекта Dolg
        form.instance.user = user_index_magazine

        # Вызываем родительский метод для сохранения формы
        return super().form_valid(form)

class ListDolg(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')  # URL to redirect to for login

    def get(self, request):
        user_index_magazine = request.user.userindexmagazine_set.first()
        object_list = Dolg.objects.filter(user=user_index_magazine, is_history=False)
        return render(request, 'list/list-dolg.html', {'object_list': object_list})



class DetailDolg(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Dolg
    template_name = 'detail/detail-dolg.html'
    context_object_name = 'object'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        return Dolg.objects.filter(user=user_index_magazine)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)

        try:
            # Try to fetch the object
            obj = queryset.get(pk=pk)
        except Dolg.DoesNotExist:
            # Raise 404 error if object does not exist
            raise Http404("Запись не найдена")

        return obj


class UpdateDolg(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Dolg
    form_class = DolgForm
    template_name = 'update/update-dolg.html'
    success_url = reverse_lazy('list-dolg')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        return Dolg.objects.filter(user=user_index_magazine)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            obj = queryset.get(pk=pk)
        except Dolg.DoesNotExist:
            return HttpResponseRedirect(reverse('list-dolg'))
        return obj


class DeleteDolg(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Dolg
    template_name = 'delete/delete-dolg.html'
    success_url = reverse_lazy('list-dolg')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        return Dolg.objects.filter(user=user_index_magazine)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            obj = queryset.get(pk=pk)
        except Dolg.DoesNotExist:
            return HttpResponseRedirect(reverse('list-dolg'))
        return obj

@login_required
def successPay(request, id):
    user_index_magazine = request.user.userindexmagazine_set.first()

    if not user_index_magazine:
        return HttpResponse("У текущего пользователя нет связанных данных.", status=403)

    try:
        dolg = Dolg.objects.get(id=id, user=user_index_magazine)
    except Dolg.DoesNotExist:
        return HttpResponse("Запись не найдена", status=404)

    if dolg.is_history:
        return HttpResponse("Клиент уже оплатил(а)")

        # Получаем комментарий к оплате из POST-запроса
    if request.method == 'POST':
        payment_comment = request.POST.get('payment_comment', '')
        dolg.payment_comment = payment_comment
        dolg.is_history = True
        dolg.save()
        return HttpResponse("Оплата успешно произведена")

    context = {
        'dolg': dolg,
    }
    return render(request, 'success_pay.html', context)


# history
@login_required
def history_list(request):
    user_index_magazine = request.user.userindexmagazine_set.first()
    history = Dolg.objects.filter(user=user_index_magazine, is_history=True)
    return render(request, 'list/history-list.html', {'history': history})

@login_required
def history_detail(request, id):
    user_index_magazine = request.user.userindexmagazine_set.first()
    try:
        hist = Dolg.objects.get(id=id, user=user_index_magazine)
    except Dolg.DoesNotExist:
        return HttpResponse("Запись не найдена", status=404)

    return render(request, 'detail/history-detail.html', {'object': hist})

@login_required
def recovery_history(request, id):
    user_index_magazine = request.user.userindexmagazine_set.first()
    try:
        history = Dolg.objects.get(id=id, user=user_index_magazine)
    except Dolg.DoesNotExist:
        return HttpResponse("Запись не найдена", status=404)

    if history.is_history:
        history.is_history = False
        history.save()
        return HttpResponse("Данные успешно восстановлены")
    else:
        return HttpResponse("Данные уже были восстановлены ранее")



