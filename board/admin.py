from django.contrib import admin
from board.models import Board

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display=('idx','writer','title','content')
    
#admin.site.register(Board, BoardAdmin)