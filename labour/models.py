from django.db import models
from django.db.models import Avg

class WorkCategory(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.name

   class Meta:
      ordering = ['created_at']

class Labour(models.Model):
   EXPERTISE = (
      (1, 'Beginner'),
      (2, 'Intermediate'),
      (3, 'Advanced'),
      (4, 'Expert'),
      (5, 'Master'),
   )
   name = models.CharField(max_length=100)
   email = models.EmailField(max_length=100)
   phone = models.CharField(max_length=15)
   address = models.TextField()
   job_type = models.CharField(max_length=100)
   cost_per_day = models.FloatField( default=0.0 )
   expertise_level  = models.IntegerField(choices=EXPERTISE, default=1)
   city = models.CharField(max_length=100)
   state = models.CharField(max_length=100)
   pincode = models.CharField(max_length=10)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   avatar = models.ImageField(upload_to='labour/avatars/', blank=True, null=True)
   work_category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, related_name='labourers')

   def __str__(self):
      return self.name

   def get_work_category(self):
      return self.work_category.name
   
   def avg_sentiment_score(self):
      return float(self.reviews.aggregate(Avg('sentiment_score'))['sentiment_score__avg'] or 0)
   
   class Meta:
      ordering = ['created_at']
