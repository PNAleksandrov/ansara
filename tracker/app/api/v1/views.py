from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Task, TaskStatusHistory
from app.api.v1.serializers import TaskSerializer, TaskStatusHistorySerializer
from django.shortcuts import get_object_or_404

class TaskListCreateView(generics.ListCreateAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    serializer_class = TaskSerializer

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()

            TaskStatusHistory.objects.create(
                task=task,
                responsible=request.user,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class TaskDestroy(generics.DestroyAPIView):
    http_method_names = ['delete']

    def destroy(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)