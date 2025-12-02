from rest_framework.routers import DefaultRouter

from core import views

app_name = 'core'

urlpatterns = []

router = DefaultRouter()

router.register('users', views.UserView, basename='users')
router.register('skin_conditions', views.SkinConditionView, basename='skin_conditions')
router.register('diagnosis_requests', views.DiagnosisRequestView, basename='diagnosis_requests')
router.register('diagnosis_results', views.DiagnosisResultView, basename='diagnosis_results')
router.register('medical_verifications', views.MedicalVerificationView, basename='medical_verifications')

urlpatterns += router.urls
