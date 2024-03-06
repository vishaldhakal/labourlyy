from django.contrib import admin
from .models import Customer, LaborBooking, Review

admin.site.register(Customer)
admin.site.register(LaborBooking)

# show all column of review in admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('laborer', 'customer','text', 'sentiment_score')

admin.site.register(Review, ReviewAdmin)