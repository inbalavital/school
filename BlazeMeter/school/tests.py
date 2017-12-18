from django.test import TestCase, Client
from models import Student, Teacher, Course, Grade
import json


class APITests(TestCase):
    def setUp(self):
        self.client = Client()

    def create(self, model, data):
        response = self.client.post('/school/' + model + '/', data)
        self.assertEqual(response.status_code, 201)

    def read(self, model):
        request = self.client.get('/school/' + model + '/')
        self.assertEqual(len(request.json()), 1)
        self.assertEqual(request.status_code, 200)

        specific_request = self.client.get('/school/' + model + '/1/')
        self.assertEqual(specific_request.json()['id'], 1)
        self.assertEqual(specific_request.status_code, 200)

    def update(self, model, data):
        response = self.client.patch('/school/' + model + '/1/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def delete(self, model):
        response = self.client.delete('/school/' + model + '/1/')
        self.assertEqual(response.status_code, 204)

    def create_students_teachers(self):
        data_students_teachers = {'first_name': 'FName1', 'last_name': 'LName1', 'email': 'FName1@gmail.com'}
        self.create('students', data_students_teachers)
        self.create('teachers', data_students_teachers)

    def create_courses(self, student):
        teacher = Teacher.objects.last().id
        data_courses = {'name': 'CName1', 'teacher': teacher, 'student': [student]}
        self.create('courses', data_courses)

    def create_grades(self, student):
        course = Course.objects.last().id
        data_grades = {'grade': 85, 'student': student, 'course': course}
        self.create('grades', data_grades)

    def test_CRUD(self):
        self.create_students_teachers()
        student = Student.objects.last().id
        self.create_courses(student)
        self.create_grades(student)

        self.read('students')
        self.read('teachers')
        self.read('courses')
        self.read('grades')

        data_students_teachers = json.dumps({'first_name': 'FName1_new'})
        self.update('students', data_students_teachers)
        self.update('teachers', data_students_teachers)
        data_courses = json.dumps({'name': 'CName1_new'})
        self.update('courses', data_courses)
        data_grades = json.dumps({'grade': 90})
        self.update('grades', data_grades)

        self.delete('grades')
        self.delete('courses')
        self.delete('students')
        self.delete('teachers')

    def teacher_max_students(self):
        request = self.client.get('/school/teachers/teacher_max_students/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['id'], 1)

    def student_highest_average(self):
        request = self.client.get('/school/students/student_highest_average/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['id'], 2)

    def easiest_course(self):
        request = self.client.get('/school/courses/easiest_course/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['id'], 2)

    def test_statistics(self):
        student1 = Student.objects.create(first_name='FName1', last_name='LName1', email='FName1@gmail.com')
        student2 = Student.objects.create(first_name='FName2', last_name='LName2', email='FName2@gmail.com')
        teacher1 = Teacher.objects.create(first_name='FName5', last_name='LName5', email='FName5@gmail.com')
        teacher2 = Teacher.objects.create(first_name='FName6', last_name='LName6', email='FName6@gmail.com')
        course1 = Course.objects.create(name="CName1", teacher=teacher1)
        course1.student.add(student1, student2)
        course2 = Course.objects.create(name="CName2", teacher=teacher2)
        course2.student.add(student1)
        self.teacher_max_students()

        course2.student.add(student2)
        Grade.objects.create(grade=80, student=student1, course=course1)
        Grade.objects.create(grade=90, student=student1, course=course2)
        Grade.objects.create(grade=85, student=student2, course=course1)
        Grade.objects.create(grade=90, student=student2, course=course2)
        self.student_highest_average()
        self.easiest_course()
