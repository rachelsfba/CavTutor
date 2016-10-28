from rest_framework import viewsets

from . import models, serializers

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows institutions to be viewed or edited.
    """
    queryset = models.Institution.objects.all().order_by('name')
    serializer_class = serializers.InstitutionSerializer


class TutorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tutors to be viewed or edited.
    """
    queryset = models.Tutor.objects.all().order_by('course')
    serializer_class = serializers.TutorSerializer


class TuteeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tutees to be viewed or edited.
    """
    queryset = models.Tutee.objects.all().order_by('course')
    serializer_class = serializers.TuteeSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = models.Course.objects.all().order_by('abbr')
    serializer_class = serializers.CourseSerializer


class AuthenticatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authneticators to be viewed or edited.
    """
    queryset = models.Authenticator.objects.all().order_by('user')
    serializer_class = serializers.AuthenticatorSerializer

