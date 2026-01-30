"""
AI Servis Entegrasyonu
OpenAI ve Google Gemini API ile özet üretimi ve içerik analizi
"""
import os
from typing import Dict, List, Optional
from django.conf import settings


class AIService:
    """
    AI servisleri için temel sınıf
    """
    
    def __init__(self, provider: str = 'openai'):
        """
        Args:
            provider: 'openai' veya 'gemini'
        """
        self.provider = provider
        self.api_key = self._get_api_key()
    
    def _get_api_key(self) -> str:
        """API anahtarını settings'ten alır"""
        if self.provider == 'openai':
            return getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))
        elif self.provider == 'gemini':
            return getattr(settings, 'GEMINI_API_KEY', os.getenv('GEMINI_API_KEY', ''))
        return ''
    
    def generate_summary(self, text: str, summary_type: str = 'medium') -> Dict[str, any]:
        """
        Metin için özet üretir
        
        Args:
            text: Özetlenecek metin
            summary_type: 'short', 'medium', 'detailed'
        
        Returns:
            Dict: {'summary': str, 'token_count': int, 'error': str}
        """
        if self.provider == 'openai':
            return self._generate_summary_openai(text, summary_type)
        elif self.provider == 'gemini':
            return self._generate_summary_gemini(text, summary_type)
        else:
            return {'error': f'Desteklenmeyen provider: {self.provider}'}
    
    def _generate_summary_openai(self, text: str, summary_type: str) -> Dict:
        """
        OpenAI ile özet üretir
        Gerekli: pip install openai
        """
        try:
            from openai import OpenAI
            
            if not self.api_key:
                return {'error': 'OpenAI API anahtarı bulunamadı'}
            
            client = OpenAI(api_key=self.api_key)
            
            # Özet uzunluğu
            length_instructions = {
                'short': 'Çok kısa bir özet (2-3 cümle)',
                'medium': 'Orta uzunlukta bir özet (1 paragraf)',
                'detailed': 'Detaylı bir özet (2-3 paragraf)',
            }
            
            prompt = f"""
Aşağıdaki metni Türkçe olarak özetle.
{length_instructions.get(summary_type, 'Orta uzunlukta bir özet')} yap.

Metin:
{text[:8000]}  # Token limitine dikkat et
"""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # veya "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "Sen profesyonel bir kitap özeti yazarısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000 if summary_type == 'detailed' else 500,
            )
            
            summary = response.choices[0].message.content
            token_count = response.usage.total_tokens
            
            return {
                'summary': summary,
                'token_count': token_count,
                'error': None
            }
        
        except ImportError:
            return {'error': 'openai paketi yüklü değil. pip install openai'}
        except Exception as e:
            return {'error': f'OpenAI hatası: {str(e)}'}
    
    def _generate_summary_gemini(self, text: str, summary_type: str) -> Dict:
        """
        Google Gemini ile özet üretir
        Gerekli: pip install google-generativeai
        """
        try:
            import google.generativeai as genai
            
            if not self.api_key:
                return {'error': 'Gemini API anahtarı bulunamadı'}
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Özet uzunluğu
            length_instructions = {
                'short': 'Çok kısa bir özet (2-3 cümle)',
                'medium': 'Orta uzunlukta bir özet (1 paragraf)',
                'detailed': 'Detaylı bir özet (2-3 paragraf)',
            }
            
            prompt = f"""
Aşağıdaki metni Türkçe olarak özetle.
{length_instructions.get(summary_type, 'Orta uzunlukta bir özet')} yap.

Metin:
{text[:30000]}
"""
            
            response = model.generate_content(prompt)
            summary = response.text
            
            return {
                'summary': summary,
                'token_count': 0,  # Gemini token bilgisi farklı
                'error': None
            }
        
        except ImportError:
            return {'error': 'google-generativeai paketi yüklü değil. pip install google-generativeai'}
        except Exception as e:
            return {'error': f'Gemini hatası: {str(e)}'}
    
    def generate_chapter_summary(self, chapter_title: str, chapter_content: str) -> Dict:
        """Bölüm özeti üretir"""
        prompt_text = f"Bölüm Başlığı: {chapter_title}\n\nİçerik:\n{chapter_content}"
        return self.generate_summary(prompt_text, 'short')
    
    def extract_keywords(self, text: str, count: int = 10) -> List[str]:
        """
        Metinden anahtar kelimeler çıkarır
        """
        try:
            from openai import OpenAI
            
            if not self.api_key or self.provider != 'openai':
                return []
            
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""
Aşağıdaki metinden en önemli {count} anahtar kelimeyi Türkçe olarak çıkar.
Sadece kelimeleri virgülle ayırarak ver, başka bir şey yazma.

Metin:
{text[:4000]}
"""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200,
            )
            
            keywords_text = response.choices[0].message.content
            keywords = [k.strip() for k in keywords_text.split(',')]
            return keywords[:count]
        
        except Exception as e:
            print(f"Anahtar kelime çıkarma hatası: {e}")
            return []


# Yardımcı fonksiyonlar
def generate_book_summary(book_text: str, provider: str = 'openai') -> Dict:
    """
    Kitap metni için kısa, orta ve detaylı özetler üretir
    """
    ai_service = AIService(provider=provider)
    
    summaries = {}
    for summary_type in ['short', 'medium', 'detailed']:
        result = ai_service.generate_summary(book_text, summary_type)
        summaries[summary_type] = result
    
    return summaries


def generate_all_chapter_summaries(chapters: List[Dict], provider: str = 'openai') -> List[Dict]:
    """
    Tüm bölümler için özet üretir
    """
    ai_service = AIService(provider=provider)
    
    chapter_summaries = []
    for chapter in chapters:
        result = ai_service.generate_chapter_summary(
            chapter['title'],
            chapter['content']
        )
        chapter_summaries.append({
            'chapter_title': chapter['title'],
            'chapter_order': chapter['order'],
            'summary': result.get('summary', ''),
            'error': result.get('error'),
        })
    
    return chapter_summaries
