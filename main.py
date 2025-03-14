import pandas as pd
import re
from datetime import timedelta

# Function to convert time descriptions into seconds
def convert_to_seconds(time_str):
    time_str = time_str.lower().strip()
    
    if "second" in time_str:
        if "few" in time_str:
            return 5  # Assume 'a few seconds' is 5 seconds
        return int(re.findall(r'\d+', time_str)[0])  # Extract number of seconds
    elif "minute" in time_str:
        if "few" in time_str:
            return 5 * 60  # Assume 'a few minutes' is 5 minutes
        elif "an" in time_str:  # "an minute" -> "1 minute"
            return 1 * 60
        return int(re.findall(r'\d+', time_str)[0]) * 60  # Extract number of minutes and convert to seconds
    elif "hour" in time_str:
        if "an" in time_str:  # "an hour" -> "1 hour"
            return 1 * 3600
        return int(re.findall(r'\d+', time_str)[0]) * 3600  # Extract number of hours and convert to seconds
    else:
        return 0  # Default case for unknown formats, treat as 0 seconds

# Function to format time in HH:MM:SS
def format_time(seconds):
    return str(timedelta(seconds=seconds))

# Sample time descriptions
time_descriptions = [
    "a few seconds", "6 minutes", "an hour", "a minute", "2 hours", 
    "12 minutes", "a minute", "a few seconds", "2 hours", "2 hours", 
    "a few seconds", "6 minutes"
]

# Convert and format each time description
formatted_times = [format_time(convert_to_seconds(time)) for time in time_descriptions]

# Print formatted times
for original, formatted in zip(time_descriptions, formatted_times):
    print(f"Original: {original} => Formatted: {formatted}")
