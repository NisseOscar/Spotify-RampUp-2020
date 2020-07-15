import numpy as np
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import RequestError


class SptfyApiHndler:
    """
        This is a Handler for the spotify Api which helps you use the API without weird HTTP requests.
    """
    def __init__(self):
        # Number of playlists sampled
        self.plylstLimit = 5
        # Number of tracks sampled from each playlist
        self.tracksLimit = 8
        # Properties of interest
        self.properties = ['acousticness',
                            'danceability',
                            'energy',
                            'instrumentalness',
                            'liveness',
                            'tempo',
                            'valence']

    """
        Searches Spotify for playlists based on a search word and returns a list of playlists limited to plylstLimit

        Args:
            word(str): The word to be searched.
            clientID(str): The clientID of the application.
            tkn(str): the spotity token.
        returns:
            playlists(lst): a list of playlist references.
        throws:
            RequestError if the API-call fails.
    """
    def search(self,word,clientID,tkn):
        req = requests.get( 'https://api.spotify.com/v1/search',
                                headers={ 'authorization': "Bearer " + tkn },
                                params={ 'q': word, 'type': 'playlist', 'limit': self.plylstLimit })
        if req.status_code != 200:
            raise RequestError(req.status_code)
        req_Json = req.json()
        playlists = req_Json['playlists']['items']
        if None in playlists:
            raise RequestError('To few playlists')
        return playlists

    """
        Gets a list of tracks from samples from a list of playlists limited to the tracksLimit.

        args:
            playlsts(lst): A list of playlists
            clientID(str): The clientID of the application.
            tkn(str): the spotity token.
        returns:
            tracklst(lst): a list of tracks.
        throws:
            RequestError if the API-call fails.
    """
    def getPlaylstTracks(self,playlsts,clientID,tkn):
        tracklst = []
        for playlst in playlsts:
            id = playlst['id']
            req = requests.get( "https://api.spotify.com/v1/playlists/"+id+"/tracks?fields=items(track(id))&limit="+str(self.tracksLimit),
                                    headers={ 'authorization': "Bearer " + tkn })
            if req.status_code != 200:
                raise RequestError(req.status_code)
            req_json = req.json()
            tracklst  = tracklst + [track['track']['id'] for track in req_json['items']]
        if None in tracklst:
            raise RequestError('To few tracks')
        return tracklst

    """
        Gets a pandas DataFrame of song properties from a list of tracks

        args:
            trakcs(lst): a list of trackIDs
            clientID(str): The clientID of the application.
            tkn(str): the spotity token.
        returns:
            props(DataFrame): a DataFrame of song properties
        throws:
            RequestError if the API-call fails.
    """
    def getTrackProperties(self,tracks,clientID,tkn):
        trackStr = "%2C".join(tracks)
        req = requests.get("https://api.spotify.com/v1/audio-features?ids="+trackStr,
                            headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            raise RequestError(req.status_code)
        req_json = req.json()
        props = req_json["audio_features"]
        if None in props:
            raise RequestError('Tracks are missing properties')
        props = pd.DataFrame.from_dict(props)
        return props


## Här testar vi grejer
if __name__ == '__main__':
    fltr = SptfyApiHndler()
    word = 'winter'
    clientID = '61ce90c9bfa841419ef3d34d439c3a42'
    tkn = "BQCJaP4jNEP5RIPszVpwAWz6FRyHj4Lfr1LnMqjmeKz5dwUy26tgjoQaWVI2ZgYIGov8rvrmUzjv7ucZ7BY1bAIZd85K4pySKOSr4iokXC9tZqv3DQT0L-qBonNsaZ-xw8Jcbyq4GhfpT53rFfsMaFB5LYaV9ksUkZQ5u7EnfHwY59WPLQvyov_BuEW8i_-AmWDHokdd41eED9fG0tT3ISxlY89Fn73J0e73TwGx0ihsu_pumtqajglp4fU"
    playlsts = fltr.search(word,clientID, tkn)
    playlstsTracks = fltr.getPlaylstTracks(playlsts,clientID,tkn)
    trackProps = fltr.getTrackProperties(playlstsTracks,clientID,tkn)
    print(trackProps)

    i=0
    for prop in fltr.properties:
        ax = plt.subplot(241+i)
        i=i+1
        if(prop == 'tempo'):
            ax.hist(trackProps[prop], density=True, bins=20)
        else:
            ax.hist(trackProps[prop], density=True, bins=20,range=(0,1))
        ax.set_xlabel(prop)

    plt.show()
