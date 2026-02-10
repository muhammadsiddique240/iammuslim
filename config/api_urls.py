from rest_framework.routers import DefaultRouter

from azkar.api import AzkarCategoryViewSet, AzkarViewSet
from hadith.api import HadithBookViewSet, HadithChapterViewSet, HadithViewSet
from quran.api import QuranAyahViewSet, QuranSurahViewSet
from research.api import ResearchPaperViewSet

router = DefaultRouter()

router.register(r"quran/surahs", QuranSurahViewSet, basename="quran-surah")
router.register(r"quran/ayahs", QuranAyahViewSet, basename="quran-ayah")
router.register(r"hadith/books", HadithBookViewSet, basename="hadith-book")
router.register(r"hadith/chapters", HadithChapterViewSet, basename="hadith-chapter")
router.register(r"hadith/hadith", HadithViewSet, basename="hadith")
router.register(r"azkar/categories", AzkarCategoryViewSet, basename="azkar-category")
router.register(r"azkar/items", AzkarViewSet, basename="azkar")
router.register(r"research/papers", ResearchPaperViewSet, basename="research-paper")

urlpatterns = router.urls
