# Define file paths
file_path = '1minute.csv'  # Replace with your actual file path if different
output_file_path = '1minutemod.csv'

# Read the CSV file into a list of lines
with open(file_path, 'r') as file:
    lines = file.readlines()

# Function to process each line: remove dashes from date, handle timezones, and format the output
def process_line(line, is_header=False):
    # Split the line by commas
    parts = line.strip().split(',')
    
    # Handle header separately
    if is_header:
        # Return header unchanged
        return line
    
    # The first part (index 0) should be the datetime with timezone
    datetime_str = parts[0].strip()
    
    # Ensure the datetime_str contains a date part
    if not datetime_str:
        print(f"Skipping line due to missing datetime: {line}")
        return None
    
    try:
        # Split datetime into date and time parts
        date_part, time_with_offset = datetime_str.split(' ')
        time_part, _ = time_with_offset.split('-')  # Ignore the timezone offset
        
        # Remove dashes from the date and reformat the date as YYYYMMDD
        date_part = date_part.replace('-', '')
        
        # Rebuild the line with the modified date and time, and append the rest of the columns
        new_line = f"{date_part},{time_part},{','.join(parts[1:])}\n"
        return new_line
    except ValueError as e:
        print(f"Skipping line due to unexpected format: {line} - Error: {e}")
        return None

# Process the header and data lines
header = process_line(lines[0], is_header=True)  # Process header separately
data_lines = [process_line(line) for line in lines[1:] if process_line(line)]

# Write the modified lines to a new CSV file
with open(output_file_path, 'w') as file:
    file.write(header)  # Write the header first
    file.writelines(data_lines)  # Then write the modified data lines

print(f"File successfully modified and saved as {output_file_path}")

