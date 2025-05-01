import re

# Path to your C file
c_file_path = 'doom1.c'  # Change this to your actual C file name
output_file_path = 'doom1.giwad'

# Read the C file
with open(c_file_path, 'r') as f:
    c_content = f.read()

# Find the array content between the braces
match = re.search(r'doom_iwad\s*\[.*?\]\s*=\s*\{(.*?)\};', c_content, re.DOTALL)

if not match:
    raise ValueError("Could not find doom_iwad array in the C file.")

array_content = match.group(1)

# Split by commas and clean up
byte_strings = [byte.strip() for byte in array_content.split(',') if byte.strip()]

# Convert to actual byte values
byte_values = bytes(int(b, 16) for b in byte_strings)

# Write to binary file
with open(output_file_path, 'wb') as f:
    f.write(byte_values)

print(f"Successfully wrote {len(byte_values)} bytes to {output_file_path}")
