from .prepare_stocks import prepare_data
from ..user_interface import Menu
import matplotlib.pyplot as plt
import seaborn as sn
from config import file_locations


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

    fig, ax = plt.subplots(2, 2)

    sn.scatterplot(data=df, x="neg", y="Stock", hue='Symbol', ax=ax[0, 0])
    sn.scatterplot(data=df, x="neu", y="Stock", hue='Symbol', ax=ax[0, 1])
    sn.scatterplot(data=df, x="pos", y="Stock", hue='Symbol', ax=ax[1, 0])

    # show graph
    fig.tight_layout()

    # shows plots
    plt.show()