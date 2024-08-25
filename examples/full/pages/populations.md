August 2024

## Summary

We can write our reports in markdown
and use a little bit of jinja magic to pull in charts that we create in python.

## Metrics

The USA's population has been growing linearly:

<pre>
{%- raw %}
{{ figure("usa_population") }}
{% endraw -%}
</pre>

{{ figure("usa_population") }}

South Africa's growth is a bit weirder looking according to this chart:

<pre>
{%- raw %}
{{ figure("population", country="South Africa") }}
{% endraw -%}
</pre>

{{ figure("population", country="South Africa") }}

We can put two charts side by side:

<pre>
{%- raw %}
{{
  row(
    figure("population", country="United Kingdom"),
    figure("population", country="France"),
  )
}}
{% endraw -%}
</pre>

{{
  row(
    figure("population", country="United Kingdom"),
    figure("population", country="France"),
  )
}}

And we can add custom tailwind classes to the figures:

<pre>
{%- raw %}
{{
  row(
    figure("population", country="Canada", class="h-[300px] min-w-[300px]"),
    figure("population", country="Australia", class="h-[300px] min-w-[300px]"),
  )
}}
{% endraw -%}
</pre>

{{
  row(
    figure("population", country="Canada", class="h-[300px] min-w-[300px]"),
    figure("population", country="Australia", class="h-[300px] min-w-[300px]"),
  )
}}

We can also dip into html when we need to
(notice this is exactly the same as the `row` helper earlier):

<pre>
{%- raw %}
&lt;div class="flex flex-wrap"&gt;
  {{ figure("population", country="United Kingdom") }}
  {{ figure("population", country="France") }}
&lt/div&gt;
{% endraw -%}
</pre>

<div class="flex flex-wrap">
  {{ figure("population", country="United Kingdom") }}
  {{ figure("population", country="France") }}
</div>
