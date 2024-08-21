August 2024

## Summary

We can write our reports in markdown
and use a little bit of jinja magic to pull in charts that we create in python.

## Metrics

The USA's population has been growing linearly:

<pre>
{%- raw %}
{{ figure("example_simple_usa") }}
{% endraw -%}
</pre>

{{ figure("example_simple_usa") }}

South Africa's growth is a bit weirder looking according to this chart:

<pre>
{%- raw %}
{{ figure("example_params", country="South Africa") }}
{% endraw -%}
</pre>

{{ figure("example_params", country="South Africa") }}

We can put two charts side by side:

<pre>
{%- raw %}
{{
  row(
    figure("example_params", country="United Kingdom"),
    figure("example_params", country="France"),
  )
}}
{% endraw -%}
</pre>

{{
  row(
    figure("example_params", country="United Kingdom"),
    figure("example_params", country="France"),
  )
}}

And we can add custom tailwind classes to the figures:

<pre>
{%- raw %}
{{
  row(
    figure("example_params", country="Canada", class="h-[300px] min-w-[300px]"),
    figure("example_params", country="Australia", class="h-[300px] min-w-[300px]"),
  )
}}
{% endraw -%}
</pre>

{{
  row(
    figure("example_params", country="Canada", class="h-[300px] min-w-[300px]"),
    figure("example_params", country="Australia", class="h-[300px] min-w-[300px]"),
  )
}}

We can also dip into html when we need to
(notice this is exactly the same as the `row` helper earlier):

<pre>
{%- raw %}
&lt;div class="flex flex-wrap"&gt;
  {{ figure("example_params", country="United Kingdom") }}
  {{ figure("example_params", country="France") }}
&lt/div&gt;
{% endraw -%}
</pre>

<div class="flex flex-wrap">
  {{ figure("example_params", country="United Kingdom") }}
  {{ figure("example_params", country="France") }}
</div>

Or a matplotlib char
(this is buggy though, mpld3 is not actively supported which means we shouldn't really do this):

{{ figure("elasticity_vs_profit") }}
