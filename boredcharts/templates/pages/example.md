{% from "components/figure.html" import figure with context %}

August 2024

## Summary

We can write our reports in markdown
and use a little bit of jinja magic to pull in charts that we create in python.

## Metrics

The USA's population has been growing linearly:

<pre>{% raw %}
{{ figure("example_simple_usa") }}
{% endraw %}</pre>

{{ figure("example_simple_usa") }}

South Africa's growth is a bit weirder looking according to this chart:

<pre>{% raw %}
{{ figure("example_params", country="South Africa") }}
{% endraw %}</pre>

{{ figure("example_params", country="South Africa") }}

We can do light HTML to put two charts side by side:

<pre>{% raw %}
&lt;div class="flex flex-wrap"&gt;
  {{ figure("example_params", country="United Kingdom") }}
  {{ figure("example_params", country="France") }}
&lt;/div&gt;
{% endraw %}</pre>

<div class="flex flex-wrap">
  {{ figure("example_params", country="United Kingdom") }}
  {{ figure("example_params", country="France") }}
</div>

And we can add custom tailwind classes to the figures:

<pre>{% raw %}
&lt;div class="flex flex-wrap"&gt;
  {{ figure("example_params", country="Canada", class="h-[300px] min-w-[300px]") }}
  {{ figure("example_params", country="Australia", class="h-[300px] min-w-[300px]") }}
&lt;/div&gt;
{% endraw %}</pre>

<div class="flex flex-wrap">
  {{ figure("example_params", country="Canada", class="h-[300px] min-w-[300px]") }}
  {{ figure("example_params", country="Australia", class="h-[300px] min-w-[300px]") }}
</div>
