import re
from textblob import TextBlob
import language_tool_python
from sentence_transformers import SentenceTransformer, util

class ScoringEngine:
    def __init__(self):
        # Load the AI model (downloads once, might take a minute)
        print("Loading AI Model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.grammar_tool = language_tool_python.LanguageTool('en-US', remote_server='https://api.languagetool.org')

    def analyze(self, text, duration_sec):
        words = text.split()
        word_count = len(words)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        scores = {}
        feedback = []

        # --- CRITERION 1: SALUTATION (5 pts) ---
        salutations_excellent = ["excited to introduce", "feeling great"]
        salutations_good = ["good morning", "good afternoon", "good evening", "hello everyone"]
        salutations_normal = ["hi", "hello"]
        
        lower_text = text.lower()
        if any(s in lower_text for s in salutations_excellent):
            scores['Salutation'] = 5
        elif any(s in lower_text for s in salutations_good):
            scores['Salutation'] = 4
        elif any(s in lower_text for s in salutations_normal):
            scores['Salutation'] = 2
        else:
            scores['Salutation'] = 0
            feedback.append("Start with a formal salutation like 'Good Morning' or 'Hello everyone'.")

        # --- CRITERION 2: KEYWORDS (30 pts) ---
        # Using Semantic Search for "Must Have" (Name, Age, School, Family, Hobbies)
        must_have_topics = ["My name is", "I am years old", "I study at school", "My family consists of", "My hobbies are"]
        good_to_have_topics = ["I am from", "My ambition is", "Fun fact about me", "My strength is"]
        
        # Calculate scores based on semantic similarity
        must_score = 0
        for topic in must_have_topics:
            if self.check_similarity(topic, sentences):
                must_score += 4
        
        good_score = 0
        for topic in good_to_have_topics:
            if self.check_similarity(topic, sentences):
                good_score += 2
        
        scores['Keywords'] = min(30, must_score + good_score) # Cap at 30

        # --- CRITERION 3: FLOW (5 pts) ---
        # Simple check: Salutation at start, Thank you at end
        has_closing = "thank" in lower_text[-50:]
        if scores['Salutation'] > 0 and has_closing:
            scores['Flow'] = 5
        else:
            scores['Flow'] = 0
            if not has_closing: feedback.append("Don't forget to close with 'Thank you'.")

        # --- CRITERION 4: SPEECH RATE (10 pts) ---
        wpm = (word_count / duration_sec) * 60 if duration_sec > 0 else 0
        if 111 <= wpm <= 140:
            scores['Speech Rate'] = 10
        elif 81 <= wpm <= 160: # Covers both slow and fast ranges roughly
            scores['Speech Rate'] = 6
        else:
            scores['Speech Rate'] = 2
            feedback.append(f"Your pace is {int(wpm)} WPM. Ideal range is 111-140 WPM.")

        # --- CRITERION 5: GRAMMAR (10 pts) ---
        matches = self.grammar_tool.check(text)
        error_count = len(matches)
        # Formula: 1 - min(errors per 100 words / 10, 1)
        errors_per_100 = (error_count / word_count) * 100 if word_count > 0 else 0
        grammar_metric = 1 - min(errors_per_100 / 10, 1)
        
        if grammar_metric > 0.9: scores['Grammar'] = 10
        elif grammar_metric > 0.7: scores['Grammar'] = 8
        elif grammar_metric > 0.5: scores['Grammar'] = 6
        elif grammar_metric > 0.3: scores['Grammar'] = 4
        else: scores['Grammar'] = 2

        # --- CRITERION 6: VOCABULARY (10 pts) ---
        unique_words = set([w.lower() for w in words])
        ttr = len(unique_words) / word_count if word_count > 0 else 0
        
        if ttr >= 0.9: scores['Vocabulary'] = 10
        elif ttr >= 0.7: scores['Vocabulary'] = 8
        elif ttr >= 0.5: scores['Vocabulary'] = 6
        elif ttr >= 0.3: scores['Vocabulary'] = 4
        else: scores['Vocabulary'] = 2

        # --- CRITERION 7: FILLER WORDS (15 pts) ---
        fillers = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically']
        filler_count = sum(lower_text.count(f) for f in fillers)
        filler_rate = (filler_count / word_count) * 100 if word_count > 0 else 0
        
        if filler_rate < 3: scores['Filler Words'] = 15
        elif filler_rate < 6: scores['Filler Words'] = 12
        elif filler_rate < 10: scores['Filler Words'] = 9
        elif filler_rate < 13: scores['Filler Words'] = 6
        else: scores['Filler Words'] = 3

        # --- CRITERION 8: ENGAGEMENT (15 pts) ---
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity # Range -1 to 1
        # Normalize to 0-1 (approximate probability of positivity)
        positivity = (sentiment + 1) / 2
        
        if positivity >= 0.9: scores['Engagement'] = 15
        elif positivity >= 0.7: scores['Engagement'] = 12
        elif positivity >= 0.5: scores['Engagement'] = 9
        elif positivity >= 0.3: scores['Engagement'] = 6
        else: scores['Engagement'] = 3

        # FINAL SCORE
        total_score = sum(scores.values())
        return total_score, scores, feedback

    def check_similarity(self, target, sentences):
        # Encodes the target phrase and all sentences in the transcript
        target_emb = self.model.encode(target, convert_to_tensor=True)
        sent_embs = self.model.encode(sentences, convert_to_tensor=True)
        # Checks if any sentence has > 0.4 similarity to the target
        cosine_scores = util.cos_sim(target_emb, sent_embs)
        return cosine_scores.max() > 0.4