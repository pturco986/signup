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



#the class defines what we intend to do
class Signup(webapp2.RequestHandler):
    def get(self):

        error = self.request.get("error")

        response = header + forminput.format("") + footer
        self.response.write(response)

    def post(self):
        #looking inside the requests to see what the user typed
        username = self.request.get("username")
        escape_username = cgi.escape(username, quote=True)
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if username == "":
            usererror ="You did not input anything".format(username)
            usererror_escaped = cgi.escape(usererror, quote=True)
            self.redirect("/?usererror=" + error_escaped)

        new_username = "<strong>" + escape_username + "</strong>"
        success = "Congratulations, " + new_username + ", your account is activated!"
        response = header + "<p>" + success + "</p>" + footer

        self.response.write(response)



app = webapp2.WSGIApplication([
    ('/', Signup)
], debug=True)
