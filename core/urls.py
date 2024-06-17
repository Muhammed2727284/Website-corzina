from django.urls import path
from .views import *

from core import admin

urlpatterns = [
    path('', core, name="core"),
    path('logout/', user_logout, name="logout"),
    path('create-dolg/', CreateDolg.as_view(), name="create-dolg"),
    path('list-dolg/', ListDolg.as_view(), name="list-dolg"),
    path('detail-dolg/<int:id>/', DetailDolg.as_view(), name="detail-dolg"),
    path('update-dolg/<int:id>/', UpdateDolg.as_view(), name="update-dolg"),
    path('delete-dolg/<int:id>/', DeleteDolg.as_view(), name="delete-dolg"),
    path('successpay/<int:id>/', successPay, name="pay"),
    path('history/', history_list, name="history-list"),
    path('history/<int:id>/', history_detail, name="history-detail"),
    path('recovery/<int:id>/', recovery_history, name="recovery"),

    path('success-pay/<int:id>/', successPay, name='success-pay'),

    path('delete-korzina/<int:id>/', delete_korzina, name='delete_korzina'),
    path('korzina-list/', korzina_list, name="korzina_list"),
    path('korzina-detail/<int:id>/', korzina_detail, name='korzina_detail'),
]