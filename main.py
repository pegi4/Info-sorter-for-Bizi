import gspread

gc = gspread.service_account(filename="creds.json")

sh1 = gc.open("HoseMilano-stranke").get_worksheet(0)

# Read data from data.txt and structure it
with open('data.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file.readlines() if line.strip()]  # Also remove empty lines

data = []

index = 0

def is_phone(s):
    # More than 5 digits and no alphabetical characters should suffice for our use case
    return len([c for c in s if c.isdigit()]) > 5 and not any(c.isalpha() for c in s)

while index < len(lines):
    # Init variables for each dataset with default values
    name, region, phone, email, website = '-', '-', '-', '-', '-'

    # Check for 'Oglas' and skip the line if found
    if "Oglas" in lines[index]:
        index += 1
        continue 

    # First line is always a name
    name = lines[index]
    #print(f"DEBUG: Name: {name}")  # Debugging print
    index += 1

    # Second line is always a region
    if index < len(lines):
        region = lines[index]
        #print(f"DEBUG: Region: {region}")  # Debugging print
        index += 1

    # Check if current line contains a phone number
    if index < len(lines) and is_phone(lines[index]):
        phone = lines[index]
        #print(f"DEBUG: Phone: {phone}")  # Debugging print
        index += 1

    # Check if current line contains an email
    if index < len(lines) and "@" in lines[index]:
        email = lines[index].replace(" @", "@").replace("@ ", "@").replace(" .", ".").replace(". ", ".").replace("- ", "-").replace(" -", "-").replace("_ ", "-").replace(" _", "-")
        #print(f"DEBUG: Email: {email}")  # Debugging print
        index += 1

    # Check if current line contains a website
    if index < len(lines) and ("http" in lines[index] or "https" in lines[index]):
        website = lines[index].replace(" .", ".").replace(". ", ".").replace(" /", "/").replace("/ ", "/").replace("- ", "-").replace(" -", "-")
        #print(f"DEBUG: Website: {website}")  # Debugging print
        index += 1

    # Append the structured data to the list
    data.append([name, region, phone, email, website])
    

#--------WRITE---------#

# Determine the first empty row in the worksheet
first_empty_row = len(sh1.get_all_values()) + 1

# Start in B column
range_to_insert = f'B{first_empty_row}:F{first_empty_row + len(data) - 1}'

# Write the structured data to the specified range
sh1.update(range_to_insert, data)

print("\033[92mData inserted into Google Sheet.\033[0m")
#print(data)