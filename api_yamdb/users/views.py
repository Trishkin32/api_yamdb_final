from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdminSuperuser
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserMeSerializer, UserSerializer)
from .validators import ValidateUsername


class UserViewSet(ValidateUsername, viewsets.ModelViewSet):
    """User viewset."""

    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAdminSuperuser,)
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserSerializer
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'post', 'delete')

    @action(
        methods=('get', 'patch'),
        url_path='me',
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):

        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(user, data=request.data,
                                      partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):

    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    try:
        user, _ = User.objects.get_or_create(
            username=username, email=email)
    except IntegrityError:
        if (
            User.objects.filter(username=username).exists()
            and User.objects.filter(email=email).exists()
        ):
            error = {
                'username': ['Это имя уже занято.'],
                'email': ['Этот email уже занят.']
            }
        elif User.objects.filter(username=username).exists():
            error = {'username': ['Это имя уже занято.']}
        else:
            User.objects.filter(email=email).exists()
            error = {'email': ['Этот email уже занят.']}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Registration Yamdb.',
        message=f'Verify code: {confirmation_code}',
        from_email='api_yamdb@staff',
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'access': str(token)}, status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Invalid confirmation code'},
        status=status.HTTP_400_BAD_REQUEST
    )
