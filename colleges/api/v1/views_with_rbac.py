from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from colleges.models import College
from .serializers import CollegeSerializer
from users.permissions import IsAdmin, IsPrincipal, IsCollegeManager

# get all colleges and create a new college
class CollegeListCreate(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions required for this view.
        """
        if self.request.method == 'GET':
            # Anyone authenticated can view colleges list
            permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == 'POST':
            # Only admins can create colleges
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        user = self.request.user
        if not user.is_authenticated:
            return College.objects.none()
        
        # Admins can see all colleges
        if user.is_admin():
            return College.objects.all()
        # Principals can see their own college
        elif user.is_principal() and user.college:
            return College.objects.filter(id=user.college.id)
        # Other users can see all colleges (read-only)
        else:
            return College.objects.all()

    @swagger_auto_schema(
        operation_summary="Create a new college",
        operation_description="Create a new college. Only system administrators can create colleges.",
        responses={
            201: CollegeSerializer,
            400: "Bad Request - Invalid data",
            403: "Forbidden - Insufficient permissions"
        }
    )
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
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions required for this view.
        """
        if self.request.method == 'GET':
            # Anyone authenticated can view college details
            permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH']:
            # Only admins or college managers can update
            permission_classes = [permissions.IsAuthenticated, IsCollegeManager]
        elif self.request.method == 'DELETE':
            # Only admins can delete colleges
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user role and permissions
        """
        user = self.request.user
        if not user.is_authenticated:
            return College.objects.none()
        
        # Admins can access all colleges
        if user.is_admin():
            return College.objects.all()
        # Principals can access their own college
        elif user.is_principal() and user.college:
            return College.objects.filter(id=user.college.id)
        # Other users can view all colleges (read-only)
        else:
            return College.objects.all()

    @swagger_auto_schema(
        operation_summary="Get college details",
        operation_description="Retrieve details of a specific college by ID.",
        responses={
            200: CollegeSerializer,
            404: "College not found"
        }
    )
    def get(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = self.get_serializer(college)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update college",
        operation_description="Update a college. Only admins or college principals can update college information.",
        responses={
            200: CollegeSerializer,
            400: "Bad Request - Invalid data",
            403: "Forbidden - Insufficient permissions",
            404: "College not found"
        }
    )
    def put(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = self.get_serializer(college, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update college",
        operation_description="Partially update a college. Only admins or college principals can update college information.",
        responses={
            200: CollegeSerializer,
            400: "Bad Request - Invalid data",
            403: "Forbidden - Insufficient permissions",
            404: "College not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        college = self.get_object()
        serializer = self.get_serializer(college, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete college",
        operation_description="Delete a college. Only system administrators can delete colleges.",
        responses={
            204: "College deleted successfully",
            403: "Forbidden - Insufficient permissions",
            404: "College not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        college = self.get_object()
        college.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
