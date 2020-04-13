from django.shortcuts import render
from django.views import View
from django_mysql.models.functions import JSONExtract
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scores.models import Score, Round
from scores.serializers import ScoreSerializer, RoundSerializer
from scores.util import convert_ms_to_minutes
import time


class RoundView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, challenge_name):
        serializer = RoundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoundDetailView(GenericAPIView, UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ScoreView(APIView):
    permission_classes = (IsAuthenticated,)

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
        latest_round = Round.objects.filter(state='FINISHED').last()
        if latest_round:
            time_passed_from_last_run = convert_ms_to_minutes((time.time() - latest_round.updated.timestamp()) * 1000)
            latest_scores = Score.objects.filter(round_id=latest_round.id).order_by(
                JSONExtract('result', '$.run_result.duration').asc(nulls_last=True)
            ).all()
        else:
            time_passed_from_last_run = 0
            latest_scores = []

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
