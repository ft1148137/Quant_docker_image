import backtrader as bt

class ChinaStockCommission(bt.CommInfoBase):
    params = (
        ('stamp_duty', 0.001),  
        ('commission', 0.0005),
        ('transfer_fee', 0.0006)
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_PERC),
    )

    def _getcommission(self,size,price,pseudoexec):
        if size > 0:
            return (size*(price * self.p.commission + self.p.transfer_fee))
        elif size < 0:
            return size * price * (self.p.stamp_duty + self.p.commission)
        else:
            return 0;