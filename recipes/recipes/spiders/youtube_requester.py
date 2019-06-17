# from apiclient.discovery import build

# key = ""

# # build connection to youtube resource
# youtube = build("youtube", "v3", developerKey = key)

# # search videos for keyword "Rezept"
# request = youtube.search().list(q = "Rezept", part="snippet", type="video", maxResults=50)

# # execute http request
# result = request.execute()

# # get recipes info
# recipes = result["items"]

# # get titles
# for recipe in recipes:
#     print(f"title: {recipe['snippet']['title']} | \ndescription: {recipe['snippet']['description']}")

# # get title and description
# recipes_dict = {}

# for recipe in recipes:
#     # get video title
#     recipes_dict["title"] = recipe["snippet"]["title"]

#     # search for specific video id
#     video = youtube.videos().list(id=recipe["id"]["videoID"],part="snippet").execute()

#     # get video description
#     recipes_dict["description"] = video["items"]["snippet"]["description"]

#     # get video tags
#     recipes_dict["tags"] = video["items"]["snippet"]["tags"]

#     # get video channel
#     recipes_dict["channel"] = video["items"]["snippet"]["channelTitle"]

#     # get video category
#     recipes_dict["category"] = video["items"]["snippet"]["channelTitle"]

#     # get video url
#     recipes_dict["url"] = f"https://www.youtube.com/watch?v={video}"