Basic Python CGI scripts to help piano teachers keep track of their students, notes, and payments.
Used this myself for several months until I moved to http://www.musicteachershelper.com/

Screenshot:
![A look at the spartan interface.](http://www.stanford.edu/~sckoo/images/pedalogue-screenshot.png)

Installation
============
Copy the files into your cgi-bin and make sure all the Python scripts are executable.

    chmod 755 *.py

Run setup.sql through sqlite3 to create your database at data.db

    sqlite3 data.db < setup.sql

Point your browser to "index.py" and hopefully everything else is self-explanatory!
