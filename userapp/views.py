from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import  Response
from rest_framework.decorators import permission_classes
from  rest_framework.permissions import AllowAny

from .serializers import UserSerializer

User = get_user_model()


class UserView(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
               generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = 'id'
    #
    def get_object(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        return user

    @permission_classes([AllowAny])
    def get(self, request, *args, **kwargs):
        user = self.get_object(request)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(request)
        data = self.request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            serializer.update(instance, validated_data)
            return Response({'message': 'user updated'}, status=status.HTTP_201_CREATED)


    def delete(self, request, *args, **kwargs):
        user = self.get_object(request, *args, **kwargs)
        user.delete()
        return Response({'message': 'user successfully deleted'},
                        status=status.HTTP_204_NO_CONTENT)

