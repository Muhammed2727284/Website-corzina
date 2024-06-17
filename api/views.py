from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from core.models import Dolg
from .serializers import (
    DolgSerializer, CreateDolgSerializer, UpdateDolgSerializer,
    SoftDeleteDolgSerializer, SuccessPaySerializer
)

class DolgViewSet(viewsets.ModelViewSet):
    queryset = Dolg.objects.all()
    serializer_class = DolgSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        return Dolg.objects.filter(user=user_index_magazine, is_deleted=False)

    def perform_create(self, serializer):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        serializer.save(user=user_index_magazine)

    @action(detail=True, methods=['patch'])
    def soft_delete(self, request, pk=None):
        dolg = self.get_object()
        serializer = SoftDeleteDolgSerializer(dolg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user_deleted=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def success_pay(self, request, pk=None):
        dolg = self.get_object()
        if dolg.is_history:
            return Response({"detail": "Клиент уже оплатил(а)"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SuccessPaySerializer(dolg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def history(self, request):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        history = Dolg.objects.filter(user=user_index_magazine, is_history=True)
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def korzina(self, request):
        user_index_magazine = self.request.user.userindexmagazine_set.first()
        korzina = Dolg.objects.filter(user=user_index_magazine, is_deleted=True)
        serializer = self.get_serializer(korzina, many=True)
        return Response(serializer.data)
