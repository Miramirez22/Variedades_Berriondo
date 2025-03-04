from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

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
    
class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('tarjeta_credito', 'Tarjeta de crédito'),
        ('tarjeta_debito', 'Tarjeta de débito'),
        ('efectivo', 'Efectivo'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect)
    card_number = forms.CharField(max_length=16, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    expiration_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
    cvv = forms.CharField(max_length=3, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    efectivo = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

