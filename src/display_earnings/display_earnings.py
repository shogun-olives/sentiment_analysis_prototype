import file_helper as fh
import os
from alive_progress import alive_bar
from sklearn.linear_model import LogisticRegression
from statistics import mean


def get_existing_data(db_name: str):
    df = fh.db_to_df(db_name, "earnings")
    df.dropna(inplace=True)

    return df

# TODO rebuild this function from the top down
def earnings_model(db_name):
    df = get_existing_data(db_name)

    dfs = df.groupby('Symbol')
    accuracies = []
    with alive_bar(len(dfs) * 2, force_tty=True, title='Fitting Model') as bar:
        for symbol, company_df in dfs:
            for analysis_type in ['REV', 'EPS']:
                temp_df = company_df[[analysis_type, 'neg', 'pos', 'neu']]
                temp_df.dropna()
                X = temp_df[['neg', 'pos', 'neu']]
                y = temp_df[[analysis_type]]
                try:
                    model = LogisticRegression(solver='liblinear', random_state=0).fit(X, y.values.ravel())
                    predictions = model.predict(X)
                    accuracies.append(
                        (
                            f'{symbol}_{analysis_type}',
                            f'Avg Prediction: {mean(predictions)}',
                            f'Accuracy: {mean([1 if i == j else 0 for i, j in zip(predictions, y[analysis_type].tolist())])}'
                        )
                    )
                except ValueError:
                    accuracies.append(
                        (f'{symbol}_{analysis_type}',
                        'Not Enough Data'
                        )
                    )

                bar()

    for x in accuracies:
        print(x)


def main() -> None:
    db_name = './files/sentiment_analysis_data.db'

    root = '../'
    os.chdir(root)

    comp = "NVDA"
    # display_data(db_name, comp)
    earnings_model(db_name)


if __name__ == "__main__":
    main()