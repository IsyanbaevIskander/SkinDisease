from rest_framework.routers import DefaultRouter

from core import views

app_name = 'core'

urlpatterns = []

router = DefaultRouter()

router.register('users', views.UserView, basename='users')
router.register('skin_conditions', views.SkinConditionView, basename='skin_conditions')
router.register('diagnosis_request', views.DiagnosisRequestView, basename='diagnosis_request')
router.register('diagnosis_result', views.DiagnosisResultView, basename='diagnosis_result')
router.register('medical_verification', views.MedicalVerificationView, basename='medical_verification')

urlpatterns += router.urls
