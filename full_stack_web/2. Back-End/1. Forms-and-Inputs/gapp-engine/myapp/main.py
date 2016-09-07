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
import webapp2
import cgi
# import validation.py

form="""
<form method="post">
    <h3>What is your birthday?</h3>
    <label> Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label> Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label> Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

def escape_html(s):
    s = cgi.escape(s, quote=True)
    return s

months = ['January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December']

def valid_month(month):
    m = month.capitalize()
    if m in months:
        return True
    else:
        return False
def valid_day(day):
    if day.isdigit():
        day = int(day)
    if day>=0 and day<=31:
        return True
    else:
        return False
def valid_year(year):
    if year.isdigit():
        year = int(year)
    if year>=1900 and year<=2020:
        return True
    else:
        return False


class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": month,
                                        "day": day,
                                        "year": year})

    def get(self):
        self.write_form()

    def post(self):
        rm = self.request.get('month')
        rd = self.request.get('day')
        ry = self.request.get('year')
        m = valid_month(rm)
        d = valid_day(rd)
        y = valid_year(ry)
        if not (m and d and y):
            self.write_form("Oops! error dude..", rm, rd, ry)
        else:
            self.redirect("/success")

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks!, you know your date well")
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/success', SuccessHandler)],
    debug=True)

