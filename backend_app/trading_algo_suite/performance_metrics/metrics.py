import numpy as np


def performance_metrics(backtest_results, no_of_trades):
    backtest_results.set_index('timestamp', inplace=True)

    # Calculate daily returns
    backtest_results['daily_return'] = backtest_results['balance'].pct_change().fillna(0)

    # Performance metrics
    initial_balance = backtest_results['balance'].iloc[0]
    ending_balance = backtest_results['balance'].iloc[-1]
    cumulative_return = (ending_balance - initial_balance) / initial_balance
    annualized_return = (1 + cumulative_return) ** (no_of_trades / len(backtest_results)) - 1
    volatility = backtest_results['daily_return'].std() * np.sqrt(no_of_trades)
    sharpe_ratio = (backtest_results['daily_return'].mean() / backtest_results['daily_return'].std()) * np.sqrt(no_of_trades)
    max_drawdown = (backtest_results['balance'].cummax() - backtest_results['balance']).max() / backtest_results[
        'balance'].cummax().max()

    # Additional metrics
    calmar_ratio = annualized_return / max_drawdown
    sortino_ratio = (backtest_results['daily_return'].mean() / backtest_results[backtest_results['daily_return'] < 0][
        'daily_return'].std()) * np.sqrt(no_of_trades)
    win_rate = len(backtest_results[backtest_results['daily_return'] > 0]) / len(backtest_results)
    profit_factor = backtest_results[backtest_results['daily_return'] > 0]['daily_return'].sum() / - \
    backtest_results[backtest_results['daily_return'] < 0]['daily_return'].sum()

    # Print metrics
    print(f'Cumulative Return: {cumulative_return * 100:.2f}%')
    print(f'Annualized Return: {annualized_return * 100:.2f}%')
    print(f'Volatility: {volatility * 100:.2f}%')
    print(f'Sharpe Ratio: {sharpe_ratio:.2f}')
    print(f'Maximum Drawdown: {max_drawdown * 100:.2f}%')
    print(f'Calmar Ratio: {calmar_ratio:.2f}')
    print(f'Sortino Ratio: {sortino_ratio:.2f}')
    print(f'Win Rate: {win_rate * 100:.2f}%')
    print(f'Profit Factor: {profit_factor:.2f}')
