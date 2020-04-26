import json
import time

from django.db.models import F

from scores.models import Score, Round
from scores.util import convert_ms_to_minutes


def process(score: Score) -> Score:
    if score.round.challenge_name == 'countme':
        return process_countme(score)
    return score


def process_countme(score: Score) -> Score:
    if score.state == 'FAILED':
        return score
    metrics_str = score.result.get('metrics', {}).get('stdout', {})
    metrics_json = json.loads(metrics_str)
    status_codes = metrics_json.get('status_codes', {})
    if len(status_codes) != 1:
        score.state = 'FAILED'
    else:
        count_of_200 = status_codes.get('200', None)
        if not count_of_200:
            score.state = 'FAILED'

    if score.state != 'FAILED':
        validation_result = metrics_json.get('validation_result', {})
        if validation_result.get('status', ) != 'SUCCEEED':
            score.state = 'FAILED'
            score.reason = validation_result.get('reason', 'UNKNOWN REASON')
    if score.state != 'FAILED':
        p95_latency_ns = metrics_json.get('latencies', {}).get('99th', 999999999)
        score.main_indicator = p95_latency_ns / 1_000_000.0

    return score


def prepare_scores_old(challenge_name: str):
    latest_round = Round.objects.filter(challenge_name=challenge_name, state='FINISHED').last()
    if latest_round:
        time_passed_from_last_run = convert_ms_to_minutes((time.time() - latest_round.updated.timestamp()) * 1000)
        latest_scores = Score.objects.filter(round_id=latest_round.id).order_by(
            JSONExtract('result', '$.run_result.duration').asc(nulls_last=True)
        ).all()
    else:
        time_passed_from_last_run = 0
        latest_scores = []
    return latest_scores, time_passed_from_last_run

def prepare_scores(challenge_name: str):
    latest_round = Round.objects.filter(challenge_name=challenge_name, state='FINISHED').last()
    if latest_round:
        time_passed_from_last_run = convert_ms_to_minutes((time.time() - latest_round.updated.timestamp()) * 1000)
        latest_scores = Score.objects.filter(round_id=latest_round.id).order_by(
            F('main_indicator').asc(nulls_last=True)
        ).all()
    else:
        time_passed_from_last_run = 0
        latest_scores = []
    return latest_scores, time_passed_from_last_run