import nltk
import os
from ..shared import merge_dicts
from alive_progress import alive_bar
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd


def analyze_sentiment(
        fn: str
) -> dict[str: float]:
    try:
        with open(fn, "r") as file:
            text = file.read()
    except UnicodeDecodeError or TypeError:
        return None
    
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)

    return scores

def nltk_analyze_all(
    src_dir: str
) -> pd.DataFrame | None:
    try:
        nltk.data.find('')
    except LookupError:
        nltk.download('all')
    
    files = os.listdir(src_dir)
    data = {}

    title = f'{'Analyzing Sentiment': <30}'
    with alive_bar(len(files), force_tty=True, title=title) as bar:
        for file in os.listdir(src_dir):
            if not file.endswith('.txt'):
                continue

            dst_fn = os.path.join(src_dir, file)
            row_data = analyze_sentiment(dst_fn)
            row_data['File'] = file
            data = merge_dicts(data, row_data)
            bar()
    
    df = pd.DataFrame.from_dict(data)
    return df