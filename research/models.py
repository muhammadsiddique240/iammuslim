from django.db import models
from .utils import get_pdf_preview_images, get_pdf_thumbnail_url, format_pdf_for_quranic_display


class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=128, default="Engineer Muhammad Ali Mirza")

    summary = models.TextField(blank=True)
    references = models.TextField(blank=True)

    pdf = models.FileField(upload_to="research/papers/", blank=True)
    published_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "title"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["author"]) ]

    def __str__(self) -> str:
        return self.title
    
    @property
    def has_pdf(self) -> bool:
        """Check if the research paper has a PDF file."""
        return bool(self.pdf and self.pdf.name)
    
    @property
    def pdf_preview_images(self) -> list:
        """Get preview images for the PDF."""
        if not self.has_pdf:
            return []
        return get_pdf_preview_images(self.pdf, max_pages=3)
    
    @property
    def pdf_thumbnail_url(self) -> str:
        """Get thumbnail URL for the PDF."""
        if not self.has_pdf:
            return ""
        return get_pdf_thumbnail_url(self.pdf, size=(300, 400)) or ""
    
    @property
    def pdf_url(self) -> str:
        """Get the URL of the PDF file."""
        if not self.has_pdf:
            return ""
        return self.pdf.url
    
    @property
    def pdf_text_content(self) -> list:
        """Get extracted text content from PDF."""
        if not self.has_pdf:
            return []
        return format_pdf_for_quranic_display(self.pdf, max_pages=10)
    
    @property
    def has_quranic_content(self) -> bool:
        """Check if PDF contains Quranic/Arabic content."""
        if not self.has_pdf:
            return False
        text_content = self.pdf_text_content
        return any(page.get('is_quranic', False) or page.get('is_arabic', False) for page in text_content)
    
    @property
    def total_verses(self) -> int:
        """Get total number of verses found in PDF."""
        if not self.has_pdf:
            return 0
        text_content = self.pdf_text_content
        return sum(page.get('verse_count', 0) for page in text_content)
