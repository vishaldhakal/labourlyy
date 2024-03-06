from django.db import models
from django.contrib.auth.models import User
from labour.models import Labour, WorkCategory
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import joblib


class Customer(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
   name = models.CharField(max_length=100)
   email = models.EmailField(max_length=100)
   phone = models.CharField(max_length=15)
   address = models.TextField()
   city = models.CharField(max_length=100)
   state = models.CharField(max_length=100)
   pincode = models.CharField(max_length=10)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return self.name
   
   class Meta:
      ordering = ['created_at']

class LaborBooking(models.Model):
   laborer = models.ForeignKey(Labour, on_delete=models.CASCADE, related_name='bookings')
   customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sbookings')
   start_date = models.DateField()
   end_date = models.DateField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   booking_price = models.DecimalField(max_digits=10, decimal_places=2)
   remarks = models.TextField(null=True, blank=True)
   no_of_days = models.IntegerField()
   work_category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE, related_name='bookings')
   booking_status = models.CharField(max_length=100, default='Initiated')

   def __str__(self):
      return f'{self.customer.name} - {self.laborer.name}'

class Review(models.Model):
   laborer = models.ForeignKey(Labour, on_delete=models.CASCADE, related_name='reviews')
   text = models.TextField()
   customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
   sentiment_score = models.FloatField(null=True, blank=True)

   def __str__(self):
      return f'Review for {self.laborer.name} = {self.sentiment_score}'
   
   class Meta:
      ordering = ['laborer', '-sentiment_score']

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Review)
def add_sentiment_score(sender, instance, **kwargs):
    if kwargs.get('update_fields') is None or 'text' in kwargs.get('update_fields'):
        instance.sentiment_score = predict_sentiment(instance.text)
        instance.save(update_fields=['sentiment_score'])        

def predict_sentiment(review):
    # Load the trained model
    model = joblib.load('sentiment_model.pkl')

    # Load the CountVectorizer
    vectorizer = joblib.load('count_vectorizer.pkl')
    
    # Transform the review using the vectorizer
    review_vectorized = vectorizer.transform([review])

    # Predict probability scores for each class
    prob_scores = model.predict_proba(review_vectorized)

    # Get the probability score for the positive class
    positive_score = prob_scores[0][1]
    print("positive_score")

    return positive_score