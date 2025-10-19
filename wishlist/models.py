from django.db import models

class Wishlist(models.Model):
    def __str__(self):
        return f'{self.user.username} wishlisted {self.artwork.title}'

    user = models.ForeignKey(
        "authentication.User",
        related_name="wishlists",
        on_delete=models.CASCADE
    )
    artwork = models.ForeignKey(
        "artworks.Artwork",
        related_name="wishlisted_by",
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artwork')