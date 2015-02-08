

import cgi, webapp2, string
html = """
<!DOCTYPE html>
<html>
<head>
<title> Rot 13 </title>
</head>
<body>
<h2> Enter some text to ROT13: </h2>
<form method="post">
<textarea name ="text" style = "height:200px; width:600px">%(encrypted)s</textarea>
<br>
<input type = "submit">
</form>
</body>
</html>
"""

lower = string.ascii_lowercase
upper = string.ascii_uppercase

def escape_html(s):
    return cgi.escape(s, quote = True)

def encrypt(s):
    def rot13(letter):
        if letter in lower:
            index = lower.find(letter)
            return lower[(index + 13) % 26]
        else:
            index = upper.find(letter)
            return upper[(index + 13) % 26]
    s = list(s)
    for x in range(0, len(s)):
        letter = s[x]
        if letter.isalpha():
            s[x] = rot13(letter)

    return "".join(s)

class MainHandler(webapp2.RequestHandler):
    def write_html(self, encrypted = ""):
        self.response.out.write(html % {"encrypted" : encrypted})
    def get(self):
        self.write_html()
    def post(self):
        text = self.request.get("text")
        self.write_html(escape_html(encrypt(text)))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
