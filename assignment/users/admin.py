from django.contrib import admin
from users.models import *


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['first_name','last_name','email']}),
        (None, {'fields': ['mailing_lists','tr_referral']}),
        ('Contacts', {'fields': ['city','country','street_number','zipcode','phone'], 'classes': ['collapse']}),
        ('Personal info',{'fields' : ['birth_date','gender']}),
        ('Other',{'fields': ['lead','utm_campaign','utm_medium','utm_source','tr_input_method','tr_ip_address','tr_language'], 'classes': ['collapse']})
    )
    list_display = ('first_name', 'last_name','email')
    search_fields = ('first_name', 'last_name','email')
    list_filter = ('country','city','gender','tr_language','mailing_lists')
    
admin.site.register(User,UserAdmin)
admin.site.register(MailingList)
admin.site.register(Referral)

