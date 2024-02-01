import csv
from datetime import timedelta

def total_time_duration(time_list, split_list):
    total_time = timedelta()
    for split, t in zip(split_list, time_list):
        if split.lower() != 'excluded':
            try:
                if t in ["0", "00", ""]:  # Skip invalid or empty time strings
                    continue
                parts = t.split(":")
                if len(parts) == 3:  # If format is hours, minutes, and seconds (HH:MM:SS)
                    hours, minutes, seconds = map(int, parts)
                    total_time += timedelta(hours=hours, minutes=minutes, seconds=seconds)
                elif len(parts) == 2:  # If format is minutes and seconds (MM:SS)
                    minutes, seconds = map(int, parts)
                    total_time += timedelta(minutes=minutes, seconds=seconds)
                else:
                    print(f"Unexpected time format: {t}")
            except ValueError as e:
                print(f"Invalid time format: {t} - Error: {e}")
                continue
    return total_time

def calculate_total_time_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        split_column, time_column = [], []
        for row in reader:
            split_column.append(row[13]) 
            time_column.append(row[6]) 
    total_time = total_time_duration(time_column, split_column)
    total_seconds = total_time.total_seconds()
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    total_seconds = total_seconds % 60
    return total_hours, total_minutes, total_seconds


hours, minutes, seconds = calculate_total_time_from_csv("C:\\Users\\nikit\\escraping_hell\\pudoms.csv")
print(f"Total time: {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds")



