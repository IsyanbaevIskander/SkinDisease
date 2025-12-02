from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Пациент'),
        ('dermatologist', 'Дерматолог'),
        ('admin', 'Администратор'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.username} ({self.get_role_display()})'


class SkinCondition(models.Model):
    name = models.CharField('Название заболевания', max_length=100)
    code = models.CharField('Код', max_length=10, unique=True, null=True, blank=True)
    description = models.TextField('описание', blank=True, default='Ничего нет')

    class Meta:
        verbose_name = 'Кожное заболевание'
        verbose_name_plural = 'Справочник кожных заболеваний'

    def __str__(self) -> str:
        return f'{self.name} ({self.code or "без кода"})'


class DiagnosisRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diagnosis_requests',
        verbose_name='Пользователь',
    )

    image = models.ImageField(
        'Изображение',
        upload_to='images/',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Запрос диагностики'
        verbose_name_plural = 'Запросы диагностики'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Запрос {self.id} ({self.user.username})'


class DiagnosisResult(models.Model):
    request = models.OneToOneField(
        DiagnosisRequest,
        on_delete=models.CASCADE,
        related_name='result',
        verbose_name='Запрос',
    )
    condition = models.ForeignKey(
        SkinCondition,
        on_delete=models.SET_NULL,
        null=True,
        related_name='results',
        verbose_name='Определённое заболевание',
    )
    confidence = models.DecimalField('Уверенность', max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = 'Результат диагностики'
        verbose_name_plural = 'Результаты диагностики'

    def __str__(self) -> str:
        return f'Результат {self.request.id}: {self.condition.name if self.condition else "Не определено"}'


class MedicalVerification(models.Model):
    result = models.OneToOneField(
        DiagnosisResult,
        on_delete=models.CASCADE,
        related_name='verification',
        verbose_name='Результат диагностики',
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'dermatologist'},
        related_name='verifications',
        verbose_name='Врач-дерматолог',
    )
    actual_condition = models.ForeignKey(
        SkinCondition,
        on_delete=models.SET_NULL,
        null=True,
        related_name='verifications',
        verbose_name='Фактическое заболевание',
    )

    class Meta:
        verbose_name = 'Медицинская верификация'
        verbose_name_plural = 'Медицинские верификации'

    def __str__(self) -> str:
        return f'Верификация {self.result.id} ({self.doctor.username})'
