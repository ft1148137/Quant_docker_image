from backtrader import observers

class my_buysell(observers.BuySell):
    params = (
        ('barplot', True), 
        ('bardist', 0.01), 
    )
    plotlines = dict(
        buy=dict(marker='^', markersize=5.0, color='#d62728', fillstyle='full', ls=''),
        sell=dict(marker='v', markersize=5.0, color='#2ca02c'))
