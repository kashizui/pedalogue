#!/usr/bin/python
import sqlite3
import cgi, cgitb
cgitb.enable()

def delete_entry():
    entry_id = int(form.getfirst("entry"))
    c = conn.cursor()
    c.execute("delete from entries where id=?", (entry_id,))

def delete_group():
    group_id = int(form.getfirst("group"))
    c = conn.cursor()
    c.execute("update groups set active=0 where id=?", (group_id,))

def main():
    global message
    if form.getfirst("entry"):
        delete_entry()
    elif form.getfirst("group"):
        delete_group()
    else:
        message = "Invalid form submission."

conn = sqlite3.connect("data.db")
form = cgi.FieldStorage()
message = ''
main()
conn.commit()
print "Content-Type: text/html"
print 
print """<html>
 <head>
  <title>submission</title>
 </head>
 <body>
 <form action="index.py" method="post" id="message">
 <input type="hidden" name="message" value="%s" />
 </form>
 <script type="text/javascript">
 document.getElementById("message").submit()
 </script>
 </body>
</html>
""" % message
