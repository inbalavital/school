from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework import status
from .serializers import StudentSerializer, TeacherSerializer, CourseSerializer, GradeSerializer
from .models import Student, Teacher, Course, Grade
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg


class ObjectList(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


class StudentViewSet(ObjectList):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @list_route(methods=['get'])
    def student_highest_average(self, request):
        try:
            student_highest_average_id = \
                Grade.objects.all().values('student').annotate(average=Avg('grade')).order_by(
                    '-average').first()['student']
            student_highest_average = Student.objects.get(id=student_highest_average_id)
            serializer = StudentSerializer(student_highest_average)
            response = serializer.data
        except TypeError:
            response = {'student': []}
        return Response(response, status.HTTP_200_OK)


class TeacherViewSet(ObjectList):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @list_route(methods=['get'])
    def teacher_max_students(self, request):
        try:
            teacher_max_students_id = \
                Course.objects.all().values('teacher').annotate(students_num=Count('student')).order_by(
                    '-students_num').first()['teacher']
            teacher_max_students = Teacher.objects.get(id=teacher_max_students_id)
            serializer = TeacherSerializer(teacher_max_students)
            response = serializer.data
        except TypeError:
            response = {'teacher': []}
        return Response(response, status.HTTP_200_OK)


class CourseViewSet(ObjectList):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = request.data['name']
        try:
            Course.objects.get(name=name)
            response = {'course': ['a course with this name already exists']}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['get'])
    def easiest_course(self, request):
        try:
            easiest_course_id = \
                Grade.objects.all().values('course').annotate(average=Avg('grade')).order_by(
                    '-average').first()['course']
            easiest_course = Course.objects.get(id=easiest_course_id)
            serializer = CourseSerializer(easiest_course)
            response = serializer.data
        except TypeError:
            response = {'course': []}
        return Response(response, status.HTTP_200_OK)


class GradeViewSet(ObjectList):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = request.data['course']
        student_id = request.data['student']
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(id=student_id)
        try:
            Grade.objects.get(student=student_id, course=course_id)
            response = {'grade': ['a course grade to this student already exists']}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Grade.DoesNotExist:
            if student not in course.student.all():
                response = {'student': ['student not in course']}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
