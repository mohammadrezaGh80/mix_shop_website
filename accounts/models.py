from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _

from accounts.validators import UsernameValidator, PhoneValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            **extra_fields
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username_validator = UsernameValidator()
    phone_validator = PhoneValidator()

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('150 characters or fewer. Letters, digits and ./-/_ only '
                    'which starts with letters and has at least 4 characters.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(verbose_name=_('First name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=150, blank=True, null=True)
    phone = models.CharField(verbose_name=_('Phone'), unique=True, max_length=11,
                             blank=True, null=True, validators=[phone_validator])
    birth_date = models.DateField(verbose_name=_('Birth date'), blank=True, null=True)

    is_active = models.BooleanField(verbose_name=_('Is active?'), default=False)
    is_admin = models.BooleanField(verbose_name=_('Is admin?'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
