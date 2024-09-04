August 2024

## Price decrease recommendation

We should drop the price of our widgets by 7% because we'll sell 18% more,
meaning we make more total profit. We observed a price elasticity of 2.5
in the experiment cell where we dropped our price by 7%. With our current margin
of 60%, this would increase our profit by $40,000.

{{ figure("price_vs_quantity", margin=0.6, css_class="") }}

We looked at other price drops of 3% and 10%. The 3% drop had the same
elasticity as the 7% drop, which means it just wouldn't make us as much absolute
profit. The 10% drop had a lower elasticity, meaning we'd make the same absolute
profit as the 7% drop, but we'd have to sell more widgets to do so. I consider
this unpreferable since it would be less capital-efficient, but if there is some
strategic reason to flood the market with our widgets it wouldn't hurt our
bottom line to do so:

{{
  row(
    figure("profit_at_price_drop", drop=0.07, css_class=""),
    figure("profit_at_price_drop", drop=0.10, css_class=""),
  )
}}

We can generalise the elasticity relationship, but the results are kind of intuitive:
the higher your margin, the more you can play with your pricing.

{{ figure("elasticity_vs_profit") }}
