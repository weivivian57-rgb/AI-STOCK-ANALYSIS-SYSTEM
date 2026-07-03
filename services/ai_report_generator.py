"""
ai_report_generator.py

AI股票分析报告生成模块
"""

from models.stock import Stock


class AIReportGenerator:
    """
    AI分析报告生成器
    """

    def generate(self, stock: Stock):
        """
        根据股票技术指标生成分析报告
        """

        report = []

        # ==========================
        # 💡 自动识别币种 (Currency Identification)
        # ==========================
        if stock.code.endswith((".SS", ".SZ")):
            currency = "元"
        else:
            currency = "美元"

        # ==========================
        # 股票信息
        # ==========================
        report.append(f"股票代码：{stock.code}")
        report.append(f"当前价格：{stock.latest_price:.2f} {currency}")

        # ==========================
        # MA分析
        # ==========================
        if stock.latest_price > stock.ma20:
            report.append(
                f"当前价格高于 MA20（{stock.ma20:.2f}），说明中期走势偏强。"
            )
        else:
            report.append(
                f"当前价格低于 MA20（{stock.ma20:.2f}），说明中期走势偏弱。"
            )

        # ==========================
        # RSI分析
        # ==========================
        if stock.rsi > 70:
            report.append(
                f"RSI 为 {stock.rsi:.2f}，股票处于超买区，短期可能回调。"
            )

        elif stock.rsi < 30:
            report.append(
                f"RSI 为 {stock.rsi:.2f}，股票处于超卖区，可能出现反弹。"
            )

        else:
            report.append(
                f"RSI 为 {stock.rsi:.2f}，市场处于中性状态。"
            )

        # ==========================
        # MACD分析
        # ==========================
        if stock.macd > 0:
            report.append(
                f"MACD 为 {stock.macd:.2f}，多头动能占优。"
            )
        else:
            report.append(
                f"MACD 为 {stock.macd:.2f}，空头动能仍然存在。"
            )

        # ==========================
        # 趋势预测
        # ==========================
        if stock.prediction:

            future = stock.prediction[-1]

            if future > stock.latest_price:
                trend = "上涨"

            elif future < stock.latest_price:
                trend = "下跌"

            else:
                trend = "震荡"

            report.append(
                f"根据线性回归模型预测，未来5个交易日股价预计呈{trend}趋势，"
                f"预测价格约为 {future:.2f} {currency}。"
            )

        # ==========================
        # 综合建议
        # ==========================
        if stock.rsi < 70 and stock.macd > 0:
            report.append(
                "综合判断：股票走势较健康，可继续关注后续上涨机会。"
            )

        elif stock.rsi > 70:
            report.append(
                "综合判断：建议谨慎追高，注意回调风险。"
            )

        else:
            report.append(
                "综合观察：建议继续观察，等待更加明确的买卖信号。"
            )

        return "\n".join(report)