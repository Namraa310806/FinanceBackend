from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction create, update, and read operations."""

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        error_messages={
            'required': 'Amount is required.',
            'invalid': 'Amount must be a valid number.',
        },
    )
    type = serializers.ChoiceField(
        choices=Transaction.Type.choices,
        error_messages={
            'required': 'Transaction type is required.',
            'invalid_choice': 'Type must be either INCOME or EXPENSE.',
        },
    )
    category = serializers.CharField(
        max_length=100,
        error_messages={
            'required': 'Category is required.',
            'blank': 'Category cannot be blank.',
            'max_length': 'Category cannot exceed 100 characters.',
        },
    )
    date = serializers.DateField(
        error_messages={
            'required': 'Date is required.',
            'invalid': 'Date must be in YYYY-MM-DD format.',
        }
    )
    notes = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Transaction
        fields = (
            'id',
            'amount',
            'type',
            'category',
            'date',
            'notes',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def validate_category(self, value):
        cleaned_value = value.strip()
        if not cleaned_value:
            raise serializers.ValidationError('Category cannot be blank.')
        return cleaned_value


class TransactionFilterSerializer(serializers.Serializer):
    """Validate transaction-list query parameters."""

    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    category = serializers.CharField(required=False, allow_blank=False)
    type = serializers.ChoiceField(
        choices=Transaction.Type.choices,
        required=False,
        error_messages={'invalid_choice': 'Type filter must be either INCOME or EXPENSE.'},
    )

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError('start_date cannot be later than end_date.')

        return attrs
