from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

class MealViewSet(viewsets.ModelViewSet):
    queryset=Meal.objects.all()
    serializer_class=MealSerializer
    
    @action(methods=['POST'],detail=True)
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            meal=Meal.objects.get(id=pk)
            stars=request.data['stars']
            username=request.data['username']
            user=User.objects.get(username=username)
            try:
                rating=Rating.objects.get(user=user.id,meal=meal.id)
                rating.stars=stars
                rating.save()
                serializer=RatingSerializer(rating,many=False)
                json={
                    'message':'Meal Rate Update',
                    'result':serializer.data
                }
                return Response(json,status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(stars=stars,meal=meal,user=user)
                serializer=RatingSerializer(rating,many=False)
                json={
                    'message':'Meal Rate Creaeted',
                    'result':serializer.data
                }
                return Response(json,status=status.HTTP_200_OK)

        else:
            json={
                'message':'stars not provided'
                    }
            return Response(json,status=status.HTTP_400_BAD_REQUEST)
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer