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
    print(selected_option)
