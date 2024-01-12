from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from teams.models import Team
from users.models import User
# fmt: off
from users.serializers import (UserCreateSerializer,
                               UserRegistrationResponseSerializer)

# fmt: off


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    # Create a new user.
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                public_serializer = UserRegistrationResponseSerializer(
                    serializer.instance
                )
                return Response(public_serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError(serializer.errors)
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Retrieve a single user instance.
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = UserRegistrationResponseSerializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Retrieve a list of all users.
    def list(self, request, *args, **kwargs):
        try:
            serializer = UserRegistrationResponseSerializer(
                self.get_queryset(), many=True
            )
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Delete a user instance.
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_202_ACCEPTED)
        except NotFound:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def add_team(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        team_name = request.data.get("name", None)

        if not email or not team_name:
            return Response(
                {"error": "Email and Team Name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_instance = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            team_instance = Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            # Створюємо новий об'єкт Team, якщо команда ще не існує
            team_instance = Team.objects.create(name=team_name)

        if user_instance.teams is not None:
            return Response(
                {"error": "User is already a member of a team."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_instance.teams = team_instance
        user_instance.save()

        serializer = UserRegistrationResponseSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def leave_team(self, request, *args, **kwargs):
        email = request.data.get("email", None)

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_instance = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if user_instance.teams is None:
            return Response(
                {"error": "User is not a member of any team."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_instance.teams = None
        user_instance.save()

        serializer = UserRegistrationResponseSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
