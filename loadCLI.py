"""Let's build an CLI for the load.py file using click library."""

import sys
import click
from mylib.load import trimp, trimp_lt, hrrs

def validate_input(value):
    """Validate that input is non-negative"""
    if value < 0:
        raise ValueError("Input values must be non-negative")
    return value

def validate_and_convert(value):
    """Convert string to integer and validate"""
    try:
        int_value = int(value)
        return validate_input(int_value)
    except ValueError:
        # Instead of raising BadParameter, we return None to handle it in the calling function
        return None

def get_valid_input(prompt_text, value=None):
    """Helper function to get and validate input"""
    if value is None:
        value = click.prompt(prompt_text, type=str)
    
    result = validate_and_convert(value)
    if result is None:
        click.echo("Error: Input must be an integer", err=True)
        sys.exit(1)
    return result

@click.group()
def cli():
    """A running load calculator"""
    click.echo("Welcome to the Load Calculator!")

@click.command("trimp")
def trimp_cli():
    """Calculate TRIMP value"""
    try:
        avg_hr = get_valid_input("Average Heart Rate")
        max_hr = get_valid_input("Maximum Heart Rate")
        rest_hr = get_valid_input("Resting Heart Rate")
        workout_duration = get_valid_input("Workout Duration")
        
        trimp_value = trimp(avg_hr, max_hr, rest_hr, workout_duration)
        click.echo(f"TRIMP value: {trimp_value:.3f}")
        return 0
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@click.command("trimp_lt")
def trimp_lt_cli():
    """Calculate TRIMP_LT value"""
    try:
        lt_hr = get_valid_input("Lactate Threshold Heart Rate")
        max_hr = get_valid_input("Maximum Heart Rate")
        rest_hr = get_valid_input("Resting Heart Rate")
        
        trimp_lt_value = trimp_lt(lt_hr, max_hr, rest_hr)
        click.echo(f"TRIMP_LT value: {trimp_lt_value:.3f}")
        return 0
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@click.command("hrrs")
def hrrs_cli():
    """Calculate HRRS value"""
    try:
        avg_hr = get_valid_input("Average Heart Rate")
        max_hr = get_valid_input("Maximum Heart Rate")
        rest_hr = get_valid_input("Resting Heart Rate")
        workout_duration = get_valid_input("Workout Duration")
        lt_hr = get_valid_input("Lactate Threshold Heart Rate")
        
        hrrs_value = hrrs(avg_hr, max_hr, rest_hr, workout_duration, lt_hr)
        click.echo(f"HRRS value: {hrrs_value:.3f}")
        return 0
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

cli.add_command(trimp_cli)
cli.add_command(trimp_lt_cli)
cli.add_command(hrrs_cli)

if __name__ == "__main__":
    cli()