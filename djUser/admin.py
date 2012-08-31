from django.contrib import admin
from djUser.models import User,Token,TimeStamp,FileBox

admin.site.register(User)
admin.site.register(Token)
admin.site.register(TimeStamp)
admin.site.register(FileBox)
