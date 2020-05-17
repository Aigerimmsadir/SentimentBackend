from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
import os

class DiplomaSentimentAnalyzer:
    def __init__(self, n_instances=500):
        self.n_instances = n_instances
        self.subj_classifier = None
        self.sentim_analyzer = None
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(os.path.join(BASE_DIR,'main\my_classifier.pickle'), 'rb') as f:
                sentim_analyzer = pickle.load(f)
                self.sentim_analyzer = sentim_analyzer
        except IOError:
            with open('plot.tok.gt9.5000') as obj_sents:
                obj_sents = obj_sents.read()
            with open('quote.tok.gt9.5000') as subj_sents:
                subj_sents = subj_sents.read()
            self.obj_sents = obj_sents
            self.sentim_analyzer = SentimentAnalyzer()
            self.train_diploma(subj_sents, obj_sents)

    def prepair_train_data(self, sents, category):
        stop_words = set(stopwords.words('english'))
        sents_processed = sent_tokenize(sents)
        sents_final = []
        for k in sents_processed:
            sent = word_tokenize(k)
            sent = [w.lower() for w in sent if w not in stop_words]
            lemmatizer = WordNetLemmatizer()
            sent = [lemmatizer.lemmatize(j) for j in sent]
            sents_final.append(sent)
        sents_final = [(i, category) for i in sents_final]
        return sents_final

    def train_diploma(self, subj_sents, obj_sents):
        train_subj = self.prepair_train_data(subj_sents, 'subj')[:self.n_instances]
        train_obj = self.prepair_train_data(obj_sents, 'obj')[:self.n_instances]
        training_docs = train_subj + train_obj
        all_words_neg = self.sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
        unigram_feats = self.sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
        self.sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
        training_set = self.sentim_analyzer.apply_features(training_docs)
        trainer = NaiveBayesClassifier.train
        subj_classifier = self.sentim_analyzer.train(trainer, training_set)
        self.subj_classifier = subj_classifier
        f = open('my_classifier.pickle', 'wb')
        pickle.dump(self.sentim_analyzer, f)
        f.close()

    def get_sentiment_values(self, text):
        result = {}
        if text:
            stop_words = set(stopwords.words('english'))
            sentences = word_tokenize(text)
            sentences = [w.lower() for w in sentences if w not in stop_words]
            lemmatizer = WordNetLemmatizer()
            sentences = [lemmatizer.lemmatize(j) for j in sentences]
            subj_count = 0
            for i in sentences:
                a = self.sentim_analyzer.classify({i, True})
                if a == 'subj':
                    subj_count += 1

            result['subjectivity'] = round((subj_count / len(sentences)),2)*100
            sid = SentimentIntensityAnalyzer()
            polarity = sid.polarity_scores(text)['compound']
            result['polarity'] = (polarity/2+0.5)*100
            return result

