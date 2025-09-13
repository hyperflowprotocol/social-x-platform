#!/usr/bin/env python3
"""Script to fix the social_trading_platform.py file by removing orphaned HTML/JS code."""

with open('social_trading_platform.py', 'r') as f:
    lines = f.readlines()

# Find the end of generate_base_html_start (around line 1870)
# and the start of generate_markets_page (around line 2101)
new_lines = []
skip_mode = False
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if we just finished generate_base_html_start
    if i > 0 and 'script src="/static/wallet-connect.js"' in lines[i-1] and '"""' in lines[i-1]:
        new_lines.append(line)  # Keep the current line
        # Skip everything until we find the next proper function definition
        skip_mode = True
    elif skip_mode and line.strip().startswith('def generate_markets_page'):
        skip_mode = False
        new_lines.append(line)
    elif not skip_mode:
        new_lines.append(line)
    
    i += 1

# Write the fixed file
with open('social_trading_platform.py', 'w') as f:
    f.writelines(new_lines)

print("File fixed! Removed orphaned HTML/JavaScript code.")