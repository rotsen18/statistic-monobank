import matplotlib.pyplot as plt
import numpy as np

from statement.report import Report


class Chart:
    @classmethod
    def show_amount(cls, report: Report):
        dates = report.get_all_date()
        balances = report.get_all_amounts()
        amount_plt = cls._build_bar(raw_x=dates, raw_y=balances)
        amount_plt.show()

    @classmethod
    def show_balance(cls, report: Report):
        dates = report.get_all_date()
        balances = report.get_all_balances()
        amount_plt = cls._build_plot(raw_x=dates, raw_y=balances)
        amount_plt.show()

    @staticmethod
    def _build_plot(raw_x: list, raw_y: list):
        np_x = np.array(raw_x)
        np_y = np.array(raw_y)
        plt.plot(np_x, np_y)
        return plt

    @staticmethod
    def _build_bar(raw_x: list, raw_y: list):
        np_x = np.array(raw_x)
        np_y = np.array(raw_y)
        plt.bar(np_x, np_y)
        return plt

