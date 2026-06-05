from django.contrib import admin
from .models import Space, Branch, PhoneNumber, SocialMedia

class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1  

class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [PhoneNumberInline, SocialMediaInline]

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'space')




# Register your models here.
