from django.contrib import admin
from .models import CompareCar, CompareCarUser

class CompareCarAdmin(admin.ModelAdmin):
    list_display = ('title', 'car1', 'car2', 'date_added') 
    list_filter = ('date_added',) 
    search_fields = ('title', 'car1__brand', 'car2__brand')  
    ordering = ('-date_added',)  

    def title(self, obj):
        return obj.title if obj.title else f"{obj.car1.brand} vs {obj.car2.brand}"
    title.short_description = 'Comparison Title'

class CompareCarUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'comparecar') 
    search_fields = ('user__username', 'comparecar__title')  

admin.site.register(CompareCar, CompareCarAdmin)
admin.site.register(CompareCarUser, CompareCarUserAdmin)
