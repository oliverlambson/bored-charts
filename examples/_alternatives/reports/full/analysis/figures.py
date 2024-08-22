import numpy as np
import matplotlib.pyplot as plt


def cosplot():
    x = np.linspace(0, 10, 100)
    y = np.cos(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Cosine Wave")
    ax.set_xlabel("x")
    ax.set_ylabel("cos(x)")
    return fig
