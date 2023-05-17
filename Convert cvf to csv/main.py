import re
from urllib import parse
import quopri
import csv


# vCard data
with open('vcard.vcf', 'r') as file:
    vcard_data = file.read()

# Regular expression patterns for extracting data
name_pattern = re.compile(r'FN:(.*)')
name_pattern_UTF8 = re.compile(r'FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:(.*)')
tel_home_pattern = re.compile(r'TEL[^:]*:(.*)')
tel_cell_pattern = re.compile(r'TEL[^:]*:(.*)')
email_pattern = re.compile(r'EMAIL:(.*)')
note_pattern = re.compile(r'NOTE:(.*)')


# Define a function to format a vCard block
def create_vcard(name, tel_home, tel_cell, email, note):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nTEL;HOME:{tel_home}\nTEL;CELL:{tel_cell}\nEMAIL:{email}\nNOTE:{note}\nEND:VCARD\n"
    return vcard

# Function to decode encoded values
def decode(encoded_string, encoding):
    decoded_string = parse.unquote(encoded_string)
    return decoded_string.encode(encoding).decode('utf-8')

# Split vCard data into individual entries
vcards = vcard_data.strip().split('END:VCARD')

# Create a CSV file to save extracted data
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Home Telephone', 'Cell Phone', 'Email', 'Note'])

    # Process each vCard entry and save extracted data in CSV file
    for vcard in vcards:
        try:
            # Extract name
            name_match = name_pattern.search(vcard)
            name_match_UTF8 = name_pattern_UTF8.search(vcard)
            if name_match:
                name = decode(name_match.group(1), 'utf-8')
            elif name_match_UTF8:
                dados_codificados = name_match_UTF8.group(1)
                # Decode encoded string using QUOTED-PRINTABLE
                name = quopri.decodestring(dados_codificados.encode('utf-8')).decode('utf-8')
            else:
                name = ""

            # Extract telephone numbers
            tel_home_match = tel_home_pattern.search(vcard)
            tel_cell_match = tel_cell_pattern.search(vcard)
            if tel_home_match:
                tel_home = tel_home_match.group(1)
            else:
                tel_home = ""
            if tel_cell_match:
                tel_cell = tel_cell_match.group(1)
            else:
                tel_cell = ""

            # Extract email
            email_match = email_pattern.search(vcard)
            if email_match:
                email = email_match.group(1)
            else:
                email = ""

            # Extract note
            note_match = note_pattern.search(vcard)
            if note_match:
                note = decode(note_match.group(1), 'latin-1')
            else:
                note = ""
              
            # Write extracted data to CSV file
            if name.find("/") != -1:
               name = re.sub(r'[<>:"/\\|?*]', "_", name)

            # Write extracted data to CSV file
            writer.writerow([name, tel_home, tel_cell, email, note])

           

            # Check if the name is blank
            if name.strip() == "":
                continue

            if name.strip():
            # Modificar o nome do arquivo para remover caracteres inválidos
             name = re.sub(r'[<>:"/\\|?*]', "_", name)

             

            # Create the vCard block
            vcard_block = create_vcard(name, tel_home, tel_cell, email, note)

           # Write the vCard block to the output file
            with open(f"Contatos/{name}.vcf", 'w') as vcf_file:
                vcf_file.write(vcard_block)
                

      

      

        except UnicodeDecodeError:
            print("Error: Unable to decode data in vCard entry.")


