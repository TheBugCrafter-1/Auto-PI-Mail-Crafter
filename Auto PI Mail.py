from pathlib import Path
import shutil
import re
import os
import webbrowser
import urllib.parse

# ======================================================
# CHANGE THESE ONLY ONCE
# ======================================================

PI_ROOT = Path(r"C:\Users\tushar\OneDrive\Order Management\Poforma invoice\2026-2027")

TO_EMAIL = "ashishberiy@gmail.com"

CC_EMAIL = "ashishberiya11@gmail.com"

FINANCIAL_YEAR = "2026-27"

# ======================================================

DESKTOP = Path.home() / "Desktop"
OUTPUT = DESKTOP / "Today's_PI"

print("=" * 60)
print("         PI MAIL AUTOMATION")
print("=" * 60)

pi_input = input("\nEnter PI Numbers (Example: P80,P81,P82): ")

# -----------------------------
# Create Output Folder
# -----------------------------

OUTPUT.mkdir(exist_ok=True)

# Delete old PDFs

for file in OUTPUT.glob("*.pdf"):
    file.unlink()

# -----------------------------
# Read User Input
# -----------------------------

requested = []

for item in pi_input.split(","):

    item = item.strip().upper()

    numbers = re.findall(r"\d+", item)

    if numbers:
        requested.append(int(numbers[0]))

requested = list(dict.fromkeys(requested))

found = []
not_found = []
mail_pi = []

# -----------------------------
# Search & Copy
# -----------------------------

for number in requested:

    copied = False

    # Example folder : 080
    folder = PI_ROOT / f"{number:03d}"

    if folder.exists():

        pdfs = list(folder.glob("*.pdf"))

        if pdfs:

            for pdf in pdfs:

                shutil.copy2(pdf, OUTPUT / pdf.name)

                found.append(pdf.name)

                mail_pi.append(f"PI-{number}/{FINANCIAL_YEAR}")

                copied = True

    # Search root if folder not found
    if not copied:

        for pdf in PI_ROOT.glob("*.pdf"):

            filename = pdf.stem.upper().replace("-", "")

            if f"PI{number}" in filename:

                shutil.copy2(pdf, OUTPUT / pdf.name)

                found.append(pdf.name)

                mail_pi.append(f"PI-{number}/{FINANCIAL_YEAR}")

                copied = True

                break

    if not copied:

        not_found.append(number)

# -----------------------------
# Gmail Subject
# -----------------------------

subject = "Proforma Invoice for " + ", ".join(mail_pi)

# -----------------------------
# Gmail Body
# -----------------------------

body = f"""Dear Sir,

Please find attached the following Proforma Invoices for your reference.

{chr(10).join('• ' + x for x in mail_pi)}

Kindly review the same.

Regards,
Ashish
"""

# -----------------------------
# Gmail Draft
# -----------------------------

params = urllib.parse.urlencode({

    "view": "cm",

    "fs": "1",

    "to": TO_EMAIL,

    "cc": CC_EMAIL,

    "su": subject,

    "body": body

})

url = "https://mail.google.com/mail/?" + params

webbrowser.open(url)

# -----------------------------
# Result
# -----------------------------

print("\n" + "=" * 60)

print("FOUND FILES")

print("=" * 60)

for file in found:
    print("✔", file)

if not_found:

    print("\nNOT FOUND")

    for n in not_found:
        print(f"✖ PI-{n}")

print("\nOpening Today's_PI Folder...")

os.startfile(OUTPUT)

print("\n✅ Gmail Draft Opened.")
print("✅ Today's_PI Folder Opened.")
print("Now attach all PDFs and click SEND.")