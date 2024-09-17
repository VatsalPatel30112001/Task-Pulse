import random
from celery import shared_task
from .models import *
from decimal import Decimal
from random import randint, uniform
import datetime

@shared_task
def update_machine_axes():
    # Fetch axes for a specific machine and update their values
    axes = Axis.objects.all()
    axis_history_entries = []
    for axis in axes:

        actual_position = round(uniform(-190, 190), 4)
        target_position = round(uniform(-190, 191), 4)

        # Calculate distance_to_go
        distance_to_go = float(Decimal(str(target_position)) - Decimal(str(actual_position)))

        axis.actual_position = actual_position
        axis.target_position = target_position
        axis.distance_to_go = distance_to_go
        axis.homed = uniform(0, 1)>0.5
        axis.acceleration=randint(0, 150)
        axis.velocity=randint(0, 80)     

        axis_history_entries.append(AxisHistory(
            axis=axis,
            actual_position=actual_position,
            target_position=target_position,
            distance_to_go=distance_to_go,
            homed=axis.homed,
            velocity=axis.velocity,
            acceleration=axis.acceleration,
            machine_tool_offset=axis.machine.tool_offset,
            machine_feedrate=axis.machine.feedrate,
            machine_tool_in_use=axis.machine.tool_in_use
        ))        

    # print('buld created and updated.', datetime.datetime.now())
    Axis.objects.bulk_update(axes, ['actual_position', 'target_position', 'distance_to_go', 'homed', 'acceleration', 'velocity'])
    AxisHistory.objects.bulk_create(axis_history_entries)

@shared_task
def update_machine_5min():
    machines = Machine.objects.all()
    for machine in machines:
        machine.tool_in_use = randint(1, machine.tool_capacity)
    Machine.objects.bulk_update(machines, ['tool_in_use'])

@shared_task
def update_machine_15min():
    machines = Machine.objects.all()
    for machine in machines:
        machine.tool_offset = round(uniform(5, 40), 1)
        machine.feedrate = randint(0, 20000)
    Machine.objects.bulk_update(machines, ['tool_offset', 'feedrate'])
