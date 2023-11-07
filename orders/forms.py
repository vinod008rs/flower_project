from django import forms
from django.core.exceptions import ValidationError

from orders.models import Product


class OrderForm(forms.Form):
    customer_name = forms.CharField(max_length=100, label='Name')
    customer_phone = forms.CharField(max_length=15, label='Phone Number')
    customer_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 33}), label='Address')
    customer_email = forms.EmailField(label='Email Address')
    order_data = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 33}),
        label='Enter your order',
        help_text='Example:\n10 R12\n15 L09\n13 T58'
    )

    def clean_order_data(self):
        order_data = self.cleaned_data['order_data']
        lines = order_data.strip().split("\n")
        invalid_lines = []
        invalid_codes = []
        code = None
        for line in lines:
            try:
                parts = line.split()
                # Check if each line has exactly 2 parts (quantity and code)
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                quantity, code = parts
                # Further checks can be added here, such as checking if quantity is a number
                if not quantity.isdigit():
                    raise ValueError("Quantity must be a number")
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than 0")
                # Check if the product code exists in the database
                Product.objects.get(code=code)
            except Product.DoesNotExist:
                invalid_codes.append(code)
            except ValueError as e:
                # You can customize the message based on the exception message if needed
                invalid_lines.append(f"{line} ({str(e)})")

        # Combine all error messages
        error_messages = []
        if invalid_lines:
            error_messages.append(f"Invalid line format: {', '.join(invalid_lines)}")
        if invalid_codes:
            error_messages.append(f"Invalid product codes: {', '.join(invalid_codes)}")

        if error_messages:
            raise ValidationError(" ".join(error_messages))

        return order_data
