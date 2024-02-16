import file_helper as fh
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
from file_helper.shared import file_exists
import timeit
import os


def preprocess(text: str) -> str:
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    lem = WordNetLemmatizer()
    lem_tokens = [lem.lemmatize(token) for token in filtered_tokens]

    processed_text = ' '.join(lem_tokens)

    return processed_text


def get_new_fn(fn: str) -> str:
    name = os.path.basename(fn)
    directory = os.path.dirname(fn)
    directory_dir = os.path.dirname(directory)
    new_dir_name = "preprocessed_transcripts"
    new = os.path.join(directory_dir, new_dir_name, name)
    return new


def preprocess_txt(fn: str) -> dict[str: str]:
    new_fn = get_new_fn(fn)

    directory = os.path.dirname(new_fn)
    os.makedirs(directory, exist_ok=True)
    data = {
        'File': [fn],
        'Processed': [new_fn],
    }

    if not file_exists(new_fn):
        t1 = timeit.default_timer()
        with open(fn, "r") as file:
            try:
                data = file.read()
            except UnicodeDecodeError:
                return None

        new_data = preprocess(data)

        with open(new_fn, "w") as file:
            file.write(new_data)
        t2 = timeit.default_timer()

        print(f"[{os.path.basename(new_fn)}] written in {t2-t1} sec")
    return data


def preprocess_all(df: pd.DataFrame) -> pd.DataFrame:
    files = df['File'].tolist()
    new_files = []
    t1 = timeit.default_timer()
    for file in files:
        new_file = preprocess_txt(file)
        new_files.append(pd.DataFrame.from_dict(new_file))
        pass
    t2 = timeit.default_timer()
    # print(f"Process completed in {t2-t1:.2f} sec")
    processed = pd.concat(new_files)

    new_df = pd.merge(df, processed, on='File', how='outer')

    return new_df


def analyze_sentiment(fn: str):
    try:
        with open(fn, "r") as file:
            text = file.read()
    except UnicodeDecodeError:
        return None
    except TypeError:
        return None
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)

    scores['Processed'] = fn
    return scores


def analyze_all_sentiments(df: pd.DataFrame) -> pd.DataFrame:
    files = df['Processed'].tolist()

    data = []
    for file in files:
        row = analyze_sentiment(file)

        if row is None:
            continue

        for key in row:
            if not isinstance(row[key], list):
                row[key] = [row[key]]

        data.append(pd.DataFrame.from_dict(row))
        pass

    processed = pd.concat(data, ignore_index=True)
    new_df = pd.merge(df, processed, on='Processed', how='outer')

    return new_df


def analyze_data(db_name: str):
    """
    Takes a database that stores presentation data and analyzes sentiment for each presentation
    :param db_name: location of database
    :return: None
    """
    # installs all data
    try:
        nltk.data.find('')
    except LookupError:
        nltk.download('all')

    # gets data from database
    print('Sentiment analysis in progress...')
    t1 = timeit.default_timer()
    df = fh.db_to_df(db_name, "transcripts")
    df = preprocess_all(df)
    df = analyze_all_sentiments(df)
    fh.df_to_db(df, db_name, "transcripts")
    t2 = timeit.default_timer()
    print(f'Time elapsed: {t2-t1:.2f} seconds')


def main() -> None:
    # Paths should be with respect to root
    db = './files/sentiment_analysis_data.db'

    root = '../'
    os.chdir(root)

    # analyzing entire database
    analyze_data(db)


if __name__ == "__main__":
    main()