#!/usr/bin/env bash

set -euo pipefail

file="${1:-}"
if [ -z "$file" ]; then
	echo "Usage: $0 <file.md>"
	exit 1
fi
name="${file%.md}"
if [ "$file" != "$name.md" ]; then
	echo "File must be markdown"
	exit 1
fi

echo "Preprocessing to make python code blocks compatible with pandoc"
sed -e 's/^```py$/```code/' -e 's/^```python$/```code/' "$file" >"$file.tmp"

echo "Converting to jupyter notebook"
pandoc -f markdown -t ipynb "$file.tmp" -o "$name.ipynb"
rm "$file.tmp"

echo "Exporting to PDF"
jupyter nbconvert --no-input --execute --allow-chromium-download --to webpdf "$name.ipynb"
rm "$name.ipynb"
