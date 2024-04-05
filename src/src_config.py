from .prep_transcripts import prep_transcripts, transcript_pdf_to_txt, transcripts_format
from .prep_stocks import prep_stocks
from .prep_earnings import prep_earnings, earning_xlsx_to_csv, earning_format
from .sentiment_analysis import sentiment_analysis, sentiment_analysis_preprocess, sentiment_analysis_nltk
from .recompile_all import recompile_all
from .display_stocks import display_stock
from .display_earnings import display_earnings
from .view_data import query_earning, query_sentiment, query_stock, query_transcript
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
    query_dict = {
        "Query transcripts": query_transcript,
        "Query stocks": query_stock,
        "Query earnings": query_earning,
        "Query sentiments": query_sentiment
    }

    # Sets the dictionaries for displaying the raw data
    # TODO create submenu functions for customizing display of data
    display_stocks_dict = {
        "Display stocks": None,
        "Select companies": None,
        "Set time period": None
    }

    display_earnings_dict = {
        "Display earnings": None,
        "Select companies": None,
        "Set time period": None
    }

    display_dict = {
        "Display stocks": display_stock,
        "Display earnings": display_earnings,
    }

    # sets the full dictionary menu
    full_dict = {
        "Recompile Data": Menu(recompile_dict),
        "Query Database": Menu(query_dict),
        "Display Data": Menu(display_dict),
        "Overwrite Mode": "Change overwrite state"
    }

    return Menu(full_dict)