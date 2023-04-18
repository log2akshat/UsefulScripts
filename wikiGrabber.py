#    Copyright (C) <2023>  <Akshat Singh>
#    <akshat-pg8@iiitmk.ac.in>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/bin/python

import wikipedia as wiki

print("Please select from the menu what you want to do.")
print("Please type 1 if you want to receive content from the wiki for the specified keyword")
print("Please type 2 if you want to search the content in the wiki for the specified keyword")
selected_option=input("Please enter your choice: ")

if (selected_option == str(1)):
    page_content=input("Please enter the content you want from the wiki from the wiki: ")
    grab_page_content = wiki.page(page_content).content
    print(grab_page_content)
elif (selected_option == str(2)):
    search_page_content=input("Please enter the content you want to search in the wiki: ")
    search_results = wiki.search(search_page_content)
    print(search_results)
else:
    print("Please select a valid option")
