from django.db import models

class Comment(models.Model):
    def __str__(self):
        return f'{self.user.username} on {self.event.title}'

    user = models.ForeignKey(
        "authentication.User",
        related_name="comments",
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        "events.Event",
        related_name="comments",
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    