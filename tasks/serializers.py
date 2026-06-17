from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'owner',
            'owner_username',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'owner',
            'owner_username',
            'created_at',
            'updated_at',
        ]