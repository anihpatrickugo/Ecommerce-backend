import logging

from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import  Response
from rest_framework.decorators import permission_classes
from  rest_framework.permissions import AllowAny

from .serializers import UserSerializer

logger = logging.getLogger('django.request')
User = get_user_model()


class UserView(mixins.UpdateModelMixin, mixins.DestroyModelMixin,
               generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def get_object(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        return user

    def get(self, request, *args, **kwargs):
        """
        This return the current authenticated user
        """
        user = self.get_object(request)
        serializer = UserSerializer(user)

        logger.info('returned a current request user')
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        This creates a new user with an email, username and passord.
        """
        data = self.request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            password = data.pop('password')
            user = User.objects.create(**data)
            user.set_password(password)
            user.save()

            logger.info('created a new request user')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        This is used for updating an authenticated user.
        """
        instance = self.get_object(request)
        data = self.request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            serializer.update(instance, validated_data)

            logger.info('modified an existing request user')
            return Response({'message': 'user updated'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """
        This is used for deleting an authenticated user
        account.
        """
        user = self.get_object(request, *args, **kwargs)
        user.delete()

        logger.info('deleted a request user')
        return Response({'message': 'user successfully deleted'},
                        status=status.HTTP_204_NO_CONTENT)


