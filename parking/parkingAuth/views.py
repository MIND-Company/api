from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# TODO: Это, конечно капец, надо разобраться как это делается по-нормальному
class UserViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        data = request.data
        if data.get('email'):
            user.email = data['email']
        if data.get('first_name'):
            user.first_name = data['first_name']
        if data.get('last_name'):
            user.last_name = data['last_name']
        if data.get('username'):
            user.username = data['username']

        user_data = UserSerializer(data=vars(user))
        if user_data.is_valid():
            user.save()
        else:
            return Response(user_data.errors, status.HTTP_400_BAD_REQUEST)

        return Response(user_data.data, status=status.HTTP_200_OK)
