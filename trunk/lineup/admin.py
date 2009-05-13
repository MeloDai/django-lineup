from django.contrib import admin
from lineup.models import Queue, QueueParam

class QueueParamAdmin(admin.TabularInline):
    model = QueueParam
    
class QueueAdmin(admin.ModelAdmin):
    inlines = [
        QueueParamAdmin,
    ]
    
admin.site.register(Queue, QueueAdmin)

