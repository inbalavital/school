from __future__ import unicode_literals

from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=75)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Teacher(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=75)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Course(models.Model):
    name = models.CharField(max_length=50)
    student = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Grade(models.Model):
    from django.core.validators import MaxValueValidator, MinValueValidator

    grade = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.grade)

    class Meta:
        ordering = ('grade',)




