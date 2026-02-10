import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from research.models import ResearchPaper


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, help="Path to Research JSON file")

    def handle(self, *args, **options):
        path = Path(options["path"]).expanduser()
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        papers = data.get("papers") if isinstance(data, dict) else data
        if not isinstance(papers, list):
            raise CommandError("Invalid JSON: expected a list or a dict with key 'papers'")

        created = 0

        with transaction.atomic():
            for p in papers:
                if not isinstance(p, dict):
                    continue

                title = (p.get("title") or "").strip()
                if not title:
                    continue

                slug = p.get("slug") or title.lower().replace(" ", "-")[:80]
                defaults = {
                    "author": p.get("author", "Engineer Muhammad Ali Mirza"),
                    "summary": p.get("summary", ""),
                    "references": p.get("references", ""),
                    "published_at": p.get("published_at") or None,
                }

                _, was_created = ResearchPaper.objects.update_or_create(slug=slug, defaults={"title": title, **defaults})
                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Imported Research. New papers: {created}"))
