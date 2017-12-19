from rest_framework import serializers
from .models import Student, Teacher, Course, Grade

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # student = StudentSerializer(many=True, source='id')
    # teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    # student = StudentSerializer()
    # course = CourseSerializer()

    class Meta:
        model = Grade
        fields = '__all__'


