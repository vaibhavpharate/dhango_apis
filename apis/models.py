from django.db import models

from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class Plans(models.Model):
    is_active = models.BooleanField(default=True)
    plan_type = models.CharField(max_length=20,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_default_name(cls):
        plan, created = cls.objects.get_or_create(
            plan_type='Basic', 
           
        )
        return plan.plan_type

    def __str__(self) -> str:
        return self.plan_type

# Create your models here.
class Clients(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"

    username = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=200,unique=True)
    client_short = models.CharField(max_length=10)
    role_type = models.CharField(max_length=10,choices=Roles.choices,default=Roles.CLIENT)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    
    date_updated = models.DateTimeField(auto_now=True)
    logos = models.ImageField(upload_to='client_logos/',default="None")
    
    plans = models.ForeignKey(Plans,on_delete=models.CASCADE,default=Plans.get_default_name,to_field='plan_type',related_name='client_plans')

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'clients'

    def __str__(self) -> str:
        return f"{self.username}"



class ClientPlans(models.Model):
    client_id = models.ForeignKey(Clients,on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plans,on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



class SiteConfig(models.Model):
    class Verification(models.TextChoices):
        VERIFIED = "VERIFIED", "VERIFIED".title()
        UNVERIFIED = "UNVERIFIED", "UNVERIFIED".title()
    class SiteType(models.TextChoices):
        SOLAR = 'Solar','Solar'
        WIND = 'Wind','Wind'
    
    site_name = models.CharField(max_length=20)
    state = models.CharField(max_length=40)
    capacity = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=12,choices=SiteType.choices,default=SiteType.SOLAR)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)

    # row_id = models.AutoField(name='row_identity',) 
    
    log_ts = models.DateTimeField(auto_now_add=True)
    # client_name = models.TextField(choices=Clients.username)
    client_name = models.ForeignKey(Clients,on_delete=models.CASCADE,to_field='username',related_name='client_name')
    site_status = models.CharField(choices=(("ACTIVE","Active"),("INACTIVE","Inactive")),default='Active')
    verified = models.CharField(choices=Verification.choices,default=Verification.UNVERIFIED)

    class Meta:
        db_table = 'site_config'
    
    def __str__(self) -> str:
        return self.site_name

