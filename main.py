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
    <h1>Welcome!</h1>
"""
#html boilerplate for the bottom of every page
footer = """
</body>
</html>
"""

forminput = """
    <form method = "post">
        <table>
            <tbody>
                <tr>
                    <td>
                        <label for="username">Username:</label>
                    </td>
                    <td>
                        <input name="username" type="text"/>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="password">Password:</label>
                    </td>
                    <td>
                        <input name="password" type="password"/>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="verify">Verify Password:</label>
                    </td>
                    <td>
                        <input name="verify" type="password"/>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="email">Email (optional)</label>
                    </td>
                    <td>
                        <input name="email" type="email"/>
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

        error = self.request.get("error")

        response = header + forminput.format("") + footer
        self.response.write(response)

    def post(self):
        #looking inside the requests to see what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username,
                      email = email)


        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        new_username = "<strong>" + username + "</strong>"
        success = "Congratulations, " + new_username + ", your account is activated!"
        response = welcome + "<p>" + success + "</p>" + footer

        #if have_error:
        #    self.response.write(error)
        #else:
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Signup)
], debug=True)
