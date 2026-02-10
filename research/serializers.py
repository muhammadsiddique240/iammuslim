from rest_framework import serializers

from .models import ResearchPaper


class ResearchPaperSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = ResearchPaper
        fields = (
            "id",
            "title",
            "slug",
            "author",
            "summary",
            "references",
            "published_at",
            "pdf_url",
        )

    def get_pdf_url(self, obj: ResearchPaper) -> str | None:
        request = self.context.get("request")
        if not obj.pdf:
            return None
        url = obj.pdf.url
        return request.build_absolute_uri(url) if request else url
