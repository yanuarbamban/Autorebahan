import json
import random
import re
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.corpus import wordnet as wn

class ArticleSpinner:
    from langdetect import detect

class ArticleSpinner:
    def __init__(self):
        with open('data/thesaurus.json', 'r', encoding='utf-8') as f:
            self.thesaurus = json.load(f)
        
        self.sentence_structures = {
            'id': [
                (lambda p1, p2: f"{p1}. Namun, {p2}", 0.6),
                (lambda p1, p2: f"Selain itu, {p1}. {p2}", 0.5)
            ],
            'en': [
                (lambda p1, p2: f"{p1}. However, {p2}", 0.7),
                (lambda p1, p2: f"Moreover, {p1}. {p2}", 0.6)
            ]
        }

    def detect_language(self, text):
        try:
            lang = detect(text)
            return 'en' if lang == 'en' else 'id'
        except:
            return 'id'

    def spin_text(self, text, spin_level=0.85):
        lang = self.detect_language(text)
        sentences = sent_tokenize(text)
        spun_sentences = []
        
        for sentence in sentences:
            # Proses spinning
            words = word_tokenize(sentence)
            tagged = pos_tag(words)
            spun_words = []
            
            for word, tag in tagged:
                if word.isupper() or tag == 'NNP':
                    spun_words.append(word)
                    continue
                
                if random.random() < spin_level:
                    synonyms = self.get_synonyms(word, tag, lang)
                    if synonyms:
                        spun_words.append(random.choice(synonyms))
                        continue
                
                spun_words.append(word)
            
            # Gabung dengan template sesuai bahasa
            if len(spun_words) > 3 and random.random() < 0.6:
                template, prob = random.choice(self.sentence_structures[lang])
                if random.random() < prob:
                    split_point = random.randint(1, len(spun_words)-1)
                    part1 = ' '.join(spun_words[:split_point])
                    part2 = ' '.join(spun_words[split_point:])
                    spun_sentence = template(part1, part2)
                    spun_sentences.append(spun_sentence)
                    continue
            
            spun_sentences.append(' '.join(spun_words))
        
        return ' '.join(spun_sentences)

    def get_synonyms(self, word, tag, lang):
        pos_map = {
            'NN': 'noun',
            'VB': 'verb',
            'JJ': 'adj',
            'RB': 'adv'
        }
        pos = pos_map.get(tag[:2], 'default')
        
        entry = self.thesaurus.get(lang, {}).get(word.lower(), {})
        if isinstance(entry, dict):
            return entry.get(pos, entry.get('default', []))
        return entry if isinstance(entry, list) else []
    def __init__(self):
        with open('data/thesaurus.json', 'r', encoding='utf-8') as f:
            self.thesaurus = json.load(f)
        
        self.sentence_structures = [
            (lambda p1, p2: f"{p1}. Namun, {p2}", 0.6),
            (lambda p1, p2: f"Selain itu, {p1}. {p2}", 0.5),
            (lambda p1, p2: f"{p1}, meskipun demikian {p2}", 0.4),
            (lambda p1, p2: f"Bukan hanya itu, {p1}. {p2}", 0.3)
        ]

    def enhance_sentence_flow(self, sentence):
        """Meningkatkan alur kalimat dengan teknik NLP sederhana"""
        # Ubah struktur aktif-pasif
        if random.random() < 0.5:
            sentence = self.change_voice(sentence)
        
        # Tambahkan konjungsi
        conjunctions = ['sehingga', 'oleh karena itu', 'sementara itu']
        if random.random() < 0.4:
            sentence += f" {random.choice(conjunctions)} {self.generate_related_phrase()}"
        
        return sentence

    def change_voice(self, sentence):
        """Mengubah struktur kalimat aktif-pasif"""
        # Contoh implementasi sederhana
        active_match = re.match(r'(\w+?) (meng|me)(\w+?) (.+)', sentence)
        if active_match:
            return f"{active_match.group(4)} {active_match.group(1)} di{active_match.group(3)}"
        
        passive_match = re.match(r'(\w+?) (di|ter)(\w+?) oleh (.+)', sentence)
        if passive_match:
            return f"{passive_match.group(4).capitalize()} {passive_match.group(1)} {passive_match.group(3)}"
        
        return sentence

    def spin_text(self, text, spin_level=0.85):
        sentences = sent_tokenize(text)
        spun_sentences = []
        
        for sentence in sentences:
            # Lakukan parafrasa struktural
            modified_sentence = self.enhance_sentence_flow(sentence)
            
            # Proses spinning kata per kata
            words = word_tokenize(modified_sentence)
            tagged = pos_tag(words)
            spun_words = []
            
            for word, tag in tagged:
                if word.isupper() or tag == 'NNP':
                    spun_words.append(word)
                    continue
                
                if random.random() < spin_level:
                    synonyms = self.get_contextual_synonyms(word, tag)
                    if synonyms:
                        spun_words.append(random.choice(synonyms))
                        continue
                
                spun_words.append(word)
            
            # Gabungkan dengan struktur kalimat acak
            if len(spun_words) > 5 and random.random() < 0.7:
                split_point = random.randint(2, len(spun_words)-2)
                part1 = ' '.join(spun_words[:split_point])
                part2 = ' '.join(spun_words[split_point:])
                structure, prob = random.choice(self.sentence_structures)
                if random.random() < prob:
                    spun_sentences.append(structure(part1, part2))
                    continue
            
            spun_sentences.append(' '.join(spun_words))
        
        return ' '.join(spun_sentences)

    def get_contextual_synonyms(self, word, tag):
        pos_map = {
            'NN': 'noun',
            'VB': 'verb',
            'JJ': 'adj',
            'RB': 'adv'
        }
        pos = pos_map.get(tag[:2], 'default')
        
        entry = self.thesaurus.get(word.lower(), {})
        if isinstance(entry, dict):
            return entry.get(pos, entry.get('default', []))
        return entry if isinstance(entry, list) else []

    def calculate_quality(self, original, spun):
        """Menghitung kualitas spin dengan 3 metrik"""
        # Hitung keunikan
        orig_words = set(word_tokenize(original.lower()))
        spun_words = set(word_tokenize(spun.lower()))
        uniqueness = len(spun_words - orig_words) / len(spun_words) * 100
        
        # Hitung perbedaan struktural
        orig_sent_count = len(sent_tokenize(original))
        spun_sent_count = len(sent_tokenize(spun))
        structure_diff = abs(orig_sent_count - spun_sent_count) / orig_sent_count * 100
        
        # Hitung variasi kosakata
        vocab_ratio = len(spun_words) / len(orig_words) * 100
        
        return {
            'uniqueness': round(uniqueness, 2),
            'structure': round(100 - structure_diff, 2),
            'vocabulary': round(vocab_ratio, 2)
        }