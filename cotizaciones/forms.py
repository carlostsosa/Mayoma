from django import forms

class CotizacionForm(forms.Form):
    nombre = forms.CharField(max_length=200, label="Nombre completo",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}))
    email = forms.EmailField(label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}))
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+52 555 123 4567"}))
    mensaje = forms.CharField(required=False, label="Comentarios",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Notas adicionales..."}))
