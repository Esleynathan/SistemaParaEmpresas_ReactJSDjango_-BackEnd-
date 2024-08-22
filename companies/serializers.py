from django.contrib.auth.models import Permission
from rest_framework import serializers

from accounts.models import User, Group, User_Groups, Group_Permissions
from companies.models import Employee, Task

class EmployeesSerializer (serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email',
        )

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email

class EmployeeSerializer (serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email',
            'groups',
        )

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email

    def get_groups(self, obj):
        groupsDB = User_Groups.objects.filter(user_id=obj.user.id).all()
        groupsDATA = []

        for group in groupsDB:
            groupsDATA.append({
                "id": group.group.id,
                "name": group.group.name
            })

        return groupsDATA

class GroupsSerializer (serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions'
        )
        
    def get_permissions(self, obj):
        groups = Group_Permissions.objects.filter(group_id=obj.id).all()
        permissionsDATA = []

        for group in groups:
            permissionsDATA.append({
                "id": group.permission.id,
                "label": group.permission.name,
                "codename": group.permission.codename,
            })

        return permissionsDATA

class PermissionsSerializer (serializers.ModelSerializer):    
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'codename'
        )

class TasksSerializer (serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'description',
            'due_data',
            'created_at',
            'status',
        )

    def get_status(self, obj):
        return obj.status.nome

class TaskSerializer (serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    
    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'description',
            'due_data',
            'created_at',
            'status',
            'employee'
        )

    def get_status(self, obj):
        return obj.status.nome
        
    def get_employee(self, obj):
        return EmployeeSerializer(obj.employee).data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.title)        
        instance.due_date = validated_data.get('due_date', instance.title)
        instance.status_id = validated_data.get('status_id', instance.title)
        instance.employee_id = validated_data.get('title', instance.title)

        instance.save()

        return instance