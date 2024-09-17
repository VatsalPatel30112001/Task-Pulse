from django.db import models
from rest_framework.exceptions import ValidationError
from decimal import Decimal

class Machine(models.Model):
    machine_id = models.BigAutoField(primary_key=True, auto_created=True)  # Machine ID
    machine_name = models.CharField(max_length=100)     # Machine Name
    tool_capacity = models.IntegerField(default=24)     # Tool Capacity
    tool_offset = models.FloatField(default=14.5)       # Tool Offset (Range: 5 to 40)
    feedrate = models.FloatField(default=10000)         # Feedrate (Range: 0 to 20000)
    tool_in_use = models.IntegerField(default=1)        # Tool in use (Range: 1 to 'tool_capacity')

    def __str__(self):
        return self.machine_name

    def clean(self):
        super().clean()  # Call the parent's clean method
        
        # Validate tool_offset
        if not (5 <= self.tool_offset <= 40):
            raise ValidationError({'tool_offset': 'Tool offset must be between 5 and 40.'})
        
        # Validate feedrate
        if not (0 <= self.feedrate <= 20000):
            raise ValidationError({'feedrate': 'Feedrate must be between 0 and 20000.'})
        
        # Validate tool_in_use
        if not (1 <= self.tool_in_use <= self.tool_capacity):
            raise ValidationError({'tool_in_use': f'Tool in use must be between 1 and {self.tool_capacity}.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Axis(models.Model):    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='axes')  # Link to Machine
    axis_name = models.CharField(max_length=1, default='X')       # Axis Name
    
    # Constant Fields
    max_acceleration = models.FloatField(default=200)
    max_velocity = models.FloatField(default=60)
    
    # Variable Fields
    actual_position = models.FloatField(default=0)
    target_position = models.FloatField(default=0)
    distance_to_go = models.FloatField(default=0)
    homed = models.BooleanField(default=False)
    acceleration = models.FloatField(default=0)
    velocity = models.FloatField(default=0)

    class Meta:
        # Ensures that each machine can only have one axis with a given axis_name
        constraints = [
            models.UniqueConstraint(fields=['machine', 'axis_name'], name='unique_machine_axis')
        ]

    def clean(self):
        super().clean()  # Call the parent's clean method

        # Validate actual_position and target_position
        if not (-190 <= self.actual_position <= 190):
            raise ValidationError({'actual_position': 'Actual position must be between -190 and 190.'})
        if not (-190 <= self.target_position <= 191):
            raise ValidationError({'target_position': 'Target position must be between -190 and 191.'})
        
        # Validate distance_to_go
        expected_distance_to_go = Decimal(str(self.target_position)) - Decimal(str(self.actual_position))
    
        if not (Decimal(str(self.distance_to_go)) == expected_distance_to_go):
            raise ValidationError({'distance_to_go': 'Distance to go must be equal to target position minus actual position.'})
        
        # Validate homed
        if self.homed not in [0, 1]:
            raise ValidationError({'homed': 'Homed field must be either 0 or 1.'})
        
        # Validate acceleration and velocity
        if not (0 <= self.acceleration <= 150):
            raise ValidationError({'acceleration': 'Acceleration must be between 0 and 150.'})
        if not (0 <= self.velocity <= 80):
            raise ValidationError({'velocity': 'Velocity must be between 0 and 80.'})

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation before saving
        # Automatically update distance_to_go before saving
        self.distance_to_go = float(Decimal(str(self.target_position)) - Decimal(str(self.actual_position)))
        super().save(*args, **kwargs)
        
        # Log the history on every save, including machine data
        AxisHistory.objects.create(
            axis=self,
            actual_position=self.actual_position,
            target_position=self.target_position,
            distance_to_go=self.distance_to_go,
            homed=self.homed,
            velocity=self.velocity,
            acceleration=self.acceleration,
            machine_tool_offset=self.machine.tool_offset,
            machine_feedrate=self.machine.feedrate,
            machine_tool_in_use=self.machine.tool_in_use
        )

    def __str__(self):
        return f"Axis {self.axis_name} on Machine {self.machine.machine_name}"

class AxisHistory(models.Model):
    axis = models.ForeignKey(Axis, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    actual_position = models.FloatField()
    target_position = models.FloatField()
    distance_to_go = models.FloatField()
    homed = models.BooleanField()
    velocity = models.FloatField()
    acceleration = models.FloatField()
    
    # Machine fields to track changes in AxisHistory
    machine_tool_offset = models.FloatField()
    machine_feedrate = models.FloatField()
    machine_tool_in_use = models.IntegerField()

    def save(self, *args, **kwargs):
        super(AxisHistory, self).save(*args, **kwargs)

    def __str__(self):
        return f"History of {self.axis} at {self.timestamp}"