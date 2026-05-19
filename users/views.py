from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import *
from .models import User
from django.shortcuts import get_object_or_404
from .permissions import *

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class CustomTokenRefreshView(TokenRefreshView):
    pass

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    


class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(role='customer').order_by('-created_at')
    serializer_class = UserManageSerializer
    permission_classes = [IsSeller]
    filterset_fields = ['role', 'is_approved']
    search_fields = ['username', 'full_name', 'phone']

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserManageSerializer
    permission_classes = [IsAdminOrSeller]
    lookup_field = 'id'

class UserApproveView(APIView):
    permission_classes = [IsAdminOrSeller]

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        if user.role != 'customer':
            return Response({"detail": "Только клиенты могут быть одобрены."},
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_approved = True
        user.save()
        serializer = UserManageSerializer(user)
        return Response(serializer.data)

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSeller]
    lookup_field = 'id'