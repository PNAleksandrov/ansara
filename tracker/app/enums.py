from django.db import models


class StatusChoices(models.TextChoices):
    CREATED = 'Задача создана',


class StatusAssign(models.TextChoices):
    ASSIGNED = 'Назначен исполнитель',
    NOT_ASSIGNED = 'Не назначен исполнитель'

class CheckChoices(models.TextChoices):
    CHECKED = 'Задача проверена',
    NOT_CHECKED = 'Задача не проверена'


class CompletedChoices(models.TextChoices):
    COMPLETED  = 'Задача выполнена',
    NOT_COMPLETED = 'Задача не выполнена'