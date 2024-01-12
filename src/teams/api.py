from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from teams.serializers import TeamCreateSerializer, TeamSerializer

from .models import Team


class TeamAPIViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]

    # Create a new team.
    def create(self, request, *args, **kwargs):
        try:
            serializer = TeamCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Retrieve a list of all teams.
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = TeamSerializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response(
                {"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Retrieve information about a specific team.
    def list(self, request, *args, **kwargs):
        try:
            serializer = TeamSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Update information about an existing team.
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = TeamCreateSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotFound:
            return Response(
                {"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Delete a team.
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except NotFound:
            return Response(
                {"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
