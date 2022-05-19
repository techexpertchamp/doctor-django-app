from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from doctor.constants import MALE, FEMALE, OTHER, ENGLISH, MANDARIN, HINDI, SPANISH, FRENCH, ARABIC, BENGALI, RUSSIAN, \
    PORTUGUESE, INDONESIAN


def upload_to(instance, filename):
    return f'images/{filename}'


class UserManager(BaseUserManager):

    def create_user(self, password=None, **kwargs):
        if not kwargs.get('email'):
            raise TypeError('User should have a Email')

        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class Doctor(AbstractBaseUser):
    GenderTypes = [
        (MALE, MALE),
        (FEMALE, FEMALE),
        (OTHER, OTHER)
    ]
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=50, choices=GenderTypes, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    @property
    def languages(self):
        try:
            languages = SpokenLanguages.objects.filter(doctor=self)
        except SpokenLanguages.DoesNotExist:
            languages = None
        return languages

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'location': self.location,
            'profile_picture': self.profile_picture,
            'languages': self.languages
        }


class SpokenLanguages(models.Model):
    Languages = [
        (ENGLISH, ENGLISH),
        (MANDARIN, MANDARIN),
        (HINDI, HINDI),
        (SPANISH, SPANISH),
        (FRENCH, FRENCH),
        (ARABIC, ARABIC),
        (BENGALI, BENGALI),
        (RUSSIAN, RUSSIAN),
        (PORTUGUESE, PORTUGUESE),
        (INDONESIAN, INDONESIAN),
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name="spoken_languages")
    language = models.CharField(max_length=50, choices=Languages, blank=True, null=True)

    def __repr__(self):
        return self.language


class Patients(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name="patients")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255)
    date_of_birth = models.DateField(null=True)

    class Meta:
        unique_together = ('doctor', 'email')
