# report on sine

> I'm not a fan of this because it's essentially a worse jupyter notebook.
> If you're going to colocate your analysis and commentary, you should use a jupyter notebook.
>
> The reason I don't want to use jupyter notebooks is because I want to do my analysis as code and commentary as markdown, then tie them together really easily.

Simple hello world print:

```py
print("Hello, world!")
```

Import numpy and pyplot.

```py
import numpy as np
import matplotlib.pyplot as plt
```

Generate some data.

```py
x = np.linspace(0, 10, 100)
y = np.sin(x)
```

Plot it:

```py
plt.plot(x, y)
plt.title("Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.show()
```
