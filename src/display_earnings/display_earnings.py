from .prepare_earnings import prepare_data
from ..user_interface import clear_console
from alive_progress import alive_bar
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from statistics import mean
from config import file_locations


def display_earnings():
    db_name = file_locations['database_db']
    sentiment_table = file_locations['sentiment_analysis_result']
    earning_table = file_locations['earning_metadata']
    earning_dir = file_locations['formatted_earnings_csv']

    df = prepare_data(db_name, sentiment_table, earning_table, earning_dir)

    scaler = StandardScaler()
    df[['neg', 'pos']] = scaler.fit_transform(df[['neg', 'pos']])

    dfs = df.groupby('Symbol')
    accuracies = []
    clear_console()
    with alive_bar(len(dfs) * 2, force_tty=True, title='Fitting Model') as bar:
        for symbol, company_df in dfs:
            for analysis_type in ['REV', 'EPS']:
                temp_df = company_df[[analysis_type, 'neg', 'pos']]
                temp_df.dropna()
                X = temp_df[['neg', 'pos']]
                y = temp_df[[analysis_type]]
                try:
                    model = LogisticRegression(solver='liblinear', random_state=0).fit(X, y.values.ravel())
                    predictions = model.predict(X)
                    accuracies.append(
                        (
                            f'{f'{symbol}_{analysis_type}':<8}',
                            f'Avg Prediction: {mean(predictions)}',
                            f'Accuracy: {mean([1 if i == j else 0 for i, j in zip(predictions, y[analysis_type].tolist())])}'
                        )
                    )
                except ValueError:
                    accuracies.append(
                        (
                            f'{f'{symbol}_{analysis_type}':<8}',
                            'Not Enough Data'
                        )
                    )

                bar()

    clear_console()
    for x in accuracies:
        print(*x, sep='\t')

    print('\n[-] Press any key to cointinue...')
    input('[+] ')
    return None