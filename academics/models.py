from django.conf import settings
from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class TeacherClass(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teaching_classes",
        limit_choices_to={"role": "TEACHER"},
    )
    class_group = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "class_group"],
                name="unique_teacher_class",
            )
        ]

    def __str__(self):
        return f"{self.teacher} → {self.class_group}"


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teaching_subjects",
        limit_choices_to={"role": "TEACHER"},
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )
    class_group = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="subject_teachers",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "subject", "class_group"],
                name="unique_teacher_subject_class",
            )
        ]

    def __str__(self):
        return f"{self.teacher} → {self.subject} → {self.class_group}"


class StudentClass(models.Model):
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_class",
        limit_choices_to={"role": "STUDENT"},
    )
    class_group = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="students",
    )

    def __str__(self):
        return f"{self.student} → {self.class_group}"