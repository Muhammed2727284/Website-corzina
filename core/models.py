from django.contrib.auth.models import User
from django.db import models



# Create your models here.
class Dolg(models.Model):
    user = models.ForeignKey('UserIndexMagazine', on_delete=models.CASCADE, verbose_name='Кассир')
    client = models.CharField(max_length=255, verbose_name='Карыз алган адам')
    phone_number = models.CharField(max_length=255, verbose_name='Номер телефона', default='0')
    summa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    description = models.TextField(verbose_name='Описание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')

    is_history = models.BooleanField(default=False, verbose_name="Из история")
    date_add_history = models.DateField(blank=True, null=True, verbose_name="Дата добавление истории")
    user_history = models.ForeignKey('UserIndexMagazine', on_delete=models.CASCADE, blank=True, null=True, related_name='user_history', verbose_name='Кассир доб. истории')

    is_deleted = models.BooleanField(default=False, verbose_name='Из удаление')
    deleted_comment = models.TextField(verbose_name='Комментарий удаление', blank=True)
    date_deleted = models.DateTimeField(blank=True, null=True, verbose_name='Дата удаление')
    user_deleted = models.ForeignKey('UserIndexMagazine', on_delete=models.CASCADE, blank=True, null=True, related_name='user_deleted', verbose_name='Кассир удаление')

    payment_comment = models.TextField(verbose_name='Комментарий к оплате', blank=True)

    def __str__(self):
        return f"Карыз: {self.client}, сумма: {self.summa}"




class Magazine(models.Model):
    name_magazine = models.CharField(max_length=255, verbose_name='Имя магазина')
    phone_magazine = models.CharField(max_length=255, verbose_name='Телефон магазина')
    pay = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Платеж')
    date_create_magazine = models.DateTimeField(verbose_name='Дата создание магазина')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f"{self.name_magazine}"


class UserIndexMagazine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кассир индекс магазина')
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, verbose_name='Магазин')
    date_create_index_user = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание индекс пользователя')

    def __str__(self):
        return f"{self.user} - {self.magazine}"


