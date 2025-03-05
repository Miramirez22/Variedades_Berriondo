from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Address, PaymentMethod, Order
from general.models import Producto

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña", required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Dirección", required=False)
    payment_method = forms.ChoiceField(choices=[
        ('tarjeta_credito', 'Tarjeta de crédito'),
        ('tarjeta_debito', 'Tarjeta de débito'),
        ('efectivo', 'Efectivo'),
    ], widget=forms.RadioSelect, label="Método de pago", required=False)
    card_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Número de tarjeta", required=False)
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), label="Fecha de expiración", required=False)
    cvv = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="CVV", required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "address", "payment_method", "card_number", "expiration_date", "cvv"]
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "first_name": "Nombre",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])  # Guarda la contraseña cifrada
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.address = self.cleaned_data['address']
            user_profile.payment_method = self.cleaned_data['payment_method']
            user_profile.card_number = self.cleaned_data['card_number']
            user_profile.expiration_date = self.cleaned_data['expiration_date']
            user_profile.cvv = self.cleaned_data['cvv']
            user_profile.save()
        return user

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="Número de tarjeta", required=True)
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}), label="Fecha de expiración", required=True)
    cvv = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label="CVV", required=True)

    class Meta:
        model = UserProfile
        fields = ["card_number", "expiration_date", "cvv"]

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Celular", required=False)

    class Meta:
        model = UserProfile
        fields = ['phone_number']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'is_preferred']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'is_preferred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['card_number', 'expiration_date', 'cvv', 'is_preferred']
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
            'is_preferred': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña actual")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Nueva contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar nueva contraseña")


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen'] 


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_amount', 'items']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'items': forms.Textarea(attrs={'class': 'form-control'}),
        }

