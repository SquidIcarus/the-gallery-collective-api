from django.db import models

class EventInterest(models.Model):
    def __str__(self):
        return f'{self.user.username} interested in {self.event.title}'

    user = models.ForeignKey(
        "authentication.User",
        related_name="event_interests",
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        "events.Event",
        related_name="interested_users",
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

