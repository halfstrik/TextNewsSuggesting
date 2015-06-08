from django.db.models.signals import pre_save
from django.dispatch import receiver
from nltk import word_tokenize
import pymorphy2

from texts.models import KeyNormalizedWords

morph = pymorphy2.MorphAnalyzer()


def normalize_words(text):
    word_tokens = word_tokenize(text.lower())
    normalized_word_tokens = []
    for word in word_tokens:
        normalized_word = morph.parse(word)[0].normal_form
        normalized_word_tokens.append(normalized_word)
    return ' '.join(normalized_word_tokens)


@receiver(pre_save, sender=KeyNormalizedWords)
def words_normalization(sender, **kwargs):
    kwargs['instance'].words = normalize_words(kwargs['instance'].words)
