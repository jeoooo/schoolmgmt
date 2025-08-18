from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from professors.models import Professor
from .serializers import ProfessorsSerializer

# get all professors and create a new professor
class ProfessorListCreate(generics.ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# get, update, delete professor by ID
class ProfessorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorsSerializer

    def get(self, request, *args, **kwargs):
        professor = self.get_object()
        serializer = self.get_serializer(professor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        professor = self.get_object()
        serializer = self.get_serializer(professor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        professor = self.get_object()
        serializer = self.get_serializer(professor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        professor = self.get_object()
        professor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)