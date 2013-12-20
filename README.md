Basic Python CGI scripts to help piano teachers keep track of their students, notes, and payments.

Installation
============
Copy the files into your cgi-bin and make sure all the Python scripts are executable.

    chmod 755 *.py

Run setup.sql through sqlite3 to create your database at data.db

    sqlite3 data.db < setup.sql

Point your browser to "index.py" and hopefully everything else is self-explanatory!
