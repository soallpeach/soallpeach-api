from django.shortcuts import render
from django.views import View
from django_mysql.models.functions import JSONExtract
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scores.models import Score
from scores.serializers import ScoreSerializer
from scores.util import convert_ms_to_minutes
import time


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
        latest_run_score: Score = Score.objects.latest('run_id')
        run_id = latest_run_score.run_id
        time_passed_from_last_run = convert_ms_to_minutes((time.time() - run_id) * 1000)

        latest_scores = Score.objects.filter(run_id=run_id).order_by(
            JSONExtract('result', '$.run_result.duration').asc(nulls_last=True)
        ).all()

        return render(request, 'scores.html',
                      {'scores': latest_scores, 'time_passed_from_last_run': time_passed_from_last_run})


class ScoreDetailView(APIView):
    def get(self, request, score_id: int):
        score = Score.objects.filter(id=score_id).first()
        return Response(ScoreSerializer(instance=score).data)


class PrimeChallengeView(View):
    def get(self, request):
        return render(request, 'challenges/prime.html')


class ParticipationView(View):
    def get(self, request):
        return render(request, 'participation.html')
