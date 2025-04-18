from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from colleges.models import College
from .serializers import CollegeSerializer

# get all colleges and create a new college
class CollegeListCreate(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get, update, delete college by ID
class CollegeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def get(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = self.get_serializer(college)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = self.get_serializer(college, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = self.get_serializer(college, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        college = self.get_object()
        college.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)