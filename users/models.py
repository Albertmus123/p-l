from django.db import models
from django.contrib.auth.models import  AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =[ "username"]

    def __str__(self):
        return self.email
    
    
    
class OTP(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"{self.user.username}"