import csv
from datetime import timedelta

def total_time_duration(time_list):
    total_time = timedelta()
    for t in time_list:
        parts = t.split(":")
        if len(parts) == 2:  # If format is minutes and seconds
            total_time += timedelta(minutes=int(parts[0]), seconds=int(parts[1]))
        elif len(parts) == 3:  # If format includes hours, which is treated as minutes here
            total_time += timedelta(minutes=int(parts[0]), seconds=int(parts[1]))
    return total_time

def calculate_total_time_from_csv(csv_file_path):
    # Open the CSV file and read the column of time data
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if there is one
        time_column = [row[0] for row in reader]  # Assuming time data is in the first column

    # Calculate total time duration
    total_time = total_time_duration(time_column)

    # Convert total duration to hours, minutes, and seconds
    total_hours = total_time.seconds // 3600
    total_minutes = (total_time.seconds // 60) % 60
    total_seconds = total_time.seconds % 60

    return total_hours, total_minutes, total_seconds

# Example usage (You will need to replace 'path/to/your/file.csv' with the actual file path)
# hours, minutes, seconds = calculate_total_time_from_csv('path/to/your/file.csv')
# print(f"Total time: {hours} hours, {minutes} minutes, and {seconds} seconds")
