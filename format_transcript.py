#!/usr/bin/env python3
import re
from datetime import datetime, timedelta

def add_time_to_timestamp(timestamp_str, hours=6, minutes=24):
    """Add specified hours and minutes to a timestamp in [HH:MM:SS] format"""
    # Extract hours, minutes, seconds from timestamp
    match = re.match(r'\[(\d{2}):(\d{2}):(\d{2})\]', timestamp_str)
    if not match:
        return timestamp_str
    
    h, m, s = map(int, match.groups())
    
    # Create datetime object (using arbitrary date)
    dt = datetime(2024, 1, 1, h, m, s)
    
    # Add the time
    dt += timedelta(hours=hours, minutes=minutes)
    
    # Format back to [HH:MM:SS]
    return f"[{dt.strftime('%H:%M:%S')}]"

def process_transcript(input_file, output_file):
    """Process transcript file according to formatting rules"""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    processed_lines = []
    previous_speaker = None
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Check if line starts with timestamp
        timestamp_match = re.match(r'^(\[\d{2}:\d{2}:\d{2}\])', line)
        
        if timestamp_match:
            # Extract timestamp and the rest of the line
            timestamp = timestamp_match.group(1)
            rest_of_line = line[len(timestamp):].strip()
            
            # Extract speaker name (everything before the first colon)
            speaker_match = re.match(r'^([^:]+):', rest_of_line)
            current_speaker = speaker_match.group(1) if speaker_match else None
            
            # Add line break between different speakers
            if previous_speaker and current_speaker and previous_speaker != current_speaker:
                processed_lines.append("")
            
            # Add time to timestamp
            new_timestamp = add_time_to_timestamp(timestamp)
            
            # Create new line with updated timestamp as a dash list item
            processed_line = f"- {new_timestamp} {rest_of_line}"
            processed_lines.append(processed_line)
            
            previous_speaker = current_speaker
        else:
            # Non-timestamp lines - add as separate dash list items
            processed_lines.append(f"- {line}")
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in processed_lines:
            f.write(line + '\n')
    
    print(f"Processed {len(processed_lines)} lines")
    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "LATE NIGHT N WORD DEBATE_v2.md"
    output_file = "LATE NIGHT N WORD DEBATE_v2_formatted.md"
    
    process_transcript(input_file, output_file)