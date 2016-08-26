#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
from string import letters

#html boiler for the top of every page
header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup-Form</title>
        <style type ="text/css">
        form{
        padding: 5px;
        }
        .error {
        color: red;
        }
        td {
        display: table-cell;
        vertical-align: inherit;
        }
    </style>
</head>
<body>
    <h1>Signup-Form</h1>
"""

welcome = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome-Page</title>
        <style type ="text/css">
        form{
        padding: 5px;
        }
        h1{
        text-align: center;
        }
        p{
        text-align: center;
        color: blue;
        }
    </style>
</head>
<body>
    <h1>Welcome {Username}!</h1>
"""
#html boilerplate for the bottom of every page
footer = """
</body>
</html>
"""

form = """
    <form action="/welcome" method = "post">
        <table>
            <tbody>
                <tr>
                    <td>
                        <label for="username">Username:</label>

                    </td>
                    <td>
                        <input name="username" type="text"/>
                        <td style="color: red"> {} </td>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="password">Password:</label>
                    </td>
                    <td>
                        <input name="password" type="password"/>
                        <td style="color: red"> {} </td>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="verify">Verify Password:</label>
                    </td>
                    <td>
                        <input name="verify" type="password"/>
                        <td style="color: red"> {} </td>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="email">Email (optional)</label>
                    </td>
                    <td>
                        <input name="email" type="email"/>
                        <td style="color: red"> {} </td>
                    </td>
                </tr>
            </tbody>
        </table>
    <input type="submit"/>
    </form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


#the class defines what we intend to do
class Signup(webapp2.RequestHandler):
    def get(self):

        name_error = self.request.get('name_error')
        name_error_element = '<p class = "error">' + name_error + '</p>' if name_error else ""

        pass_error = self.request.get('pass_error')
        pass_error_element = '<p class = "error">' + pass_error + '</p>' if pass_error else ""

        veri_error = self.request.get('veri_error')
        veri_error_element = '<p class = "error">' + veri_error + '</p>' if veri_error else ""

        email_error = self.request.get('email_error')
        email_error_element = '<p class = "error">' + email_error + '</p>' if email_error else ""

        self.response.write(header + form.format(name_error, pass_error, veri_error, email_error) + footer)

class Welcome(webapp2.RequestHandler):
    def post(self):
        error = ""
        #looking inside the requests to see what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if not valid_username(username):
            error = "name_error=Invalid username"

        if not valid_password(password):
            if error != "":
                error += "&"
            error += "pass_error=Invalid password"

        if not password == verify:
            if error != "":
                error += "&"
            error = "veri_error=Passwords do not match"

        if not valid_email(email):
            if error != "":
                error += "&"
            error += "email_error=Invalid email"

        username = cgi.escape(username)
        password = cgi.escape(password)
        verify = cgi.escape(verify)
        email = cgi.escape(email)

        if error != "":
            self.redirect("/?" + error)

        self.response.write(header + "Welcome " + username + footer)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
