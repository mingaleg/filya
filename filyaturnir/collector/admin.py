from django.contrib import admin
from collector.models import Submit, Battle, BattleSerial

def admin_submit(modeladmin, request, queryset):
    for foo in queryset.order_by("sid"):
        foo.reset()
    for foo in queryset.order_by("sid"):
        foo.submit()
admin_submit.short_description = 'Submit'

class SubmitAdmin(admin.ModelAdmin):
    actions = (admin_submit,)
    list_display = ('sid', 'time', 'source_file', 'user', 'language', 'status', 'current')

def run(modeladmin, request, queryset):
    for foo in queryset:
        foo.run()
run.short_description = "Run"

class BattleAdmin(admin.ModelAdmin):
    actions = (run,)
    list_display = ('sid', 'time', 'player1', 'player2', 'winner', 'score', 'status', 'done', 'success')

class BattleSerialAdmin(admin.ModelAdmin):
    actions = (run,)
    list_display = ('sid', '__str__')

admin.site.register(Submit, SubmitAdmin)
admin.site.register(Battle, BattleAdmin)
admin.site.register(BattleSerial, BattleSerialAdmin)
