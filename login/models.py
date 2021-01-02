from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

# unique id code


def random_code(digit=5, letter=2):
    sample_str = ''.join((random.choice(string.ascii_uppercase) for i in range(letter)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digit)))

    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string


# Create your models here.
class User(AbstractUser):
    unique_id = models.CharField(default=random_code, max_length=7)
    STAFF_POSITION = [
        ('admin', 'admin'),
        ('front_office', 'front_office'),
        ('restaurant', 'restaurant')
    ]
    staff_position = models.CharField(choices=STAFF_POSITION, max_length=20, default=False)


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateField(help_text='State when you joined the hotel workforce')
    middle_name = models.CharField(max_length=25, help_text='Enter your middle name here if any')
    birthday = models.DateField()
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(choices=GENDER, max_length=10)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if (instance.staff_position == 'admin') or (instance.staff_position == 'front_office') or (instance.staff_position == 'restaurant'):
            StaffProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.staff_position == 'admin' or instance.staff_position == 'front_office' or instance.staff_position == 'restaurant':
        instance.staffprofile.save()
'''


