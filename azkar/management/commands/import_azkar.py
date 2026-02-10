import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from azkar.models import Azkar, AzkarCategory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, help="Path to Azkar JSON file")

    def handle(self, *args, **options):
        path = Path(options["path"]).expanduser()
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        categories = data.get("categories") if isinstance(data, dict) else data
        if not isinstance(categories, list):
            raise CommandError("Invalid JSON: expected a list or a dict with key 'categories'")

        created_categories = 0
        created_items = 0

        with transaction.atomic():
            for c in categories:
                if not isinstance(c, dict):
                    continue

                title = (c.get("title") or "").strip()
                if not title:
                    continue

                slug = c.get("slug") or title.lower().replace(" ", "-")
                category, category_created = AzkarCategory.objects.update_or_create(
                    slug=slug,
                    defaults={"title": title},
                )
                if category_created:
                    created_categories += 1

                items = c.get("items", [])
                if not isinstance(items, list):
                    items = []

                for z in items:
                    if not isinstance(z, dict):
                        continue

                    item_title = (z.get("title") or "").strip()
                    if not item_title:
                        continue

                    item_slug = z.get("slug") or item_title.lower().replace(" ", "-")[:60]
                    defaults = {
                        "title": item_title,
                        "arabic": z.get("arabic", ""),
                        "urdu": z.get("urdu", ""),
                        "reference": z.get("reference", ""),
                        "time_of_day": z.get("time_of_day", Azkar.TimeOfDay.ANY),
                        "order": int(z.get("order") or 0),
                    }

                    _, created = Azkar.objects.update_or_create(
                        category=category,
                        slug=item_slug,
                        defaults=defaults,
                    )
                    if created:
                        created_items += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported Azkar. New categories: {created_categories}, new items: {created_items}"
            )
        )
