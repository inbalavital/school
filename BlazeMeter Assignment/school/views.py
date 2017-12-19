from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework import status
from .serializers import StudentSerializer, TeacherSerializer, CourseSerializer, GradeSerializer
from .models import Student, Teacher, Course, Grade
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg


class HomeViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ObjectList(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def validate(self, request):
        """
        validate the student/teacher create request
        :param request: 
        :return: proper response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        try:
            Teacher.objects.get(email=email)
            # doesn't create the student/teacher in case a teacher with the same email exists
            response = {'teacher': ['a teacher with this email already exists']}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        # if a teacher with this email doesn't exist in DB, check for a student
        except Teacher.DoesNotExist:
            try:
                Student.objects.get(email=email)
                # doesn't create the student/teacher in case a student with the same email exists
                response = {'student': ['a student with this email already exists']}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StudentViewSet(ObjectList):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        return self.validate(request)

    @list_route(methods=['get'])
    def student_highest_average(self, request):
        """
        calculate the student with highest average in courses
        :param request: 
        :return: proper response
        """
        try:
            student_highest_average_id = \
                Grade.objects.all().values('student').annotate(average=Avg('grade')).order_by(
                    '-average').first()['student']
            student_highest_average = Student.objects.get(id=student_highest_average_id)
            serializer = StudentSerializer(student_highest_average)
            response = serializer.data
        # in case there is not enough data in DB
        except TypeError:
            response = {'student': []}
        return Response(response, status.HTTP_200_OK)


class TeacherViewSet(ObjectList):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def create(self, request, *args, **kwargs):
        """
        create a new teacher object
        :param request: 
        :param args: 
        :param kwargs: 
        :return: proper response
        """
        return self.validate(request)

    @list_route(methods=['get'])
    def teacher_max_students(self, request):
        """
        calculate the teacher with max number of students
        :param request: 
        :return: proper response
        """
        try:
            teacher_max_students_id = \
                Course.objects.all().values('teacher').annotate(students_num=Count('student')).order_by(
                    '-students_num').first()['teacher']
            teacher_max_students = Teacher.objects.get(id=teacher_max_students_id)
            serializer = TeacherSerializer(teacher_max_students)
            response = serializer.data
        # in case there is not enough data in DB
        except TypeError:
            response = {'teacher': []}
        return Response(response, status.HTTP_200_OK)


class CourseViewSet(ObjectList):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def validate(self, request):
        """
        validate the course create request
        :param request: 
        :return: proper response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = request.data['name']
        try:
            Course.objects.get(name=name)
            # doesn't create the course in case there is a course with the same name in DB
            response = {'course': ['a course with this name already exists']}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        """
        create a new course object
        :param request: 
        :param args: 
        :param kwargs: 
        :return: proper response
        """
        return self.validate(request)

    @list_route(methods=['get'])
    def easiest_course(self, request):
        """
        calculate the course with highest average of grades
        :param request: 
        :return: 
        """
        try:
            easiest_course_id = \
                Grade.objects.all().values('course').annotate(average=Avg('grade')).order_by(
                    '-average').first()['course']
            easiest_course = Course.objects.get(id=easiest_course_id)
            serializer = CourseSerializer(easiest_course)
            response = serializer.data
        # in case there is not enough data in DB
        except TypeError:
            response = {'course': []}
        return Response(response, status.HTTP_200_OK)


class GradeViewSet(ObjectList):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def validate(self, request):
        """
        validate the grade create request
        :param request: 
        :return: proper response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = request.data['course']
        student_id = request.data['student']
        course = Course.objects.get(id=course_id)
        student = Student.objects.get(id=student_id)
        try:
            Grade.objects.get(student=student_id, course=course_id)
            # in case a course grade to this student already exists, doesn't create the grade object
            response = {'grade': ['a course grade to this student already exists']}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Grade.DoesNotExist:
            if student not in course.student.all():
                # if the student isn't enrolled in the course, doesn't create the grade object
                response = {'student': ['student not in course']}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        """
        create a new grade object
        :param request: 
        :param args: 
        :param kwargs: 
        :return: proper response
        """
        return self.validate(request)
