from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer (data=request.data)
        serializer.is_valid (raise_exception=True) 
        self.perform_create (serializer) 
        token, created = Token.objects.get_or_create(user=serializer.instance) 
        return Response({ 'token': token.key, }, status=status.HTTP_201_CREATED)
    
    
    def list(self, request, *args, **kwargs):
        response = { 'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    queryset=Meal.objects.all()
    serializer_class=MealSerializer
    
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    
    @action(methods=['POST'],detail=True)
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            meal=Meal.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user
            # username=request.data['username']
            # user=User.objects.get(username=username)

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
    
    authentication_classes=(TokenAuthentication)
    permission_classes=(IsAuthenticated)
    
    def update(self,request,*args, **kwargs):
        response={
            'message':'This is not how you should create/update'
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    def create(self,request,*args, **kwargs):
        response={
            'message':'This is not how you should create/update'
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)