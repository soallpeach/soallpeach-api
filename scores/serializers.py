from rest_framework.serializers import ModelSerializer

from scores.models import Score, Round


class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'


class RoundSerializer(ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'
