from django.db import models

# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.firstname

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
