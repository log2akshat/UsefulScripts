import wikipedia as wiki

page_content = wiki.page("Jupiter").content
print(page_content)

search_results = wiki.search("Mars")
print(search_results)
