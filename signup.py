import cgi, webapp2, re

def escape_html(s):
    return cgi.escape(s, quote = True)

html = """
<!DOCTYPE html>
<html>
<head>
  <title> User Signup </title>
  <style type = "text/css">
  .label {text-align : right}
  .error {color : red}
  </style>
</head>
<body>
  <h2> Signup </h2>
  <form method = "post">
    <table>
      <tr>
        <td class = "label">
          Username
        </td>
        <td>
          <input type = "text" name = "username" value = "%(username)s">
        </td>
        <td class = "error">
            %(username_error)s
        </td>
      </tr>
      <tr>
        <td class = "label">
          Password
        </td>
        <td>
          <input type = "password" name = "password" value = "%(password)s">
        </td>
        <td class = "error">
            %(password_error)s
        </td>
      </tr>
      <tr>
        <td class = "label">
          Verify Password
        </td>
        <td>
          <input type = "password" name = "verify" value = "%(verify)s">
        </td>
        <td class = "error">
            %(verify_error)s
        </td>
      </tr>
      <tr>
        <td class = "label">
          Email (optional)
        </td>
        <td>
          <input type = "text" name = "email" value = "">
        </td>
        <td class = "error">
            %(email_error)s
        </td>
      </tr>
    </table>
    <input type = "submit">
  </form>
</body>
</html>
"""
username_r = r'^[a-zA-Z0-9_-]{3,20}$'
password_r = r'^.{3,20}$'
email_r = r'^[\S]+@[\S]+\.[\S]+$'

def valid_username(s):
    return re.match(username_r, s)


def valid_password(s):
    return re.match(password_r, s)


def valid_email(s):
    return re.match(email_r, s)


def valid_match(password, verify_password):
    return password == verify_password


class MainHandler(webapp2.RequestHandler):
    def write_html(self, username = "", password = "", verify = "", email = "", username_error = "", password_error = "", verify_error = "", email_error = ""):
        self.response.out.write(html % {"username" : username, "password" : password, "verify" : verify, "email" : email, "username_error" : username_error, "verify_error" : verify_error, "password_error" : password_error, "email_error" : email_error})
    def get(self):
        self.write_html()
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        password = "" if not valid_password(password) else password
        verify = self.request.get("verify")
        verify = "" if not valid_match(password, verify) else verify
        email = self.request.get("email")
        username_error = "" if valid_username(username) else "That's not a valid username."
        password_error = "" if valid_password(password) else "That wasn't a valid password."
        verify_error = "" if valid_match(password, verify) else "Your passwords didn't match."
        if verify_error != "":
            password = ""

        email_error = "" if valid_email(email) or email == "" else "That's not a valid email."
        error = False
        error = (username_error != "") or (password_error != "") or (verify_error != "") or (email_error != "")
        if error:
            self.write_html(username, password, verify, email, username_error, password_error, verify_error, email_error)
        else:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("<h2> Welcome, " + username + "!</h2>")




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
