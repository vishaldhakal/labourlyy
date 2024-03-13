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
        workcategory = data.get('work_category')
        print("Work category is: ", workcategory)
        if workcategory:
            if workcategory == 'All':
                laborers = Labour.objects.all()
            else:
                laborers = Labour.objects.filter(work_category__name=workcategory,cost_per_day__lte=max_cost_per_day)
        else:
            laborers = Labour.objects.filter(cost_per_day__lte=max_cost_per_day)
            
        matched_laborers = []
        for laborer in laborers:
            c_score = cost_score(min_cost_per_day, max_cost_per_day, laborer.cost_per_day)
            e_score = expertise_score(required_expertise, laborer.expertise_level)
            s_score = laborer.avg_sentiment_score()

            """ print("Scores are: ", c_score, e_score, s_score) """

            w_score = 0.2 * c_score + 0.2 * e_score + 0.6 * s_score
            """ print("w_score : " + str(w_score)) """
            laborer_data = {
                'id': laborer.id,
                'name': laborer.name,
                'email': laborer.email,
                'phone': laborer.phone,
                'address': laborer.address,
                'job_type': laborer.job_type,
                'cost_per_day': laborer.cost_per_day,
                'expertise_level': laborer.expertise_level,
                'city': laborer.city,
                'state': laborer.state,
                'pincode': laborer.pincode,
                'created_at': laborer.created_at,
                'updated_at': laborer.updated_at,
                'avatar': laborer.avatar.url if laborer.avatar else None,
                "work_category": {
                    "name": laborer.work_category.name,
                },
                'weighted_score': w_score
            }
            matched_laborers.append(laborer_data)

        # Sort the matched laborers based on weighted score
        matched_laborers.sort(key=lambda x: x['weighted_score'], reverse=True)

        # Return only the top 30 matches
        top_30_matches = matched_laborers[:30]
        print("Top 30 matches are: ", top_30_matches)

        return Response(top_30_matches)
