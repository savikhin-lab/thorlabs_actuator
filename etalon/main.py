import os
import sys
import click
import numpy as np
from math import floor
from pathlib import Path
from scipy.interpolate import interp1d
from .actuator import Actuator


@click.group()
def cli():
    pass


@click.command()
@click.option("-l", "loop", is_flag=True, help="Print the position in an indefinite loop.")
@click.option("-w", "wl", is_flag=True, help="Print the position as a wavelength.")
def pos(loop, wl):
    """Report the current position of the stepper motor.
    """
    act = Actuator()
    if wl:
        cal_file_path = os.environ["THORLABSMOTORCAL"]
        if cal_file_path is None:
            print("THORLABSMOTORCAL environment variable not found.")
            sys.exit(-1)
        cal_file_path = Path(cal_file_path)
        cal_data = np.loadtxt(cal_file_path, delimiter=",")
        interp = interp1d(cal_data[:, 1], cal_data[:, 0], kind="linear")
    if loop:
        if wl:
            while True:
                steps = act.pos()
                print(f"{interp(steps):.2f}nm")
        else:
            while True:
                print(f"{act.pos()}")
    else:
        if wl:
            steps = act.pos()
            print(f"{interp(steps):.2f}nm")
        else:
            print(f"{act.pos()}")
    return


@click.command()
@click.argument("new_pos", type=click.FLOAT)
@click.option("-s", "--steps", "is_steps", is_flag=True, help="The position is specified in steps of the stepper motor rather than as a wavelength.")
def move(new_pos, is_steps):
    """Send the stepper to a new position.

    The default units for position are steps of the stepper motor.
    """
    act = Actuator()
    if is_steps:
        act.move(new_pos)
    else:
        act.move_wl(new_pos)
    return


@click.command()
def home():
    """Home the actuator.
    """
    act = Actuator()
    click.echo("Homing...", nl=False)
    act.home()
    click.echo("done")


cli.add_command(pos)
cli.add_command(move)
cli.add_command(home)
