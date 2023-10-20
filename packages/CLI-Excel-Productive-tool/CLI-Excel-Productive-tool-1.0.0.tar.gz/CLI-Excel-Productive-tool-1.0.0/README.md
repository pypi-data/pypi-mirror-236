## CLI-Excel-Productive-tool

TimeTracker-CLI is a command-line interface (CLI) application designed to help users efficiently track and manage their time spent on various tasks and projects.

#### Description. 
Easy-to-use CLI Interface: TimeTracker-CLI provides a user-friendly command-line interface, enabling users to quickly start, stop, and manage their time tracking without the need for complex graphical user interfaces. With a series of simple commands, users can navigate the application and maintain their time records with ease.

#### Code Explanation.
<ol>
<li><code>initial_start()</code>: This function initializes the CSV file 'timers.csv' with the headers ('Topic', 'Start Date', 'Start Time', 'Duration') if it doesn't exist.</li>
<li><code>timer()</code>: This function manages the countdown timer for the user. It gets the countdown duration and topic name from the user, starts the timer, and updates the CSV file with the topic, start date, start time, and duration after the timer ends.</li>
<li><code>stat():</code>' This function reads data from the 'timers.csv' file and displays it in a table format using the Rich library. It also adds styling to the table for better visualization.
</li>
</ol>

The rest of the code in the script is primarily concerned with user interface (UI) elements, such as getting input from the user, displaying options and choices, and handling the user's selections. The main part of the code, the <code>if __name__ == "__main__":</code> block, initializes the CSV file, and runs a loop to handle user input for starting timers, viewing stats, or exiting the application.
