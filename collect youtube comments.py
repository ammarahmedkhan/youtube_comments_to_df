# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 21:43:51 2018

@author: DELL inspiron
"""

"""
The features / values i get are the following
authorChannelId
authorChannelUrl
authorDisplayName
authorProfileImageUrl
canRate
likeCount
publishedAt
textDisplay
textOriginal
updatedAt
"""

#the goodies
import json
import pandas as pd
import requests
"""
the video id used is of the song
Tonic - You Wanted More - gr8 song!
"""
"""
the whole youtube api`s URL taken apart into
relevant substrings that where can pass in our
values
"""
base = "https://www.googleapis.com/youtube/v3/commentThreads?"
api_key="<YOUR-API-KEY>"
format_snipp = "textFormat=plainText&part=snippet"
videoId="videoId=z04VDnr5k4I" 
extra="maxResults=50"
nextPageToken=""


"""
the features we can get from the api,
although theres not much we can get except
comment date and the comment text itself, i 
thought I`d add all and you can keep what you
like
"""

authorChannelId=[]
authorChannelUrl=[]
authorDisplayName=[]
authorProfileImageUrl=[]
canRate=[]
likeCount=[]
publishedAt=[]
textDisplay=[]
textOriginal=[]
updatedAt=[]
#videoId=[]
#viewerRating=[]

"""
this is for the latest 100 comments.
for more comments, you can increase the 
value of n.
alternatively you can use ,
while(nextPageToken)    
    nextPageToken = "nextPageToken" in json_file.keys()
    <....rest of the code ....>

in place
of the for loop to get ALL the comments.
"""
n = 2
for i in range(n):
#on first call of the api, we get the nextpagetoken
#on subsequent calls, we dont.so we create the calling
#url accordingly.
    if i == 1:
        url = "&".join([api_key,format_snipp,videoId,extra])
    else:
        url = "&".join([api_key,nextPageToken,format_snipp,videoId,extra])
    

        url = "".join([base,url])
#call the api        
        r=requests.get(url)
        text=r.text
        json_file=json.loads(text)
#iterate through the items and extract your data.        
    for a in json_file['items']:
        authorChannelId.append(a["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
        authorChannelUrl.append(a["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"])
        authorDisplayName.append(a["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
        authorProfileImageUrl.append(a["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"])
        canRate.append(a["snippet"]["topLevelComment"]["snippet"]["canRate"])
        likeCount.append(a["snippet"]["topLevelComment"]["snippet"]["likeCount"])
        publishedAt.append(a["snippet"]["topLevelComment"]["snippet"]["publishedAt"])
        textDisplay.append(a["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
        textOriginal.append(a["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
        updatedAt.append(a["snippet"]["topLevelComment"]["snippet"]["updatedAt"])
    #if theres any next page token
    nextPageToken = json_file["nextPageToken"]
    nextPageToken = "nextPageToken=" + nextPageToken
    

    
#save the results to a dictionary.
df_dict=        {
                'authorChannelId' : authorChannelId,
                'authorChannelUrl' : authorChannelUrl ,
                'authorDisplayName' : authorDisplayName, 
                'authorProfileImageUrl' : authorProfileImageUrl,
                'canRate' : canRate,
                'likeCount' : likeCount,
                'publishedAt' : publishedAt,
                'textDisplay' : textDisplay,
                'textOriginal' : textOriginal,
                'updatedAt' : updatedAt,
#                'videoId' : videoId,
#                'viewerRating' : viewerRating
                }
#save the dictionary to a df.
df=pd.DataFrame(
        data=df_dict
        )
#convert the date-time features to pandas date-time.
df['publishedAt'] = pd.to_datetime(df['publishedAt'])
df['updatedAt'] = pd.to_datetime(df['updatedAt'])

