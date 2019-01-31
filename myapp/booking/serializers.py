import inject
from myapp.models.stadium_registers import StadiumRegister
from rest_framework.serializers import (
        ModelSerializer,
        ValidationError,
    )
class BookingCancelSerializer(ModelSerializer):
    class Meta:
        model = StadiumRegister
        fields = ['id', 'status']
    
    def validate(self, data):
        if self.instance.user.id != self.context['request'].user.id:
            raise ValidationError({"permission": "This booking's request is not your booking request"})
        # check current booking request is pending

        if not StadiumRegister.custom_objects.is_pending(self.instance.id):
            raise ValidationError({"booking": "Current booking's request is not pending"})
        return data
