from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UsuarioManager(BaseUserManager):
    def create_user(self, email, fecha_nac, password=None):
        """
        Crea y guarda un Usuario con el correo electrónico dado, fecha de
        nacimiento y contraseña.
        """
        if not email:
            raise ValueError('Los usuarios deben tener una dirección de correo electrónico')

        user = self.model(
            email=self.normalize_email(email),
            fecha_nac=fecha_nac,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fecha_nac, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            fecha_nac=fecha_nac,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email = models.EmailField('correo electrónico', max_length=255, unique=True)
    fecha_nac = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fecha_nac']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Tiene el usuario un permiso específico?"
        # Respuesta más simple posible: Sí, siempre
        return True

    def has_module_perms(self, app_label):
        "Tiene el usuario permisos para ver la app `app_label`?"
        # Respuesta más simple posible: Sí, siempre
        return True

    @property
    def is_staff(self):
        "El usuario es del staff?"
        # La respuesta más simple posible: todos los admin son del staff
        return self.is_admin

