from django.contrib import admin
from JIRA_multi_board_view.models import BoardDefinition, EpicDefinition


class BoardDefinitionAdmin(admin.ModelAdmin):
    pass

class EpicDefinitionAdmin(admin.ModelAdmin):
	pass

admin.site.register(BoardDefinition, BoardDefinitionAdmin)
admin.site.register(EpicDefinition, EpicDefinitionAdmin)
