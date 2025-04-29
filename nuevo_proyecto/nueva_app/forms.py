# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Tag, Comment

# Formulario para el registro de usuario
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electronico")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Formulario para el login de usuario
class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electronico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


# Formulario para crear o editar un post
class PostForm(forms.ModelForm):
    # Especificamos el modelo y los campos que queremos mostrar en el formulario
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Incluir 'tags' en los campos del formulario
        widgets = {
            'tags': forms.CheckboxSelectMultiple  # Utilizamos Checkboxes para seleccionar múltiples tags
        }

    # Este campo es para seleccionar múltiples tags para el post
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  # Obtiene todos los tags disponibles en la base de datos
        widget=forms.CheckboxSelectMultiple,  # Usamos casillas de verificación
        required=False,  # Esto permite que el post se cree sin necesidad de seleccionar tags
        label="Selecciona los tags"  # Etiqueta para el campo
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']