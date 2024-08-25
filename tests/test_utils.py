from pathlib import Path

from boredcharts.utils import DirTree, get_dirtree


def test_get_dirtree() -> None:
    directory = Path(__file__).parent.parent / "examples/full/pages"
    expected: DirTree = DirTree(
        name=Path(),
        files=[
            Path("price-elasticity.md"),
            Path("vega-lite-is-cool.md"),
            Path("populations.md"),
        ],
        dirs=[
            DirTree(
                name=Path("more"),
                files=[
                    Path("test.md"),
                ],
                dirs=[],
            )
        ],
    )
    result = get_dirtree(directory)
    assert expected == result
