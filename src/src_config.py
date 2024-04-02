from .prep_transcripts import prep_transcripts, transcript_pdf_to_txt, transcripts_format
from .prep_stocks import prep_stocks
from .prep_earnings import prep_earnings, earning_xlsx_to_csv, earning_format
from .sentiment_analysis import sentiment_analysis, sentiment_analysis_preprocess, sentiment_analysis_nltk
from .recompile_all import recompile_all
from .user_interface import Menu

def get_sentiment_analysis_menu() -> Menu:
    # Sets the dictionaries for recompiling the data
    recompile_transcripts_dict = {
        "Recompile transcripts": prep_transcripts,
        "Recompile transcript from pdf to txt": transcript_pdf_to_txt,
        "Recompile transcript formatting": transcripts_format
    }

    recompile_earnings_dict = {
        "Recompile earnings": prep_earnings,
        "Recompile earning from xlsx to csv": earning_xlsx_to_csv,
        "Recompile earning formatting": earning_format
    }

    recompile_sentiment_analysis_dict = {
        "Recompile sentiments": sentiment_analysis,
        "Recompile processed transcripts": sentiment_analysis_preprocess,
        "Recompile sentiment analysis": sentiment_analysis_nltk
    }

    recompile_dict = {
        "Recompile all steps": recompile_all,
        "Recompile transcripts": Menu(recompile_transcripts_dict),
        "Recompile stocks": prep_stocks,
        "Recompile earnings": Menu(recompile_earnings_dict),
        "Recompile sentiments": Menu(recompile_sentiment_analysis_dict)
    }

    # sets the fictionary for querying the data
    # TODO complete querying functions
    query_dict = {
        "Query transcripts": None,
        "Query stocks": None,
        "Query earnings": None,
        "Query sentiments": None
    }

    # Sets the dictionaries for displaying the raw data
    # TODO complete displaying functions
    display_dict = {
        "Display earnings": None,
        "Display stocks": None,
    }

    # sets the full dictionary menu
    full_dict = {
        "Recompile Data": Menu(recompile_dict),
        "Query Dataframe": Menu(query_dict),
        "Display Data": Menu(display_dict),
        "Overwrite Mode": "Change overwrite state"
    }

    return Menu(full_dict)