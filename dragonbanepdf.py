import json
import csv
from fillpdf import fillpdfs

def main():

# FIX ADULT MERCHANT, SHOULD HAVE DONKEY

# Path to your CSV file
    file_path = 'dragonbane.csv'
    in_pdf  = 'DB-Prefilled'
    #in_pdf = 'Cello.pdf'

    weapon_properties = {
        "BL": "Bludgeoning",
        "PC": "Piercing",
        "SL": "Slashing",
        "SB": "Subtle",
        "TH": "Thrown",
        "TP": "Toppling",
        "NP": "No Parry",
        "LG": "LG",
        "RM": "Requires Mount",
        "TN": "Tiny",
        "QV": "Quiver",
        "ND": "No damage bonus"
    }

    fields = {
	"string": [
        "Kin", "Age", "Profession", "Weakness", "Appearance",
        "STR", "CON", "AGL", "INT", "WIL", "CHA",
        "STR bonus", "AGL bonus", "Movement", "Silver", "Memento", "Enc limit",
        "1 Equipment", "2 Equipment", "3 Equipment", "4 Equipment", "5 Equipment", "6 Equipment",
        "7 Equipment", "8 Equipment", "9 Equipment", "10 Equipment", "11 Equipment", "12 Equipment",
        "SecondarySkillName_0",
        "Abilities + Spells", "Additional Information", "Tiny Items",
        "1 weapon", "1 grip", "1 range", "1 damage", "1 durability", "1 features",
        "2 weapon", "2 grip", "2 range", "2 damage", "2 durability", "2 features",
        "3 weapon", "3 grip", "3 range", "3 damage", "3 durability", "3 features",
        "Armor name", "Armor value", "Helmet name", "Helmet value", "WP", "HP"
	],
    'skills' : ["Axes", "Bows", "Brawling", "Crossbows", "Hammers", "Knives", "Slings", "Spears", "Staves", "Swords",
        "Acrobatics", "Awareness", "Bartering", "BeastLore", "Bluffing", "Bushcraft", "Crafting", "Evade",
        "Healing", "HuntingAndFishing", "Languages", "MythsAndLegends", "Performance", "Persuasion", "Riding",
        "Seamanship", "SleightOfHand", "Sneaking", "SpotHidden", "Swimming", "SecondarySkill_0"],
	"checks": [
        "SneakBaneMark", "EvadeBaneMark", "AcrobaticsBaneMark", "BackpackMark", "AwarenessBaneMark", "RangedBaneMark",
        "WP_0", "WP_1", "WP_2", "WP_3", "WP_4", "WP_5", "WP_6", "WP_7", "WP_8", "WP_9","WP_10",
        "WP_11", "WP_12", "WP_13", "WP_14", "WP_15", "WP_16", "WP_17", "WP_18", "WP_19",
        "HP_0", "HP_1", "HP_2", "HP_3", "HP_4", "HP_5", "HP_6", "HP_7", "HP_8", "HP_9", "HP_10",
        "HP_11", "HP_12", "HP_13", "HP_14", "HP_15", "HP_16", "HP_17", "HP_18", "HP_19"
	]
}
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        # Create a DictReader object
        reader = list(csv.DictReader(file))
    for row in reader:
        # Set the checkbox values to True or Fales
        for checkbox in fields['checks']:
            if checkbox in row and row[checkbox] == 'X':
                row[checkbox] = 'Yes'
            else:
                row[checkbox] = 'Off'

        # Fix Age
        row['Age'] == row['Age'].capitalize()

        # Check for weapon notes to add details on abbreviations
        weaponNotes = set()
        for abbrev,details in weapon_properties.items():
            for feature in [ '1 features', '2 features', '3 features' ]:
                if feature in row and abbrev in row[feature]:
                    weaponNotes.add(f'{abbrev}: {details}')
        
        # Now check for bane notes
        for skill in fields['skills']:
            if '†' in row[skill]:
                weaponNotes.add(f'†: Bane on roll due to armor')
            if '‡' in row[skill]:
                weaponNotes.add(f'‡: Bane on ranged attacks due to helmet.')

        # Insert a line break in Weakness
        row['Weakness'] = row['Weakness'].replace('. ','.\n')

        if len(row['Additional Information']) > 0:
            info = row['Additional Information'].split('\n')
        else:
            info = []

        if len(list(weaponNotes)) > 0:
            info.extend(sorted(list(weaponNotes)))
        
        row['Additional Information'] = get_formatted_info(info)

        # Strip leading/trailing space
        for k,v in row.items():
            if isinstance(v,str):
                row[k] = v.strip()
        this_in_pdf = f'{in_pdf}-{row["Age"]}.pdf'
        #print(json.dumps(row,indent=2))
        out_pdf = row['Profession'] + '_' + row['Kin'] + '_' + row['Age'] + '.pdf'
        fill_pdf(this_in_pdf,out_pdf,row)
       
def fill_pdf(in_pdf,out_pdf,data):
    fields = fillpdfs.get_form_fields(in_pdf)
    print(json.dumps(fields,indent=2))
    fillpdfs.write_fillable_pdf(in_pdf, out_pdf, data)
    return

def get_formatted_info(data):
    # Pad the list to ensure the first column is always 3 items long
    data += [''] * (3 - len(data) % 3) if len(data) % 3 != 0 else []

    # Split the list into chunks of 3 items each
    chunks = [data[i:i+3] for i in range(0, len(data), 3)]

    # Format each chunk into rows and columns
    formatted_chunks = []
    for chunk in chunks:
        # Find the length of the longest item in the first column
        max_length = max(len(item) for item in chunk)
        
        rows = []
        for item in chunk:
            # Calculate padding for the second column based on the longest item in the first column
            padding = max_length + 2
            row = f'{item:<{padding}}'  # Left-align each item with padding
            rows.append(row)
        formatted_chunks.append(rows)

    # Transpose the rows to columns
    columns = zip(*formatted_chunks)

    # Join the columns into rows
    result = '\n'.join([' '.join(column) for column in columns])
    
    
    return (result)

if __name__ == "__main__":
    main()