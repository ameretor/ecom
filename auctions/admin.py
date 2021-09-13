from django.contrib import admin
from .models import User, Gender, category, listing, Comments, watchList

# Register your models here.
admin.site.register(User)
admin.site.register(Gender)
admin.site.register(category)
admin.site.register(listing)
admin.site.register(Comments)
admin.site.register(watchList)
