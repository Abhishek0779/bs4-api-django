from django.db import models

# Create your models here.
class movie_details(models.Model):
    movie_name = models.CharField(max_length = 250,blank=True,null=True)
    movie_rating = models.CharField(max_length = 250,blank=True,null=True)
    movie_link = models.CharField(max_length = 250,blank=True,null=True)
    movie_release_date = models.CharField(max_length = 250,blank=True,null=True)
    movie_duration = models.CharField(max_length = 250,blank=True,null=True)
    movie_descriptions = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.movie_name