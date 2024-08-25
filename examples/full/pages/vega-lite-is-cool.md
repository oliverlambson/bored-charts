August 2024

## Vega-Lite is cool

Vega-Lite is a "declarative" way to define interactive visualisations.
It's pretty cool, the creators even wrote [a paper about it](https://idl.uw.edu/papers/vega-lite).

Altair is the offical Python library built on top of it,
it's supposed to let you "spend less time writing code and more time exploring your data",
which in-line with what I'm trying to do with [bored-charts](https://github.com/oliverlambson/bored-charts).

Without a lot of effort, you can make a bar chart:

{{ figure("medals") }}

And with the same amount of effort, you can make a multifaceted group of scatterplots showing the correlation between a bunch of variables:

{{ figure("cars.scatter-correlation") }}
