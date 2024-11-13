from rest_framework import serializers
from app.models import Task, TaskStatusHistory, CustomUser
from app.enums import StatusChoices, CheckChoices, CompletedChoices
from django.utils.translation import gettext_lazy as _




def format_field_value(field_name, value):
    if value:
        if isinstance(value, str):  # Check if it's an enum value
            if field_name == 'status':
                status_enum = StatusChoices
            elif field_name == 'task_completed':
                status_enum = CompletedChoices
            elif field_name == 'task_check_by':
                status_enum = CheckChoices

            try:
                status_text = getattr(status_enum, value).value
                return f"{status_text}: {value}"
            except AttributeError:
                # If the value is not found in the enum, return the value as-is
                return f"{field_name}: {value}"
        elif isinstance(value, CustomUser):  # Check if it's a User object
            return f"{field_name}: {value.username}, {value.date_joined}"
        else:  # Assume it's a datetime object
            return f"{field_name}: {value}"
    return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class TaskStatusHistorySerializer(serializers.ModelSerializer):
    responsible = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TaskStatusHistory
        fields = ['responsible', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'task_completed', 'task_check_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Create nested representations
        status_history = self._get_status_history(instance)
        assigned_to_history = self._get_assigned_to_history(instance)
        task_completed_history = self._get_task_completed_history(instance)
        task_check_by_history = self._get_task_check_by_history(instance)

        # Combine all histories
        history = {
            "status": status_history,
            "assigned_to": assigned_to_history,
            "task_completed": task_completed_history,
            "task_check_by": task_check_by_history,
        }

        # Replace fields with nested representations
        representation.update(history)

        return representation

    def _get_status_history(self, instance):
        status_history = {}

        current_status_text = self._translate_choice(StatusChoices, instance.status)
        status_history[current_status_text] = f"{instance.created_at}"

        for history in instance.status_history.all():
            status_text = self._translate_choice(StatusChoices, history.task.status)
            status_history[status_text] = f"{history.responsible.username}, {history.created_at}"

        return status_history

    def _get_assigned_to_history(self, instance):
        if instance.assigned_to:
            return {"Задача назначена на": f"{instance.assigned_to.username}, {instance.updated_at}"}
        return {}

    def _get_task_completed_history(self, instance):
        completed_text = self._translate_choice(CompletedChoices, instance.task_completed)
        return {completed_text: f"{instance.assigned_to.username}, {instance.updated_at}"}

    def _get_task_check_by_history(self, instance):
        if instance.task_check_by:
            return {"Задача проверена": f"{instance.task_check_by.username}, {instance.updated_at}"}
        return {}

    def _translate_choice(self, choices_enum, value):
        choices_dict = dict(choices_enum.choices)
        english_key = choices_dict[value]
        russian_translations = {
            "Created": "Задача создана",
            "Completed": "Задача завершена"
            # Add more translations as needed
        }

        return russian_translations.get(english_key, english_key)