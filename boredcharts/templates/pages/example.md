{% from "components/figure.html" import figure with context %}

August 2024

## Summary

...

## Metrics

The USA's population has been growing linearly:

{{ figure(report, "example_simple_usa") }}

South Africa's growth is a bit weirder looking according to this chart:

{{ figure(report, "example_params", country="South Africa") }}
