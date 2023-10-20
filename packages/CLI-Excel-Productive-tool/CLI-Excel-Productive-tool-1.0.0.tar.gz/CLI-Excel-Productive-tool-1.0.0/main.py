from rich.live import Live
from rich.console import Console
from rich.style import Style
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich import box


import os
import sys
import csv
from time import sleep
import time
import datetime
from datetime import timedelta

import pyfiglet
from tqdm import tqdm
import inquirer
from yaspin import yaspin
from contextlib import contextmanager

os.system('cls' if os.name == 'nt' else 'clear')  
console = Console()

# Global Variable.
fieldnames = ['Topic', 'Start Date', 'Start Time', 'Duration']

# Define three styles with different colors
excel_style = Style(color="cyan")
productivity_style = Style(color="magenta")
cli_style = Style(color="green")

# Print the text with the respective styles
result = pyfiglet.figlet_format("Excel Productivity", font = "digital" )
console.print("\n",Align.center(Text(result)))

# Create a Text object with the three text parts and their respective styles
text = Text()
text.append("Record Time |", style=excel_style)
text.append(" Stay Productive |", style=productivity_style)
text.append(" CLI Application", style=cli_style)

# Print the centered text
console.print(Align.center(text),"\n")

for i in tqdm(range(0, 100), desc ="Loading ... "):
    sleep(.01)


def initial_start():
        # Create the CSV file if it doesn't exist and write the header row
    with open('timers.csv', 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvfile.seek(0) # Move the file pointer to the beginning
        first_char = csvfile.read(1) # Read the first character
        if not first_char: # If the file is empty
            writer.writeheader()
    

def timer():
    console.clear()
    # Create Figlet object with "big" font
    f = pyfiglet.Figlet(font='big')

    # Get the countdown duration and topic name from the user
    countdown_duration = 0
    while True:
        countdown_input = input("Enter the countdown duration in the format (hh:mm:ss): ")
        try:
            hours, minutes, seconds = countdown_input.split(':')
            countdown_duration = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
            break
        except ValueError:
            print("Invalid input. Please enter the duration in the format '00:00:00'.")

    topic_input = input("Please enter the topic name: ")

    # Record the start date and time
    start_datetime = datetime.datetime.now()
    start_date = start_datetime.strftime('%Y-%m-%d')
    start_time = start_datetime.strftime('%I:%M:%S %p')

    # Loop through the countdown
    for i in range(countdown_duration, 0, -1):
        # Convert the remaining time to hours, minutes, and seconds
        hours = i // 3600
        minutes = (i % 3600) // 60
        seconds = i % 60

        # Format the remaining time as a string
        time_string = f"{hours:02d} : {minutes:02d} : {seconds:02d}"

        # Clear the line and move cursor to beginning of line
        print('\033[2K\r', end='')

        countdown_text = f.renderText(time_string)
        print(countdown_text, end='', flush=True)

        # Calculate the position to move the cursor back to
        # the beginning of the countdown text
        countdown_text_lines = countdown_text.count('\n')
        print('\033[{}A\r'.format(countdown_text_lines), end='')

        # Wait for one second
        time.sleep(1)

    # Add a row to the CSV file
    with open('timers.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'Topic': topic_input,
            'Start Date': start_date,
            'Start Time': start_time,
            'Duration': countdown_input
        })

    # Clear the line and move cursor to beginning of line
    print('\033[2K\r', end='')
    # Print "Time's up!" in big font
    print(f.renderText("Time's up!"))


def stat():
    # Read data from CSV file
        with open("timers.csv", newline="") as csvfile:
            reader = csv.reader(csvfile)
            TABLE_DATA = list(reader)
            column_titles = TABLE_DATA.pop(0)

        BEAT_TIME = 0.04
        
        @contextmanager
        def beat(length: int = 1) -> None:
            yield
            time.sleep(length * BEAT_TIME)

        table = Table(show_footer=False)
        table_centered = Align.center(table)

        console.clear()

        with Live(table_centered, console=console, screen=False, refresh_per_second=20):
            
            table.title = "[not italic]:book:[/] Productive Table [not italic]:book:[/]"
            
            table.add_column("Topic", style="bold", justify="center", no_wrap=True)
            table.add_column("Start Date", style="bold", justify="center", no_wrap=True)
            table.add_column("Start Time", Text.from_markup("[b]Total", justify="right"), style="bold", justify="center", no_wrap=True)

            total_duration = timedelta()
            for row in TABLE_DATA:
                duration = row[3]
                if ":" not in duration:
                    continue
                duration_time = timedelta(hours=int(duration.split(":")[0]), minutes=int(duration.split(":")[1]), seconds=int(duration.split(":")[2]))
                total_duration += duration_time

            table.add_column("Duration\nhh:mm:ss", f"{total_duration}", style="bold", justify="right", no_wrap=True)

            table.columns[2].justify = "right"
            table.columns[3].justify = "right"

        
            for row in TABLE_DATA:
                with beat(10):
                    table.add_row(*row)

            with beat(10):
                table.show_footer = True

            table_width = console.measure(table).maximum

            with beat(10):
                table.columns[0].style = "cyan"
                table.columns[0].header_style = "bold cyan"

                table.columns[1].style = "magenta"
                table.columns[1].header_style = "bold magenta"

                table.columns[2].header_style = "bold red"
                table.columns[2].style = "red"
                table.columns[2].footer_style = "bright_red"
            
                table.columns[3].header_style = "bold green"
                table.columns[3].style = "green"
                table.columns[3].footer_style = "bright_green"
                
                
            with beat(10):
                table.box = box.SIMPLE_HEAD
            
            with beat(10):
                table.row_styles = ["none", "dim"]

            with beat(10):
                table.width = console.width / 1.5
            
            with beat(10):
                table.width = console.width


if __name__ == "__main__":
    initial_start()
    

    while True:
        # Define the options for the main menu
        options = [
            inquirer.List('choice',
                        message="Select an option:",
                        choices=['Start Timer', 'View Stats', 'Exit'],
            ),
        ]

        # Ask the user to choose an option from the main menu
        answers = inquirer.prompt(options)

        # Show a loading symbol for 1 second
        with yaspin(text="Loading...", color="yellow") as spinner:
            sleep(1)
            spinner.ok("✔")

        if answers['choice'] == 'Start Timer':
            timer()
            # Define the options for starting the timer submenu
            options = [
                inquirer.List('choice',
                            message="Select an option:",
                            choices=['Go Back', 'Exit'],
                ),
            ]

            # Ask the user to choose an option from the timer submenu
            answers = inquirer.prompt(options)

            # Show a loading symbol for 1 second
            with yaspin(text="Loading...", color="yellow") as spinner:
                sleep(1)
                spinner.ok("✔")

            if answers['choice'] == 'Go Back':
                continue  # go back to the main menu
            elif answers['choice'] == 'Exit':
                sys.exit()  # exit the program

        elif answers['choice'] == 'View Stats':
            stat()
            # Define the options for viewing stats submenu
            options = [
                inquirer.List('choice',
                            message="Select an option:",
                            choices=['Go Back', 'Exit'],
                ),
            ]

            # Ask the user to choose an option from the stats submenu
            answers = inquirer.prompt(options)

            # Show a loading symbol for 1 second
            with yaspin(text="Loading...", color="yellow") as spinner:
                sleep(1)
                spinner.ok("✔")

            if answers['choice'] == 'Go Back':
                continue  # go back to the main menu
            elif answers['choice'] == 'Exit':
                sys.exit()  # exit the program

        elif answers['choice'] == 'Exit':
            sys.exit()  # exit the program
