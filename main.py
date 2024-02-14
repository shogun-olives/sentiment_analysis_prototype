from src import format_data
from src import sentiment_analysis
from src import display_data


def main() -> None:
    # TODO modify to work on personal device, paths may be relative or absolute
    # Paths should be with respect to main
    pdf_loc = './raw/transcripts/pdf'
    txt_loc = './raw/transcripts/txt'
    csv_loc = './raw/stock_history/csv'
    format_txt_loc = './files/transcripts'
    format_csv_loc = './files/stock_data'
    db_name = './files/sentiment_analysis_data.db'

    # formats data
    # format_data.format_data(pdf_loc, txt_loc, csv_loc, format_txt_loc, format_csv_loc, db_name)

    # sensitivity analysis
    # sentiment_analysis.sentiment_analysis(format_txt_loc, db_name)

    # graph

    pass


if __name__ == "__main__":
    main()