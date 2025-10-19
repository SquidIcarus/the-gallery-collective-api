from django.db import models

class Artwork(models.Model):
    def __str__(self):
        return f'{self.title} by {self.artist.user.username}'

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='artworks/')
    dimensions = models.CharField(max_length=100, blank=True)
    year_created = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(
        "artists.Artist",
        related_name="artworks",
        on_delete=models.CASCADE
    )
