import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from ..file_helper import file_exists
from alive_progress import alive_bar
import string
import os


def preprocess_str(
    text: str,
    freq_threshold: float = 0.1
) -> str:
    """
    Preprocesses text by removing stopwords, punctuation, and lemmatizing words
    :param text: text to be preprocessed
    :param freq_threshold: threshold for removing words that appear more than a certain percentage of the time
    :return: preprocessed text
    """
    # If invalid frequency threshold, warn user and set to default
    if freq_threshold < 0 or freq_threshold > 1:
        print("Invalid frequency threshold. Defaulting to 0.1")
        freq_threshold = 0.1

    # Get necessary datasets
    stopWords = set(stopwords.words('english'))
    words = set(nltk.corpus.words.words())
    
    # Remove unnecessary spaces
    text = text.strip()
    text = " ".join(text.split())

    # Tokenize the text
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]

    # Remove stopwords and punctuation and apostrophes
    filtered_tokens = [token for token in tokens if token not in stopWords]
    filtered_tokens = [token for token in filtered_tokens if token not in string.punctuation]
    rem_chars = ['\'', '-', '�']
    filtered_tokens = [token for token in filtered_tokens if not any(w in token for w in rem_chars)]

    # removes words that appear in more than 10% of the document
    fdist = nltk.FreqDist(tokens)
    filtered_tokens = [token for token in filtered_tokens if fdist[token] < fdist.N() * freq_threshold]

    # Lemmatize the tokens
    lem = WordNetLemmatizer()
    lem_tokens = [lem.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back together
    processed_text = ' '.join(lem_tokens)

    # return the processed text
    return processed_text


def preprocess_txt(
    src_fn: str,
    dst_fn: str,
    overwrite: bool = False
) -> bool:
    """
    Preprocesses a text file by removing stopwords, punctuation, and lemmatizing words
    :param src_fn: source file name
    :param dst_fn: destination file name
    :return: True if successful, False otherwise
    """
    if not file_exists(src_fn):
        return False
    if file_exists(dst_fn) and not overwrite:
        return True
    
    os.makedirs(os.path.dirname(dst_fn), exist_ok=True)

    try:
        with open(src_fn, "r") as file:
            text = file.read()
    except UnicodeDecodeError or TypeError:
        return False
    
    processed = preprocess_str(text) 

    with open(dst_fn, "w") as file:
        file.write(processed)
    
    return True


def preprocess_all(
    src_dir: str,
    dst_dir: str,
    overwrite: bool = False
) -> bool:
    """
    Preprocesses all text files in src_dir by removing stopwords, punctuation, and lemmatizing words
    :param src_dir: source directory
    :param dst_dir: destination directory
    :param overwrite: True to overwrite existing, False to do nothing
    :return: True if successful, False otherwise
    """
    files = os.listdir(src_dir)
    success = False
    title = f'{'Preprocessing Transcripts': <30}'
    with alive_bar(len(files), title=title, force_tty=True) as bar:
        for file in files:
            if not file.endswith('.txt'):
                continue

            src_fn = os.path.join(src_dir, file)
            dst_fn = os.path.join(dst_dir, file)
            if preprocess_txt(src_fn, dst_fn, overwrite):
                success = True
            bar()
    return success