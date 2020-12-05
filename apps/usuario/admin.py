from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Usuario


class UserCreationForm(forms.ModelForm):
    """Formulario para crear nuevos usuarios. Incluye todos los campos requeridos,
    más la contraseña y confirmacion."""
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'fecha_nac')

    def clean_password2(self):
        # Comprueba que las dos contraseñas coincidan
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Guarda la contraseña en formato hash
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """Formulario para actualizar usuarios. Incluye todos los campos del usuario, pero
    reemplaza la visualizacion del campo de la contraseña con el hash de la contraseña.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'fecha_nac', 'is_active', 'is_admin')

    def clean_password(self):
        # Independientemente de lo que proporcione el usuario, devuelva el valor inicial.
        # Esto se hace aquí, en lugar de en el campo,
        # porque el campo no tiene acceso al valor inicial.
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # formulario para agregar y cambiar instancias de usuario
    form = UserChangeForm
    add_form = UserCreationForm

    # Campos que se utilizarán para mostrar el modelo de usuario.
    # Estos anulan las definiciones en base UserAdmin
    # que hacen referencia a campos específicos en auth.User.
    list_display = ('email', 'fecha_nac', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fecha_nac',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets no es un atributo estándar de ModelAdmin. UserAdmin
    # anula get_fieldsets para utilizar este atributo al crear un usuario.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fecha_nac', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Ahora registra el nuevo UserAdmin...
admin.site.register(Usuario, UserAdmin)
# ... y, dado que no usamos los permisos integrados de Django,
# anula el registro del modelo de grupo de admin.
admin.site.unregister(Group)

