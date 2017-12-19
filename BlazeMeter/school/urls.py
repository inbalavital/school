from django.conf.urls import url, include
from views import StudentViewSet, TeacherViewSet, CourseViewSet, GradeViewSet
from rest_framework.routers import DefaultRouter

app_name = 'school'

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
