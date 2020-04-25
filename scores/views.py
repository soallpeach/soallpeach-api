from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scores.models import Score, Round
from scores.score_processor import process, prepare_scores
from scores.serializers import ScoreSerializer, RoundSerializer


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
            score = serializer.save()
            processed_score = process(score)
            processed_score.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreTableView(View):
    def get(self, request):
        latest_scores, time_passed_from_last_run = prepare_scores('prime')

        return render(request, 'scores.html',
                      {'scores': latest_scores, 'time_passed_from_last_run': time_passed_from_last_run})


class ScoreDetailView(APIView):
    def get(self, request, score_id: int):
        score = Score.objects.filter(id=score_id).first()
        return Response(ScoreSerializer(instance=score).data)


class PrimeChallengeView(View):
    def get(self, request):
        return render(request, 'challenges/prime.html')


class CountmeChallengeView(View):
    def get(self, request):
        latest_scores, time_passed_from_last_run = prepare_scores('countme')

        return render(request, 'challenges/countme.html',
                      {'scores': latest_scores, 'time_passed_from_last_run': time_passed_from_last_run})


class ParticipationView(View):
    def get(self, request):
        return render(request, 'participation.html')
