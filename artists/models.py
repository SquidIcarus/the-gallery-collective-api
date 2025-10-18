from django.db import models

class Artist(models.Model):
    def __str__(self):
        return f'{self.user.username}'

    user = models.OneToOneField(
        "authentication.User",
        primary_key=True,
        on_delete=models.CASCADE
    )

    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=300, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
