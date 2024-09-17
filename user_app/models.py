from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    ADMIN = 'admin'
    MANAGER = 'manager'
    OPERATOR = 'operator'
    SUPERVISOR = 'supervisor'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (OPERATOR, 'Operator'),
        (SUPERVISOR, 'Supervisor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=OPERATOR)
    
    def __str__(self):
        return f'{self.user.username} - {self.role}'
