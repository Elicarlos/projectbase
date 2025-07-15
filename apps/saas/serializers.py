from rest_framework import serializers
from  . models  import Organization, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer)
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "owner", "plan", "is_trial", "trial_ends_at", "is_active"]
        read_only_fields = ["owner"]