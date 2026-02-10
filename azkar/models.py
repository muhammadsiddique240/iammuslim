from django.db import models


class AzkarCategory(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["slug"])]

    def __str__(self) -> str:
        return self.title


class Azkar(models.Model):
    class TimeOfDay(models.TextChoices):
        MORNING = "morning", "Morning"
        EVENING = "evening", "Evening"
        ANY = "any", "Any"

    category = models.ForeignKey(AzkarCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="items")
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    arabic = models.TextField(blank=True)
    urdu = models.TextField(blank=True)
    reference = models.CharField(max_length=255, blank=True)

    time_of_day = models.CharField(max_length=16, choices=TimeOfDay.choices, default=TimeOfDay.ANY)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["time_of_day", "order", "title"]
        unique_together = [("category", "slug")]
        indexes = [models.Index(fields=["time_of_day"])]

    def __str__(self) -> str:
        return self.title
