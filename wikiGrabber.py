import wikipedia

page_content = wikipedia.page("Jupiter").content
print(page_content)

search_results = wikipedia.search("Mars")
print(search_results)
