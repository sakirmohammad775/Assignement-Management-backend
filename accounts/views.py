from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from academics.models import Class, StudentClass
from .serializers import LoginSerializer, UserSerializer, AdminStudentSerializer
from .permissions import IsAdmin
from .models import User


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            }
        )


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class AdminTeacherViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role=User.Role.TEACHER).order_by("-date_joined")


class AdminStudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserSerializer

        return AdminStudentSerializer

    def get_queryset(self):
        return (
            User.objects.filter(role=User.Role.STUDENT)
            .select_related(
                "student_class",
                "student_class__class_group",
            )
            .order_by("-date_joined")
        )

    def perform_create(self, serializer):
        serializer.save(role=User.Role.STUDENT)


class AdminStudentClassView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, student_id):
        try:
            student = User.objects.get(
                id=student_id,
                role=User.Role.STUDENT,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Student not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        class_id = request.data.get("class_id")

        if not class_id:
            return Response(
                {"class_id": "Class is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            class_group = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response(
                {"class_id": "Class not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        student_class, _ = StudentClass.objects.update_or_create(
            student=student,
            defaults={
                "class_group": class_group,
            },
        )

        return Response(
            {
                "student_id": student.id,
                "class_id": student_class.class_group.id,
                "class_name": student_class.class_group.name,
                "class_code": student_class.class_group.code,
            }
        )
