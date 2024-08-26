import seaborn as sns
from boredcharts.router import FigureRouter

figures = FigureRouter()


@figures.chart("penguins")
def penguins() -> sns.PairGrid:
    df = sns.load_dataset("penguins")
    return sns.pairplot(df, hue="species")
