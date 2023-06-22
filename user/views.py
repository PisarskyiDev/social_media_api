from rest_framework import generics, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import UserSerializer, UserCreateSerializer


class OrderPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 100


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    authentication_classes = ()
    permission_classes = ()


class UserView(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related("subscribe__followers")
    pagination_class = OrderPagination


class SelfUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects

    def get_object(self):
        return self.request.user
