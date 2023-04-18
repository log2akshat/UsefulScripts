import wikipedia as wiki

print("Please select from the menu what you want to do..")
print("Option 1: Type 1 if you want the content from the wiki for the specified keyword")
print("Option 2: Type 2 if you want to search the content in the wiki for the specified keyword")
selected_option=input("Please select your option: ")

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
