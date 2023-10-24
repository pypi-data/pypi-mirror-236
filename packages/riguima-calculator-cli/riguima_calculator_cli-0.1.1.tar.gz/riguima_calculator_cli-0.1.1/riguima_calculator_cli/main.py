import math

import click


@click.group()
def cli():
    pass


def get_numbers(numbers, float_numbers, even, odd):
    if even:
        return [n for n in numbers if n % 2 == 0]
    elif odd:
        return [n for n in numbers if n % 2 != 0]
    else:
        return numbers + float_numbers


@click.command()
@click.option('-f', '--float-numbers', type=float, multiple=True)
@click.option('--even', is_flag=True)
@click.option('--odd', is_flag=True)
@click.argument('numbers', nargs=-1, type=int)
def add(numbers, float_numbers, even, odd):
    click.echo(sum(get_numbers(numbers, float_numbers, even, odd)))


@click.command()
@click.option('-f', '--float-numbers', type=float, multiple=True)
@click.option('--even', is_flag=True)
@click.option('--odd', is_flag=True)
@click.argument('numbers', nargs=-1, type=int)
def subtract(numbers, float_numbers, even, odd):
    final_numbers = get_numbers(numbers, float_numbers, even, odd)
    result = final_numbers[0]
    for e, _ in enumerate(final_numbers):
        if e != len(final_numbers) - 1:
            result -= final_numbers[e + 1]
    click.echo(result)


@click.command()
@click.option('-f', '--float-numbers', type=float, multiple=True)
@click.option('--even', is_flag=True)
@click.option('--odd', is_flag=True)
@click.argument('numbers', nargs=-1, type=int)
def multiply(numbers, float_numbers, even, odd):
    click.echo(math.prod(get_numbers(numbers, float_numbers, even, odd)))


@click.command()
@click.option('-f', '--float-numbers', type=float, multiple=True)
@click.option('--even', is_flag=True)
@click.option('--odd', is_flag=True)
@click.argument('numbers', nargs=-1, type=int)
def divide(numbers, float_numbers, even, odd):
    final_numbers = get_numbers(numbers, float_numbers, even, odd)
    result = final_numbers[0]
    for e, _ in enumerate(final_numbers):
        if e != len(final_numbers) - 1:
            result /= final_numbers[e + 1]
    click.echo(result)


cli.add_command(add)
cli.add_command(subtract)
cli.add_command(multiply)
cli.add_command(divide)


if __name__ == '__main__':
    cli()
