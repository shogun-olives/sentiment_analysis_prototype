from .prepare_stocks import prepare_data
import matplotlib.pyplot as plt
import seaborn as sn
from config import file_locations


# TODO Add functionality to display stock data selectively
def display_stock(
    stock_symbol: str = None,
    time_period: int = 3
) -> None:
    db_name = file_locations['database_db']
    sentiment_table = file_locations['sentiment_analysis_result']
    stock_table = file_locations['stock_metadata']
    stock_dir = file_locations['formatted_stock_csv']
    df = prepare_data(db_name, sentiment_table, stock_table, stock_dir, time_period)
    
    if df is None:
        return None
    
    for col in ['neg', 'neu', 'pos', "Stock", "Symbol"]:
        if col not in df.columns:
            return None

    if stock_symbol is not None:
        if stock_symbol not in df["Symbol"].values:
            return None
        df = df[df["Symbol"] == stock_symbol]

    x_vals = ["neg", "neu", "pos"]

    for x in x_vals:
        sn.scatterplot(data=df, x=x, y="Stock", hue='Symbol')
        # increase resolution of figure
        fig = plt.gcf()
        fig.set_dpi(200)
        fig.tight_layout()
        plt.show()

    return None