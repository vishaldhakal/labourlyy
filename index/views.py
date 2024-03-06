from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from labour.models import Labour
from labour.serializers import LabourSerializer

def cost_score(min_cost, max_cost, laborer_cost):
    if laborer_cost <= min_cost:
        return 1
    elif laborer_cost >= max_cost:
        return 0
    else:
        return 1 - (abs(min_cost - laborer_cost)) / (max_cost - min_cost)

def expertise_score(required_expertise, laborer_expertise):
    return max(0, 1 - abs(required_expertise - laborer_expertise) / 5)


class MatchLabourersAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            min_cost_per_day = float(data.get('min_cost_per_day'))
            max_cost_per_day = float(data.get('max_cost_per_day'))
            required_expertise = int(data.get('required_expertise'))

        except (ValueError, TypeError, KeyError):
            return Response({'error': 'Invalid request data'}, status=400)

        laborers = Labour.objects.all()
        matched_laborers = []
        for laborer in laborers:
            c_score = cost_score(min_cost_per_day, max_cost_per_day, laborer.cost_per_day)
            e_score = expertise_score(required_expertise, laborer.expertise_level)
            s_score = laborer.avg_sentiment_score()

            print("Scores are: ", c_score, e_score, s_score)

            w_score = 0.2 * c_score + 0.2 * e_score + 0.6 * s_score
            print("w_score : " + str(w_score))
            laborer_data = {
                'id': laborer.id,
                'name': laborer.name,
                'cost_per_day': laborer.cost_per_day,
                'expertise_level': laborer.expertise_level,
                'avg_sentiment_score': s_score,
                'weighted_score': w_score,
                'avatar': laborer.avatar.url if laborer.avatar else None,
                'work_category': laborer.work_category.name,
            }
            matched_laborers.append(laborer_data)

        # Sort the matched laborers based on weighted score
        matched_laborers.sort(key=lambda x: x['weighted_score'], reverse=True)

        # Return only the top 30 matches
        top_30_matches = matched_laborers[:30]

        return Response(top_30_matches)
