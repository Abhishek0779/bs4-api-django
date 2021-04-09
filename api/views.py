from django.shortcuts import get_object_or_404, redirect, render
from bs4 import BeautifulSoup
import requests
import re
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from rest_framework import permissions


def get_movies_from_imdb(request):
    movie_details.objects.all().delete()

    urls = 'http://www.imdb.com/chart/top?ref_=nv_mv_250'
    response = requests.get(urls)
    soup = BeautifulSoup(response.text,'html.parser')

    movies = soup.select('td.titleColumn')
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    

    imdb = []

    for index in range(0, len(movies)):
        movie_string = movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index))+1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        place = movie[:len(str(index))-(len(movie))]
        data = {"movie_title": movie_title+' ('+year+')',
                "id": place, 
                "rating": ratings[index],
                "link": "https://www.imdb.com"+links[index]}
        imdb.append(data)
        
        obj = movie_details(id=data['id'],movie_name=data["movie_title"],movie_rating=data["rating"],movie_link=data["link"])
        obj.save()
    return redirect('/get/')

def get_details(request):
    get_url = movie_details.objects.all()

    for i in range(len(get_url)):
        id = get_url[i].id
        url = get_url[i].movie_link
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')

        release_date = soup.find_all('time')[0].text;
        duration = soup.find_all('a', title='See more release dates')[0].text;
        description = soup.find_all('div', class_='summary_text')[0].text;
        
        movie_details.objects.filter(id=id).update(movie_release_date=release_date.strip(),movie_duration=duration.strip(),movie_descriptions=description.strip())
    return redirect('/')

class movie_detailsListCreateAPIView(ListCreateAPIView):
    queryset = movie_details.objects.all()
    serializer_class = movie_detailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['movie_name', 'movie_descriptions']
    ordering_fields = ['movie_name','movie_rating','movie_release_date','movie_duration']
   
    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
       queryset = movie_details.objects.all()
       return queryset

class movie_detailsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = movie_detailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(movie_details, pk=self.kwargs.get("id"))