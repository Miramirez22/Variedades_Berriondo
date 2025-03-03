from django import forms
from django.contrib.auth.models import User

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name"]
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
        user.set_password(self.cleaned_data["password"])  # Guarda la contraseña cifrada
        if commit:
            user.save()
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
        
