from django.contrib import admin
from evaluArt.models import UserProfile, ContactUs

# Register your models here.
admin.site.register(UserProfile)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'

admin.site.register(ContactUs, ContactUsAdmin)