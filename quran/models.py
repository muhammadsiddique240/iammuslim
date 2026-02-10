from django.db import models


class QuranSurah(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    name_ar = models.CharField(max_length=64)
    name_en = models.CharField(max_length=64, blank=True)
    name_ur = models.CharField(max_length=64, blank=True)
    slug = models.SlugField(unique=True)
    ayah_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["number"]
        indexes = [models.Index(fields=["number"]), models.Index(fields=["slug"])]

    def __str__(self) -> str:
        return f"{self.number}. {self.name_ar}"


class QuranAyah(models.Model):
    surah = models.ForeignKey(QuranSurah, on_delete=models.CASCADE, related_name="ayahs")
    number_in_surah = models.PositiveSmallIntegerField()
    text_ar = models.TextField()
    translation_ur = models.TextField(blank=True)
    translation_en = models.TextField(blank=True)

    class Meta:
        ordering = ["surah__number", "number_in_surah"]
        unique_together = [("surah", "number_in_surah")]
        indexes = [
            models.Index(fields=["surah", "number_in_surah"]),
        ]

    def __str__(self) -> str:
        return f"{self.surah.number}:{self.number_in_surah}"
