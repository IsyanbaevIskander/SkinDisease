from django.contrib import admin

from core import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')
    list_filter = ('role',)
    search_fields = ('username',)


@admin.register(models.SkinCondition)
class SkinConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


@admin.register(models.DiagnosisRequest)
class DiagnosisRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)


@admin.register(models.DiagnosisResult)
class DiagnosisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'condition', 'confidence')
    list_filter = ('condition',)
    search_fields = ('condition__name',)


@admin.register(models.MedicalVerification)
class MedicalVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'result', 'doctor', 'actual_condition')
    search_fields = ('doctor__username', 'actual_condition__name')
