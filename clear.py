#!/usr/bin/python
import cgi
import cgitb
import sqlite3
cgitb.enable()

def clear(group_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("update entries set pending=0 where group_id=?", (group_id,))
    conn.commit()

form = cgi.FieldStorage()
message = ''
group_id = form.getfirst("who")
if group_id:
    clear(group_id)
else:
    message = "No group id provided for entry clearing."

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
