from .prep_transcripts import prep_transcripts
from .prep_stocks import prep_stocks
from .prep_earnings import prep_earnings
from .sentiment_analysis import sentiment_analysis


def recompile_all() -> bool:
    funcs = [
        prep_transcripts,
        prep_stocks,
        prep_earnings,
        sentiment_analysis
    ]

    for func in funcs:
        if not func():
            return False
        
    return True