from django.core.management import BaseCommand

from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords

from texts.models import Text
from texts.signals import normalize_words


class Command(BaseCommand):
    def handle(self, *args, **options):
        stop_words = stopwords.words('russian')

        n_samples = 2000
        n_features = 1000
        min_rating = 0.1

        vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                     stop_words=stop_words)

        texts = Text.objects.filter(is_moderated=False, keywords__isnull=True).order_by('-published')
        print str(len(texts)) + ' frame ' + str(n_samples)
        texts = texts[0:n_samples]
        if len(texts) < n_samples:
            print 'Not enough news, wait while will be more available'
            return
        normalized_texts = []
        for text in texts:
            all_words = unicode(text.title) + ' ' + unicode(text.description) + ' ' + unicode(text.body)
            all_words_normalized = normalize_words(all_words)
            normalized_texts.append(all_words_normalized)

        tfidf = vectorizer.fit_transform(normalized_texts)

        feature_names = vectorizer.get_feature_names()

        for i, text in enumerate(texts):
            rank_per_word = {}
            key_words = []
            for j, word in enumerate(feature_names):
                rank = tfidf[i, j]
                rank_per_word[word] = rank
            while True:
                word_local_max_rank = max(rank_per_word, key=rank_per_word.get)
                local_max_rank = rank_per_word[word_local_max_rank]
                if local_max_rank < min_rating:
                    break
                key_words.append(word_local_max_rank)
                del rank_per_word[word_local_max_rank]
            keywords = ' '.join(key_words)
            text.keywords = keywords if len(keywords) < 1024 else key_words[0:1024]
            text.save()
