import file_helper as fh
import os
import matplotlib.pyplot as plt


def get_existing_data(db_name: str):
    df = fh.db_to_df(db_name, "sentiment_analysis")
    df.dropna(inplace=True)

    return df


def display_data(db_name, stock_symbol):
    df = get_existing_data(db_name)
    df = df[df["Symbol"] == stock_symbol]

    fig, ax = plt.subplots(2, 2)

    nltk_types = ['neg', 'neu', 'pos']
    x_labels = ["Negative Sentiment", "Neutral Sentiment", "Positive Sentiment"]
    axes = [ax[0, 0], ax[0, 1], ax[1, 0]]

    dfs = df.groupby("Type")

    for label, data in dfs:
        for a, sentiment, x_label in zip(axes, nltk_types, x_labels):
            # model = LinearRegression()
            # model.fit(data[sentiment].tolist(), data['Stock'].tolist())
            #
            # x_new = np.linspace(0, 30, 100)
            # y_new = model.predict(x_new[:, np.newaxis])

            a.scatter(data[sentiment], data['Stock'], alpha=0.5, label=label, s=5)
            a.set_xlabel(x_label)
            a.set_ylabel("Stock Performance")
            a.legend(fontsize="4", loc="upper left")

            # ax.plot(x_new, y_new)

    # improve resolution of output
    plt.gcf().set_dpi(1000)

    # show graph
    fig.tight_layout()

    # shows plots
    plt.show()


def display_all_data(db_name):
    df = get_existing_data(db_name)

    fig, ax = plt.subplots(2, 2)

    nltk_types = ['neg', 'neu', 'pos']
    x_labels = ["Negative Sentiment", "Neutral Sentiment", "Positive Sentiment"]
    axes = [ax[0, 0], ax[0, 1], ax[1, 0]]

    dfs = df.groupby("Symbol")

    for label, data in dfs:
        for a, sentiment, x_label in zip(axes, nltk_types, x_labels):
            a.scatter(data[sentiment], data['Stock'], alpha=0.5, label=label, s=5)
            a.set_xlabel(x_label)
            a.set_ylabel("Stock Performance")
            a.legend(fontsize="4", loc="upper left")

    # improve resolution of output
    plt.gcf().set_dpi(1000)

    # show graph
    fig.tight_layout()

    # shows plots
    plt.show()


def main() -> None:
    db_name = './files/sentiment_analysis_data.db'

    root = '../'
    os.chdir(root)

    comp = "NVDA"
    # display_data(db_name, comp)
    display_all_data(db_name)


if __name__ == "__main__":
    main()