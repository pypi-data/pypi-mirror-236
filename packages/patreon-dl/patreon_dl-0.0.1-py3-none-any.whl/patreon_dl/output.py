import click


def print_table(headers: list[str], data: list[list[str]]):
    widths = [[len(cell) for cell in row] for row in data + [headers]]
    widths = [max(width) for width in zip(*widths)]

    def print_row(row: list[str]):
        for idx, cell in enumerate(row):
            width = widths[idx]
            click.echo(cell.ljust(width), nl=False)
            click.echo("  ", nl=False)
        click.echo()

    underlines = ["-" * width for width in widths]

    print_row(headers)
    print_row(underlines)

    for row in data:
        print_row(row)
