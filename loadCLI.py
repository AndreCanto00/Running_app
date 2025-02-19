"""Let's build an CLI for the load.py file using click library."""

import click

from mylib.load import trimp, trimp_lt, hrrs


@click.group()
def cli():
    """A running load calculator"""
    click.echo("Welcome to the Load Calculator!")


# Let's build 3 commands for each function in load.py file. We can ask to input the input of the function and return the output.
# The first command is for trimp function. Use the click.prompt to ask the user to input the values.
# The function trimp is called with the input values and the output is printed.


@click.command("trimp")
def trimp_cli():
    """Calculate TRIMP value"""
    avg_hr = click.prompt("Average Heart Rate", type=int)
    max_hr = click.prompt("Maximum Heart Rate", type=int)
    rest_hr = click.prompt("Resting Heart Rate", type=int)
    workout_duration = click.prompt("Workout Duration", type=int)
    trimp_value = trimp(avg_hr, max_hr, rest_hr, workout_duration)
    click.echo(f"TRIMP value: {trimp_value}")


# The second command is for trimp_lt function
@click.command("trimp_lt")
def tripm_lt_cli():
    """Calculate TRIMP_LT value"""
    lt_hr = click.prompt("Lactate Threshold Heart Rate", type=int)
    max_hr = click.prompt("Maximum Heart Rate", type=int)
    rest_hr = click.prompt("Resting Heart Rate", type=int)
    trimp_lt_value = trimp_lt(lt_hr, max_hr, rest_hr)
    click.echo(f"TRIMP_LT value: {trimp_lt_value}")


# The third command is for hrrs function
@click.command("hrrs")
def hrrs_cli():
    """Calculate HRRS value"""
    avg_hr = click.prompt("Average Heart Rate", type=int)
    max_hr = click.prompt("Maximum Heart Rate", type=int)
    rest_hr = click.prompt("Resting Heart Rate", type=int)
    workout_duration = click.prompt("Workout Duration", type=int)
    lt_hr = click.prompt("Lactate Threshold Heart Rate", type=int)
    hrrs_value = hrrs(avg_hr, max_hr, rest_hr, workout_duration, lt_hr)
    click.echo(f"HRRS value: {hrrs_value}")


# Add the commands to the group
cli.add_command(trimp_cli)
cli.add_command(tripm_lt_cli)
cli.add_command(hrrs_cli)


if __name__ == "__main__":
    cli()
