# def open_git():
#     import requests
#     import webbrowser
    
#     url = "https://github.com/hxhkim"
#     response = requests.get(url)
#     if response.status_code == 200:
#         git_link = response.url
#         webbrowser.open(git_link)
#     else:
#         print("Failed to retrieve the GitHub page.")