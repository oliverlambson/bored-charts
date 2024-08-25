from pathlib import Path

from boredcharts.utils import DirTree, get_dirtree


def test_get_dirtree() -> None:
    directory = Path(__file__).parent / "pages"
    expected: DirTree = DirTree(
        name=Path(),
        files=[
            Path("example.md"),
        ],
        dirs=[
            DirTree(
                name=Path("nest"),
                files=[
                    Path("test.md"),
                ],
                dirs=[
                    DirTree(
                        name=Path("doublenest"),
                        files=[
                            Path("test2.md"),
                        ],
                        dirs=[],
                    )
                ],
            )
        ],
    )
    result = get_dirtree(directory)
    assert expected == result
