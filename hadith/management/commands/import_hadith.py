import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from hadith.models import Hadith, HadithBook, HadithChapter


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, help="Path to Hadith JSON file")

    def handle(self, *args, **options):
        path = Path(options["path"]).expanduser()
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        books = data.get("books") if isinstance(data, dict) else data
        if not isinstance(books, list):
            raise CommandError("Invalid JSON: expected a list or a dict with key 'books'")

        created_books = 0
        created_chapters = 0
        created_hadith = 0

        with transaction.atomic():
            for b in books:
                if not isinstance(b, dict):
                    continue
                title = (b.get("title") or "").strip()
                if not title:
                    continue

                book_defaults = {"slug": b.get("slug") or title.lower().replace(" ", "-")}
                book, book_created = HadithBook.objects.update_or_create(title=title, defaults=book_defaults)
                if book_created:
                    created_books += 1

                chapters = b.get("chapters", [])
                if not isinstance(chapters, list):
                    chapters = []

                for c in chapters:
                    if not isinstance(c, dict):
                        continue

                    chapter_number = int(c.get("number") or 0)
                    chapter_title = (c.get("title") or "").strip()
                    if not chapter_title:
                        continue

                    chapter_slug = c.get("slug") or f"{chapter_number}-{chapter_title.lower().replace(' ', '-')[:50]}"
                    chapter_defaults = {"title": chapter_title, "slug": chapter_slug}
                    chapter, chapter_created = HadithChapter.objects.update_or_create(
                        book=book,
                        number=chapter_number,
                        defaults=chapter_defaults,
                    )
                    if chapter_created:
                        created_chapters += 1

                    hadith_items = c.get("hadith", [])
                    if not isinstance(hadith_items, list):
                        hadith_items = []

                    for h in hadith_items:
                        if not isinstance(h, dict):
                            continue

                        num = int(h.get("number_in_chapter") or 0)
                        if num <= 0:
                            continue

                        defaults = {
                            "text_ar": h.get("text_ar", ""),
                            "text_ur": h.get("text_ur", ""),
                            "text_en": h.get("text_en", ""),
                            "grade": h.get("grade", Hadith.Grade.UNKNOWN),
                            "reference": h.get("reference", ""),
                        }

                        _, hadith_created = Hadith.objects.update_or_create(
                            chapter=chapter,
                            number_in_chapter=num,
                            defaults=defaults,
                        )
                        if hadith_created:
                            created_hadith += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported Hadith. New books: {created_books}, new chapters: {created_chapters}, new hadith: {created_hadith}"
            )
        )
