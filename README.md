# Campaign-Coding

## Participant sourcing

Interface 1 accepts CSV, XLSX, TXT, JSON, text-based PDF, and DOCX contact lists.
Records need a recognizable first name, last name, and email address. Tabular
files should include name/email columns; plain-text documents should place a
person's name and email address on the same line. Scanned PDFs and image files
are not supported.

The app randomly selects up to 12 students, 5 faculty members, and 6 completed
participants from their respective uploaded lists. Declined candidates are
excluded from future draws and replaced when another eligible record exists.
Accepted participants are saved by group in the Participants subtab and included
in the app's JSON export.