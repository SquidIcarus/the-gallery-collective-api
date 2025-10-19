from django.db import models

class Event(models.Model):
    def __str__(self):
        return f'{self.title} by {self.artist.user.username}'

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(
        "artists.Artist",
        related_name="events",
        on_delete=models.CASCADE
    )

