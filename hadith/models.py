from django.db import models


class HadithBook(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["slug"])]

    def __str__(self) -> str:
        return self.title


class HadithChapter(models.Model):
    book = models.ForeignKey(HadithBook, on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ["book", "number"]
        unique_together = [("book", "slug"), ("book", "number")]
        indexes = [models.Index(fields=["book", "slug"])]

    def __str__(self) -> str:
        return f"{self.book.title} - {self.title}"


class Hadith(models.Model):
    class Grade(models.TextChoices):
        SAHIH = "sahih", "Sahih"
        HASAN = "hasan", "Hasan"
        DAIF = "daif", "Daif"
        UNKNOWN = "unknown", "Unknown"

    chapter = models.ForeignKey(HadithChapter, on_delete=models.CASCADE, related_name="hadiths")
    number_in_chapter = models.PositiveIntegerField()

    text_ar = models.TextField(blank=True)
    text_ur = models.TextField(blank=True)
    text_en = models.TextField(blank=True)

    grade = models.CharField(max_length=16, choices=Grade.choices, default=Grade.UNKNOWN)
    reference = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["chapter", "number_in_chapter"]
        unique_together = [("chapter", "number_in_chapter")]
        indexes = [models.Index(fields=["chapter", "number_in_chapter"]), models.Index(fields=["grade"])]

    def __str__(self) -> str:
        return f"{self.chapter.book.title} - {self.chapter.title} #{self.number_in_chapter}"
