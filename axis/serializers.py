from rest_framework import serializers
from .models import *

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['machine_id', 'machine_name', 'tool_capacity', 'tool_offset', 'feedrate', 'tool_in_use']
        extra_kwargs = {
            'machine_id': {'read_only': True}  # machine_id is read-only and will be auto-assigned
        }
    
class AxisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Axis
        fields = ['id', 'machine', 'axis_name', 'max_acceleration', 'max_velocity', 
                  'actual_position', 'target_position', 'distance_to_go', 
                  'homed', 'acceleration', 'velocity']

class AxisHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AxisHistory
        fields = '__all__'  # or specify the fields you want to include
