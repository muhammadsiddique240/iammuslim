import os
import tempfile
import re
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class PDFProcessor:
    """Utility class for processing PDF files and converting them to images and extracting text."""
    
    def __init__(self):
        self.pdf2image_available = PDF2IMAGE_AVAILABLE
        self.pil_available = PIL_AVAILABLE
        self.pypdf2_available = PYPDF2_AVAILABLE
        self.pdfplumber_available = PDFPLUMBER_AVAILABLE
        
    def can_process_pdfs(self) -> bool:
        """Check if PDF processing dependencies are available."""
        return self.pil_available and (self.pdf2image_available or self.pypdf2_available or self.pdfplumber_available)
    
    def extract_text_from_pdf(self, pdf_path: str, max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        Extract text from PDF pages, with special handling for Arabic/Quranic content.
        
        Args:
            pdf_path: Path to the PDF file
            max_pages: Maximum number of pages to extract
            
        Returns:
            List of dictionaries with page number and extracted text
        """
        if not os.path.exists(pdf_path):
            return []
        
        extracted_pages = []
        
        # Try pdfplumber first (best for text extraction)
        if self.pdfplumber_available:
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for i, page in enumerate(pdf.pages[:max_pages]):
                        text = page.extract_text()
                        if text and text.strip():
                            # Clean and format the text
                            cleaned_text = self._clean_arabic_text(text)
                            extracted_pages.append({
                                'page_number': i + 1,
                                'text': cleaned_text,
                                'is_arabic': self._is_arabic_text(cleaned_text)
                            })
                return extracted_pages
            except Exception as e:
                print(f"pdfplumber extraction failed: {e}")
        
        # Fallback to PyPDF2
        if self.pypdf2_available:
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for i, page in enumerate(pdf_reader.pages[:max_pages]):
                        text = page.extract_text()
                        if text and text.strip():
                            # Clean and format the text
                            cleaned_text = self._clean_arabic_text(text)
                            extracted_pages.append({
                                'page_number': i + 1,
                                'text': cleaned_text,
                                'is_arabic': self._is_arabic_text(cleaned_text)
                            })
                return extracted_pages
            except Exception as e:
                print(f"PyPDF2 extraction failed: {e}")
        
        return []
    
    def _clean_arabic_text(self, text: str) -> str:
        """Clean and format Arabic text for proper display."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common Arabic text issues
        text = text.replace('؟', '؟')  # Ensure proper question mark
        text = text.replace('،', '،')  # Ensure proper comma
        
        # Try to identify and format Quranic verses (Ayah patterns)
        # Look for patterns like "1:1" or "١:١" or verse numbers
        ayah_pattern = r'(\d+:\d+|[٠-٩]+:[٠-٩]+)'
        if re.search(ayah_pattern, text):
            # This might be Quranic content, format it nicely
            lines = text.split('\n')
            formatted_lines = []
            for line in lines:
                line = line.strip()
                if line:
                    # Check if line starts with verse number
                    if re.match(r'^(\d+:\d+|[٠-٩]+:[٠-٩]+)', line):
                        formatted_lines.append(f"﴿{line}﴾")
                    else:
                        formatted_lines.append(line)
            text = '\n'.join(formatted_lines)
        
        return text
    
    def _is_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters."""
        if not text:
            return False
        
        # Arabic Unicode range
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        return bool(arabic_pattern.search(text))
    
    def format_quranic_text(self, text: str, page_number: int = 1) -> Dict[str, Any]:
        """
        Format extracted text specifically for Quranic display.
        
        Args:
            text: Extracted text from PDF
            page_number: Page number for reference
            
        Returns:
            Dictionary with formatted text and metadata
        """
        if not text:
            return {
                'formatted_text': '',
                'is_quranic': False,
                'verses': [],
                'page_info': f'Page {page_number}'
            }
        
        is_arabic = self._is_arabic_text(text)
        verses = []
        formatted_text = text
        
        if is_arabic:
            # Try to extract verses from Arabic text
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                if line and len(line) > 5:  # Ignore very short lines
                    # Check if this looks like a verse
                    if self._looks_like_verse(line):
                        verses.append({
                            'number': i + 1,
                            'text_ar': line,
                            'translation': ''  # Could be added later
                        })
        
        # Determine if this looks like Quranic content
        is_quranic = is_arabic and len(verses) > 0
        
        return {
            'formatted_text': formatted_text,
            'is_quranic': is_quranic,
            'is_arabic': is_arabic,
            'verses': verses,
            'page_info': f'Page {page_number}',
            'verse_count': len(verses)
        }
    
    def _looks_like_verse(self, text: str) -> bool:
        """Check if text looks like a Quranic verse."""
        # Quranic verses typically have certain characteristics
        if len(text) < 10:
            return False
        
        # Contains Arabic characters
        if not self._is_arabic_text(text):
            return False
        
        # Contains common Quranic phrases or patterns
        quranic_indicators = [
            'بسم الله', 'الرحمن', 'الرحيم', 'الحمد لله',
            'سبحان', 'قال', 'رب', 'علم', 'خلق', 'جنة', 'نار'
        ]
        
        for indicator in quranic_indicators:
            if indicator in text:
                return True
        
        # If it contains Arabic and is reasonably long, likely a verse
        return len(text) > 20
    
    def pdf_to_images(self, pdf_path: str, max_pages: int = 5, dpi: int = 150) -> List[str]:
        """
        Convert PDF pages to images and return the image URLs.
        
        Args:
            pdf_path: Path to the PDF file
            max_pages: Maximum number of pages to convert
            dpi: Resolution for the converted images
            
        Returns:
            List of image URLs that can be used in templates
        """
        if not self.can_process_pdfs():
            return []
            
        try:
            # Convert PDF to list of images
            images = convert_from_path(pdf_path, dpi=dpi)
            
            # Limit the number of pages
            images = images[:max_pages]
            
            image_urls = []
            
            for i, image in enumerate(images):
                # Save each image as JPEG
                image_filename = f"pdf_page_{i+1}.jpg"
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    image.save(temp_file.name, 'JPEG', quality=85)
                    
                    # Read the file and save to Django storage
                    with open(temp_file.name, 'rb') as f:
                        image_content = f.read()
                    
                    # Save to media storage
                    storage_path = f"research/previews/{image_filename}"
                    if default_storage.exists(storage_path):
                        default_storage.delete(storage_path)
                    
                    saved_path = default_storage.save(storage_path, ContentFile(image_content))
                    image_url = default_storage.url(saved_path)
                    image_urls.append(image_url)
                    
                    # Clean up temporary file
                    os.unlink(temp_file.name)
            
            return image_urls
            
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            return []
    
    def get_pdf_thumbnail(self, pdf_path: str, size: tuple = (300, 400)) -> Optional[str]:
        """
        Generate a thumbnail from the first page of a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            size: Thumbnail size as (width, height)
            
        Returns:
            URL of the thumbnail image or None if failed
        """
        if not self.can_process_pdfs():
            return None
            
        try:
            # Convert first page to image
            images = convert_from_path(pdf_path, dpi=150)
            if not images:
                return None
                
            image = images[0]
            
            # Create thumbnail
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Save thumbnail
            thumbnail_filename = "pdf_thumbnail.jpg"
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                image.save(temp_file.name, 'JPEG', quality=85)
                
                # Read the file and save to Django storage
                with open(temp_file.name, 'rb') as f:
                    thumbnail_content = f.read()
                
                # Save to media storage
                storage_path = f"research/thumbnails/{thumbnail_filename}"
                if default_storage.exists(storage_path):
                    default_storage.delete(storage_path)
                
                saved_path = default_storage.save(storage_path, ContentFile(thumbnail_content))
                thumbnail_url = default_storage.url(saved_path)
                
                # Clean up temporary file
                os.unlink(temp_file.name)
                
                return thumbnail_url
                
        except Exception as e:
            print(f"Error generating PDF thumbnail: {e}")
            return None


# Global PDF processor instance
pdf_processor = PDFProcessor()


def get_pdf_preview_images(pdf_field, max_pages: int = 5) -> List[str]:
    """
    Get preview images for a PDF file field.
    
    Args:
        pdf_field: Django FileField containing the PDF
        max_pages: Maximum number of pages to convert
        
    Returns:
        List of image URLs
    """
    if not pdf_field or not pdf_field.name:
        return []
        
    # Get the full path to the PDF file
    pdf_path = pdf_field.path
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        return []
    
    return pdf_processor.pdf_to_images(pdf_path, max_pages=max_pages)


def get_pdf_thumbnail_url(pdf_field, size: tuple = (300, 400)) -> Optional[str]:
    """
    Get thumbnail URL for a PDF file field.
    
    Args:
        pdf_field: Django FileField containing the PDF
        size: Thumbnail size as (width, height)
        
    Returns:
        Thumbnail URL or None
    """
    if not pdf_field or not pdf_field.name:
        return None
        
    # Get the full path to the PDF file
    pdf_path = pdf_field.path
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        return None
    
    return pdf_processor.get_pdf_thumbnail(pdf_path, size=size)


def extract_pdf_text_content(pdf_field, max_pages: int = 10) -> List[Dict[str, Any]]:
    """
    Extract text content from a PDF file field.
    
    Args:
        pdf_field: Django FileField containing the PDF
        max_pages: Maximum number of pages to extract
        
    Returns:
        List of dictionaries with extracted text content
    """
    if not pdf_field or not pdf_field.name:
        return []
        
    # Get the full path to the PDF file
    pdf_path = pdf_field.path
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        return []
    
    return pdf_processor.extract_text_from_pdf(pdf_path, max_pages=max_pages)


def format_pdf_for_quranic_display(pdf_field, max_pages: int = 5) -> List[Dict[str, Any]]:
    """
    Extract and format PDF content specifically for Quranic display.
    
    Args:
        pdf_field: Django FileField containing the PDF
        max_pages: Maximum number of pages to process
        
    Returns:
        List of formatted pages ready for Quranic display
    """
    extracted_pages = extract_pdf_text_content(pdf_field, max_pages)
    formatted_pages = []
    
    for page in extracted_pages:
        formatted = pdf_processor.format_quranic_text(
            page['text'], 
            page['page_number']
        )
        formatted_pages.append(formatted)
    
    return formatted_pages
