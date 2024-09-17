from django.contrib import admin
from .models import *
# Register your models here.

class MachineAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('machine_id', 'machine_name', 'tool_capacity', 'tool_offset', 'feedrate', 'tool_in_use')
    
    # Fields to add filters for in the right sidebar
    list_filter = ('tool_capacity', 'tool_offset', 'feedrate', 'tool_in_use')

class AxisAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('machine', 'axis_name', 'actual_position', 'target_position', 'velocity', 'acceleration', 'distance_to_go', 'homed')
    
    # Fields to add filters for in the right sidebar
    list_filter = ('machine', 'axis_name', 'homed')

class AxisHistoryAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('axis', 'timestamp', 'actual_position', 'target_position', 'distance_to_go', 'velocity', 'acceleration', 'machine_tool_offset', 'machine_feedrate', 'machine_tool_in_use')
    
    # Fields to add filters for in the right sidebar
    list_filter = ('axis', 'timestamp')

admin.site.register(Machine, MachineAdmin)
admin.site.register(Axis, AxisAdmin)
admin.site.register(AxisHistory, AxisHistoryAdmin)