from .prep_transcripts import prep_transcripts
from .prep_stocks import prep_stocks
from .sentiment_analysis import sentiment_analysis


def recompile_all() -> bool:
    funcs = [
        prep_transcripts,
        prep_stocks,
        sentiment_analysis
    ]

    for func in funcs:
        if not func():
            return False
        
    return True