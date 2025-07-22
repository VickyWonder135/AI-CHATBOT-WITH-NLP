import nltk
import wikipedia
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Small talk dictionary
small_talk = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there!",
    "hey": "Hey! Ask me anything.",
    "who are you": "I am PyBot 🤖, your friendly AI assistant.",
    "what are you": "I am a chatbot that uses AI and Wikipedia to answer your questions.",
    "how are you": "I'm just code, but I'm doing great!"
}

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def get_response(user_input):
    user_input_lower = user_input.lower()
    
    # Check for small talk first
    if user_input_lower in small_talk:
        return small_talk[user_input_lower]
    
    # Try to fetch from Wikipedia
    try:
        keywords = preprocess(user_input)
        if not keywords:
            return "Please ask a more specific question."
        query = " ".join(keywords)
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your question is too broad. Try being more specific like: {e.options[0]}"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything related to that topic."
    except Exception as e:
        return "Oops! Something went wrong. Please try again."

# Chat loop
print("🤖 PyBot: Hi! Ask me anything. Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("🤖 PyBot: Goodbye! 👋")
        break
    response = get_response(user_input)
    print("🤖 PyBot:", response)
