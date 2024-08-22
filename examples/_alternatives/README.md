# Reports from markdown + python with existing tools

It's useful to consider our alternatives before rolling our own ([bored-charts](https://www.github.com/oliverlambson/bored-charts)).

> [!NOTE]
>
> I've come across [jupytext](https://jupytext.readthedocs.io/en/latest/using-cli.html) since writing this,
> it looks like it might be a slicker solution than pandoc + nbconvert.
>
> Regardless, I'll probably use that instead of committing my jupyter notebooks in the future.
> You can edit both the .py (vim!) and the .ipynb (visualisations!), and they'll stay in sync.

We can achieve markdown with python charts -> pdf via pandoc and nbconvert:

1. Convert markdown to jupyter notebook with pandoc
2. Execute the notebook and output it to pdf with nbconvert

Two examples are provided: (1) a full example with separated python analysis and execution of
them in markdown code cells, and (2) a minimal example with inline python code. (I really
don't like the inline code—at that point all we've done is make a worse jupyter notebook.
Remember, the point of this is to actually do our analysis as code so that it's separate, clear, and maybe even tested.)

## Running the examples

You're going to need [uv](<(https://docs.astral.sh/uv/getting-started/installation/)>) and
[pandoc](https://pandoc.org/installing.html) installed.

```sh
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate
./build.sh examples/full/main.md # or ./build.sh examples/minimal/main.md
```

## Comparison to bored-charts

<table>
  <tr>
    <th></th>
    <th>pros</th>
    <th>cons</th>
  </tr>
  <tr>
    <th>pandoc + nbconvert</th>
    <td>
      <ul>
        <li>uses existing tools</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>no live reports, only statically built<sup>[1]</sup></li>
        <li>heavy dependencies</li>
        <li>encourages inline code</li>
      </ul>
    </td>
  </tr>
  <tr>
    <th>bored-charts</th>
    <td>
      <ul>
        <li>live reports</li>
        <li>lightweight</li>
        <li>extensible</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>some guy's side project</li>
        <li>limited analysis logic in markdown<sup>[2]</sup></li>
      </ul>
    </td>
  </tr>
</table>

---

1. We could use voila for live reports, but at that point we've gone fully square peg in round hole.
2. I think this is a pro.
