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
# import validation.py

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
        return m
    else:
        return None

def valid_day(day):
  if day.isdigit():
    day = int(day)
    if day>=0 and day<=31:
      return day
  else:
    return None

def valid_year(year):
  if year.isdigit():
    year = int(year)
    if year>=0 and year<=31:
      return year
  else:
    return None

form="""
<form method="post">
    <h3>What is your birthday?</h3>
    <label> Month
        <input type="text" name="month">
    </label>
    <label> Day
        <input type="text" name="day">
    </label>
    <label> Year
        <input type="text" name="year">
    </label>
    <br>
    <br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form)

    def post(self):
        m = valid_month(self.request.get('month'))
        d = valid_day(self.request.get('day'))
        y = valid_year(self.request.get('year'))
        if not (m and d and y):
            self.response.out.write(form)
        else:
            self.response.out.write("Thanks!, you know your date well")

app = webapp2.WSGIApplication([
    ('/', MainPage)],
    debug=True)

