from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.exceptions import ValidationError
from random import randint, uniform
from .models import *
import ast
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Create your views here.

class MachineCRUDOperation(APIView):
    def get(self, request):
        id = request.GET.get('id', None)
        axes = request.GET.get('axes', [])
        if axes and not isinstance(axes, list):
            axes = ast.literal_eval(axes)

        if not id or not(isinstance(axes, list)):
            return JsonResponse({
                'status': 'fail',
                'message': 'Please provide proper machine id with axes list.'
            }, status=404)

        id = int(id)
        machine_obj = Machine.objects.filter(machine_id=id).first()

        if not machine_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Machine with provided ID does not exist.'
            }, status=404)

        if len(axes)>0:
            now = timezone.now()
            fifteen_minutes_ago = now - timedelta(minutes=15)

            queryset = AxisHistory.objects.filter(
                    axis__machine=machine_obj, 
                    axis__axis_name__in=axes, 
                    timestamp__gte=fifteen_minutes_ago,  # Filter for records after 15 minutes ago
                    timestamp__lte=now).order_by('timestamp')

            serializer = AxisHistorySerializer(queryset, many=True)

        else:
            # Serialize the data
            serializer = MachineSerializer(machine_obj)

        return JsonResponse({
            'status': 'success',
            'data': serializer.data if serializer else []
        }, status=200)

    def post(self, request):
        machine_data = request.data
        if machine_data['tool_in_use']: machine_data['tool_in_use'] = None
        # Serialize the data, note that `machine_id` is not included here
        serializer = MachineSerializer(data=machine_data)
        
        if serializer.is_valid():
            machine = serializer.save()  # `machine_id` will be auto-assigned

            # axes = ['X', 'Y', 'Z', 'A', 'C']
            # for axis_name in axes:

            #     actual_position = round(uniform(-190, 190), 4)
            #     target_position = round(uniform(-190, 191), 4)

            #     # Calculate distance_to_go
            #     distance_to_go = Decimal(str(target_position)) - Decimal(str(actual_position))

            #     Axis.objects.create(
            #         machine=machine,
            #         axis_name=axis_name,
            #         max_acceleration=uniform(0, 150),  # Example dynamic value
            #         max_velocity=uniform(0, 80),       # Example dynamic value
            #         actual_position=actual_position, # Example dynamic value
            #         target_position=target_position, # Example dynamic value
            #         distance_to_go=distance_to_go,     # Example dynamic value
            #         homed=uniform(0, 1) > 0.5,          # Randomly True or False
            #         acceleration=randint(0, 150),       # Random int for acceleration
            #         velocity=randint(0, 80)             # Example dynamic value
            #     )

            return JsonResponse({
                'status': 'success',
                'message': 'Machine created successfully.',
                'machine_id': serializer.data['machine_id']
            }, status=201)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

    def put(self, request, id):
        # Fetch the Machine instance
        machine_obj = Machine.objects.filter(machine_id=id).first()

        if not machine_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Machine with provided ID does not exist.'
            }, status=404)

        # Serialize the data with partial update
        serializer = MachineSerializer(machine_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Machine updated successfully.',
                'machine_id': serializer.data['machine_id']
            }, status=200)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

    def delete(self, request, id):
        # Fetch the Machine instance
        machine_obj = Machine.objects.filter(machine_id=id).first()

        if not machine_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Machine with provided ID does not exist.'
            }, status=404)

        # Delete the Machine instance
        try:
            machine_obj.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Machine deleted successfully.'
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'status': 'fail',
                'message': f'Error deleting machine: {e}'
            }, status=500)


class AxisCRUDOperation(APIView):
    def get(self, request, id):
        # Fetch the Axis instance
        axis_obj = Axis.objects.filter(id=id).first()

        if not axis_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Axis with provided ID does not exist.'
            }, status=404)

        # Serialize the data
        serializer = AxisSerializer(axis_obj)

        return JsonResponse({
            'status': 'success',
            'data': serializer.data
        }, status=200)

    def post(self, request):
        axis_data = request.data

        # Serialize the data
        serializer = AxisSerializer(data=axis_data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Axis created successfully.',
                'axis_id': serializer.data['id']
            }, status=201)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

    def put(self, request, id):
        # Fetch the Axis instance
        axis_obj = Axis.objects.filter(id=id).first()

        if not axis_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Axis with provided ID does not exist.'
            }, status=404)

        # Serialize the data with partial update
        serializer = AxisSerializer(axis_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Axis updated successfully.',
                'axis_id': serializer.data['id']
            }, status=200)
        else:
            return JsonResponse({
                'status': 'fail',
                'message': 'Invalid data provided.',
                'errors': serializer.errors
            }, status=400)

    def delete(self, request, id):
        # Fetch the Axis instance
        axis_obj = Axis.objects.filter(id=id).first()

        if not axis_obj:
            return JsonResponse({
                'status': 'fail',
                'message': 'Axis with provided ID does not exist.'
            }, status=404)

        # Delete the Axis instance
        try:
            axis_obj.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Axis deleted successfully.'
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'status': 'fail',
                'message': f'Error deleting axis: {e}'
            }, status=500)

