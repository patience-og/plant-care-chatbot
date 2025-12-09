import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. DATA PREPROCESSING FUNCTIONS ---

def split_sentences(text):
    """Splits text into sentences using basic punctuation."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.replace('\n', ' ').strip() for s in sentences if s.strip()]

def clean_text(sentence):
    """Performs simple cleaning: lowercase, removes punctuation/numbers."""
    sentence = sentence.lower()
    sentence = re.sub(r'[^a-z\s]', '', sentence)
    return sentence

def preprocess(text):
    """Orchestrates sentence splitting and cleaning."""
    original_sentences = split_sentences(text)
    cleaned_sentences = [clean_text(s) for s in original_sentences]
    return cleaned_sentences, original_sentences

# --- 2. CHATBOT CORE FUNCTION ---

def plant_chatbot(user_query, top_n=3):
    """
    Finds the top N most relevant statements from the text using TF-IDF.
    """
    try:
        # NOTE: Assumes the plant data file is named 'plant.txt'
        with open("plant.txt", "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        return "Error: Cannot find 'plant.txt'. Please ensure it's in the same directory."

    cleaned, original_sentences = preprocess(text)

    # Filter out sentences that are questions for statement-only answers
    statement_sentences = []
    cleaned_statements = []
    for i, s in enumerate(original_sentences):
        if not s.strip().endswith('?') and cleaned[i].strip():
            statement_sentences.append(s)
            cleaned_statements.append(cleaned[i])

    if not cleaned_statements:
        return "The plant data is empty or only contains questions. I cannot answer."

    # TF-IDF Setup
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(cleaned_statements)

    # Clean and vectorize the user query
    cleaned_query = clean_text(user_query)
    query_vec = vectorizer.transform([cleaned_query])
    similarity = cosine_similarity(query_vec, tfidf).flatten()

    # Check for a high enough initial match to proceed
    if similarity.max() < 0.15: 
        return "I'm sorry, I couldn't find any relevant information for that specific query in my plant knowledge base."
        
    # Get indices of the top N sentences, sorted best to worst
    top_indices = similarity.argsort()[-top_n:][::-1]

    # Combine the top N original statements that have a minimum relevance score
    response_parts = []
    for i in top_indices:
        # Only include answers that are somewhat relevant (score > 0.05)
        if similarity[i] > 0.05:
            response_parts.append(statement_sentences[i])

    if not response_parts:
         return "I couldn't find a sufficiently relevant answer in the data."

    # Join the top sentences with empty lines for clear formatting in Streamlit
    return "\n\n".join(response_parts)