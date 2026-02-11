// Islamic UI Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    // Scroll animations - temporarily disabled to prevent vibration
    /*
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe elements for animations
    document.querySelectorAll('.fade-in-up, .slide-in-left, .slide-in-right').forEach(el => {
        observer.observe(el);
    });
    */

    // Quranic Verses Slider
    initVersesSlider();
    
    // Scholar Videos Section
    initScholarVideos();
    
    // Parallax effect for background
    initParallaxEffect();
});

// Quranic Verses Slider
function initVersesSlider() {
    const verses = [
        {
            arabic: "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
            translation: "In the name of Allah, the Most Gracious, the Most Merciful",
            reference: "Al-Fatihah 1:1"
        },
        {
            arabic: "الرَّحْمَنُ الرَّحِيمُ",
            translation: "The Most Gracious, the Most Merciful",
            reference: "Al-Fatihah 1:2"
        },
        {
            arabic: "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
            translation: "All praise is due to Allah, Lord of the worlds",
            reference: "Al-Fatihah 1:3"
        },
        {
            arabic: "الرَّحْمَنُ الرَّحِيمُ",
            translation: "The Most Gracious, the Most Merciful",
            reference: "Al-Fatihah 1:4"
        },
        {
            arabic: "مَالِكِ يَوْمِ الدِّينِ",
            translation: "Sovereign of the Day of Recompense",
            reference: "Al-Fatihah 1:5"
        },
        {
            arabic: "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
            translation: "It is You we worship and You we ask for help",
            reference: "Al-Fatihah 1:6"
        },
        {
            arabic: "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
            translation: "Guide us to the straight path",
            reference: "Al-Fatihah 1:7"
        }
    ];

    let currentVerse = 0;
    const sliderContainer = document.getElementById('verses-slider');
    
    if (sliderContainer) {
        // Create verse slides
        verses.forEach((verse, index) => {
            const slide = document.createElement('div');
            slide.className = 'verse-slide fade-in-up';
            slide.innerHTML = `
                <div class="verse-arabic">${verse.arabic}</div>
                <div class="verse-translation">${verse.translation}</div>
                <div class="verse-reference">${verse.reference}</div>
            `;
            sliderContainer.appendChild(slide);
        });

        // Auto-rotate verses
        setInterval(() => {
            currentVerse = (currentVerse + 1) % verses.length;
            updateSlider();
        }, 5000);

        updateSlider();
    }

    function updateSlider() {
        const slides = sliderContainer.querySelectorAll('.verse-slide');
        slides.forEach((slide, index) => {
            slide.style.display = index === currentVerse ? 'block' : 'none';
            if (index === currentVerse) {
                slide.classList.add('visible');
            }
        });
    }
}

// Scholar Videos Section
function initScholarVideos() {
    const scholars = [
        {
            name: "Engineer Ali Mirza",
            title: "Islamic Scholar & Engineer",
            videoUrl: "https://www.youtube.com/embed/qMXHTr3qe2E",
            image: "https://img.youtube.com/vi/qMXHTr3qe2E/hqdefault.jpg"
        },
        {
            name: "Maulana Tariq Jameel",
            title: "Islamic Scholar & Speaker",
            videoUrl: "https://www.youtube.com/embed/1fVp3rK8pLk",
            image: "https://img.youtube.com/vi/1fVp3rK8pLk/hqdefault.jpg"
        },
        {
            name: "Javed Ahmad Ghamdi",
            title: "Islamic Scholar & Thinker",
            videoUrl: "https://www.youtube.com/embed/9kCg_8mz8wY",
            image: "https://img.youtube.com/vi/9kCg_8mz8wY/hqdefault.jpg"
        },
        {
            name: "Dr. Israr Ahmed",
            title: "Islamic Scholar & Philosopher",
            videoUrl: "https://www.youtube.com/embed/7Cq7XtSjw9Y",
            image: "https://img.youtube.com/vi/7Cq7XtSjw9Y/hqdefault.jpg"
        }
    ];

    const scholarsContainer = document.getElementById('scholars-container');
    
    if (scholarsContainer) {
        scholars.forEach((scholar, index) => {
            const card = document.createElement('div');
            card.className = `scholar-card slide-in-up ${index % 2 === 0 ? 'slide-in-left' : 'slide-in-right'}`;
            card.innerHTML = `
                <div class="relative">
                    <img src="${scholar.image}" alt="${scholar.name}" class="scholar-video">
                    <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300">
                        <button class="bg-white text-gray-900 rounded-full p-3 hover:bg-gray-100 transition-colors" onclick="playVideo('${scholar.videoUrl}')">
                            <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="scholar-info">
                    <h3 class="scholar-name">${scholar.name}</h3>
                    <p class="scholar-title">${scholar.title}</p>
                    <button class="bg-gradient-to-r from-islamic-green to-islamic-blue text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity" onclick="playVideo('${scholar.videoUrl}')">
                        Watch Videos
                    </button>
                </div>
            `;
            scholarsContainer.appendChild(card);
        });
    }
}

// Play video function
function playVideo(videoUrl) {
    // Create modal for video playback
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <div class="flex justify-between items-center p-4 border-b">
                <h3 class="text-lg font-semibold">Islamic Lecture</h3>
                <button onclick="closeVideoModal()" class="text-gray-500 hover:text-gray-700">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
            <div class="aspect-video">
                <iframe src="${videoUrl}" class="w-full h-full" frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
    `;
    modal.onclick = function(e) {
        if (e.target === modal) {
            closeVideoModal();
        }
    };
    document.body.appendChild(modal);
}

// Close video modal
function closeVideoModal() {
    const modal = document.querySelector('.fixed.inset-0');
    if (modal) {
        modal.remove();
    }
}

// Parallax effect for background
function initParallaxEffect() {
    const islamicBg = document.querySelector('.islamic-bg');
    if (islamicBg) {
        // Temporarily disabled parallax effect
        /*
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            islamicBg.style.transform = `translateY(${parallax}px)`;
        });
        */
    }
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states for dynamic content
function showLoading(element) {
    element.innerHTML = '<div class="loading-spinner mx-auto"></div>';
}

function hideLoading(element, content) {
    element.innerHTML = content;
}
