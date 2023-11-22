from rest_framework import serializers
from .models import Attendence

class AttendenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = '__all__'
        read_only_fields = ['isApprooved']

class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = '__all__'
    
    def update(self, instance, validated_data):
        # Check if the user making the request is an admin
        user = self.context['request'].user
        if user.role == 'admin':
            print('-------------------------------','admin',instance.isApprooved,validated_data)
            # Allow admin users to update the isApproved field
            instance.isApprooved = validated_data.get('isApprooved', instance.isApprooved)
        # Ignore isApprooved field if the user is not an admin
        validated_data.pop('isApprooved', None)
        
        # Update the other fields as usual
        instance.user = validated_data.get('user', instance.user)
        instance.date = validated_data.get('date', instance.date)
        instance.checkin = validated_data.get('checkin', instance.checkin)
        instance.checkout = validated_data.get('checkout', instance.checkout)
        instance.status = validated_data.get('status', instance.status)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        
        instance.save()
        return instance
