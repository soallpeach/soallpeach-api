from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scores.models import Score
from scores.serializers import ScoreSerializer


class ScoreView(APIView):
    permission_classes = (IsAuthenticated,)  # <-- And here

    def get(self, request):
        return Response(ScoreSerializer(instance=Score.objects.all(), many=True).data)

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreTableView(View):
    def get(self, request):
        latest_run_score = Score.objects.latest('run_id')
        latest_scores = Score.objects.filter(run_id=latest_run_score.run_id).all()
        return render(request, 'scores.html', {'scores': latest_scores})
