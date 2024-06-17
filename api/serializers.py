from rest_framework import serializers
from core.models import Dolg

class DolgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolg
        fields = '__all__'

class CreateDolgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolg
        fields = ['client', 'phone_number', 'summa', 'description']

class UpdateDolgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolg
        fields = ['client', 'phone_number', 'summa', 'description', 'payment_comment']

class SoftDeleteDolgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolg
        fields = ['deleted_comment']

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.deleted_comment = validated_data.get('deleted_comment', instance.deleted_comment)
        instance.date_deleted = timezone.now()
        instance.save()
        return instance

class SuccessPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dolg
        fields = ['payment_comment']

    def update(self, instance, validated_data):
        instance.is_history = True
        instance.payment_comment = validated_data.get('payment_comment', instance.payment_comment)
        instance.save()
        return instance
