import os

# Set the path to your folder
folder_path = "C:\\Users\\nikit\\escraping_hell\\PDF"

# Define the range of numbers you want to check
start_number = 1
end_number = 213

# Create a set with all numbers in the range
full_range = set(range(start_number, end_number + 1))

# Create an empty set to store the found numbers
found_numbers = set()

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    try:
        # Extract the number from the filename (assuming the format "X.pdf")
        number = int(filename.split('.')[0])
        
        # Add the number to the found_numbers set
        found_numbers.add(number)
    except (ValueError, IndexError):
        # Ignore files that are not in the expected format
        pass

# Calculate the missing numbers by finding the difference
missing_numbers = full_range - found_numbers

# Print the missing numbers
if missing_numbers:
    print("Missing numbers:", sorted(missing_numbers))
else:
    print("No missing numbers found.")