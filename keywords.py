import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

def keywords(file_text):
    translator = str.maketrans('', '', string.punctuation)
    words = word_tokenize(file_text.translate(translator))

            # Remove stop words
    stop_words = set(stopwords.words('english'))
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAa",stop_words)
    words = [word for word in words if word.casefold() not in stop_words]

            # print("BBBBBBBBBBBBBBBBBBBBB",words)

    clean_paragraph = file_text.translate(str.maketrans("", "", string.punctuation))
            # Perform lemmatization on words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCC",words)

            # Get the frequency distribution of words
    freq_dist = nltk.FreqDist(words)

    # Get the most common words as keywords
    keywords = [word for word, freq in freq_dist.most_common(5)]

    print("Top 5 Keywords ===================>>>>>>  ",keywords)
    return keywords