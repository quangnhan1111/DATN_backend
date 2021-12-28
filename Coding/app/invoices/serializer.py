from rest_framework import serializers

from invoices.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

    def create(self, validated_data):
        invoice = Invoice.objects.create(**validated_data)
        invoice.save()
        return invoice

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.message = validated_data.get('message', instance.message)
        instance.totalPrice = validated_data.get('totalPrice', instance.totalPrice)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.employee = validated_data.get('staff', instance.employee)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()
        return instance
