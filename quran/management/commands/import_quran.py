import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from quran.models import QuranAyah, QuranSurah


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--path", required=True, help="Path to Quran JSON file")

    def handle(self, *args, **options):
        path = Path(options["path"]).expanduser()
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))
        surahs = data.get("surahs") if isinstance(data, dict) else data
        if not isinstance(surahs, list):
            raise CommandError("Invalid JSON: expected a list or a dict with key 'surahs'")

        created_surahs = 0
        created_ayahs = 0

        with transaction.atomic():
            for s in surahs:
                if not isinstance(s, dict):
                    continue

                number = int(s.get("number"))
                defaults = {
                    "name_ar": s.get("name_ar", ""),
                    "name_en": s.get("name_en", ""),
                    "name_ur": s.get("name_ur", ""),
                    "slug": s.get("slug") or str(number),
                }
                surah, surah_created = QuranSurah.objects.update_or_create(number=number, defaults=defaults)
                if surah_created:
                    created_surahs += 1

                ayahs = s.get("ayahs", [])
                if not isinstance(ayahs, list):
                    ayahs = []

                for a in ayahs:
                    if not isinstance(a, dict):
                        continue
                    number_in_surah = int(a.get("number_in_surah"))
                    ayah_defaults = {
                        "text_ar": a.get("text_ar", ""),
                        "translation_ur": a.get("translation_ur", ""),
                        "translation_en": a.get("translation_en", ""),
                    }
                    _, ayah_created = QuranAyah.objects.update_or_create(
                        surah=surah,
                        number_in_surah=number_in_surah,
                        defaults=ayah_defaults,
                    )
                    if ayah_created:
                        created_ayahs += 1

                surah.ayah_count = surah.ayahs.count()
                surah.save(update_fields=["ayah_count"])

        self.stdout.write(self.style.SUCCESS(f"Imported Quran. New surahs: {created_surahs}, new ayahs: {created_ayahs}"))
