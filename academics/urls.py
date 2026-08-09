from rest_framework.routers import DefaultRouter

from .views import (
    ClassViewSet,
    SubjectViewSet,
    TeacherClassViewSet,
    TeacherSubjectViewSet,
    StudentClassViewSet,
)


router = DefaultRouter()

router.register("classes", ClassViewSet, basename="class")
router.register("subjects", SubjectViewSet, basename="subject")
router.register(
    "teacher-classes",
    TeacherClassViewSet,
    basename="teacher-class",
)
router.register(
    "teacher-subjects",
    TeacherSubjectViewSet,
    basename="teacher-subject",
)
router.register(
    "student-classes",
    StudentClassViewSet,
    basename="student-class",
)

urlpatterns = router.urls