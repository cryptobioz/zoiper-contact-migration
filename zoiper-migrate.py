#!/usr/bin/env python

import sqlite3, argparse
from lxml import etree

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--from", dest="from_file", help="Old Zoiper contact file", metavar="FILE", required=True)
parser.add_argument("-t", "--to", dest="to_file", help="New Zoiper contact file", metavar="FILE", required=True)

args = parser.parse_args()

db = sqlite3.connect(args.to_file)

tree = etree.parse(args.from_file)
for contact in tree.xpath("/contacts/contact"):
    cursor = db.cursor()

    contact_display = contact.xpath("display")[0].text

    # Create Contact
    print "[*] Creating contact: '%s'..." % contact_display
    cursor.execute("INSERT INTO Contact DEFAULT VALUES")
    
    # Retrieve generate Contact ID
    contact_id = cursor.lastrowid

    # Create Name
    print "[*] Importing basic informations..."
    flag = 1
    title = ""
    first = contact.xpath("first_name")[0].text
    middle = contact.xpath("middle_name")[0].text
    last = contact.xpath("last_name")[0].text
    display = contact_display

    cursor.execute("INSERT INTO Name VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (contact_id, flag, title, first, middle, last, display))

    # Create Info
    print "[*] Importing personnal informations..."
    gender = 1
    company = None
    position = None
    profession = None
    hidden = None

    cursor.execute("INSERT INTO Info Values (NULL, ?, ?, ?, ?, ?, ?)", (contact_id, gender, company, position, profession, hidden))

    # Create Phone (home_phone)
    print "[*] Importing home's phone number..."
    phone_type = 8
    phone = contact.xpath("home_phone")[0].text
    normal = phone
    
    cursor.execute("INSERT INTO Phone Values (NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (contact_id, phone_type, phone, normal))
 
    # Create Phone (work_phone)
    print "[*] Importing work's phone number..."
    phone_type = 8
    phone = contact.xpath("work_phone")[0].text
    normal = phone
    
    cursor.execute("INSERT INTO Phone Values (NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (contact_id, phone_type, phone, normal))

   
    # Create Phone (cell_phone)
    print "[*] Importing cell phone number..."
    phone_type = 16
    phone = contact.xpath("cell_phone")[0].text
    normal = phone
    
    cursor.execute("INSERT INTO Phone Values (NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (contact_id, phone_type, phone, normal))
  
    # Create Phone (mail)
    print "[*] Importing email address..."
    phone_type = 4
    phone = contact.xpath("mail")[0].text
    normal = phone
    
    cursor.execute("INSERT INTO Phone Values (NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (contact_id, phone_type, phone, normal))

    # Create Phone (fax_number)
    print "[*] Importing fax number..."
    phone_type = 32
    phone = contact.xpath("fax_number")[0].text
    normal = phone
    
    cursor.execute("INSERT INTO Phone Values (NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", (contact_id, phone_type, phone, normal))

    db.commit()

    print "[+] '%s' successfully imported." % contact_display

db.close()
