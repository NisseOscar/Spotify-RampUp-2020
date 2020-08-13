import numpy as np
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from .RequestError import RequestError
from sklearn.neighbors import NearestNeighbors

class SptfyApiHndler:
    """
        This is a Handler for the spotify Api which helps you use the API without weird HTTP requests.
    """
    def __init__(self):
        # Number of playlists sampled
        self.plylstLimit = 5
        # Number of tracks sampled from each playlist
        self.tracksLimit = 10
        # Properties of interest
        self.properties = ['acousticness',
                            'danceability',
                            'energy',
                            'instrumentalness',
                            'liveness',
                            'tempo',
                            'valence']
        self.n_neighbors = 5
        self.threshold = 5

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
        if None in playlsts:
            raise RequestError('To few playlists')
        for playlst in playlsts:
            id = playlst['id']
            req = requests.get( "https://api.spotify.com/v1/playlists/"+id+"/tracks?fields=items(track(id))&limit="+str(self.tracksLimit),
                                    headers={ 'authorization': "Bearer " + tkn })
            if req.status_code != 200:
                raise RequestError(req.status_code)
            req_json = req.json()
            tracklst  = tracklst + [track['track']['id'] for track in req_json['items'] if track['track']!=None]
        if None in tracklst:
            raise RequestError('To few tracks')
        return tracklst

    def getAllPlaylstTracks(self,playlsts,clientID,tkn):
        tracklst = []
        for id in playlsts:
            i=0
            tmp_tracklist = []
            while(i==len(tmp_tracklist)):
                req = requests.get("https://api.spotify.com/v1/playlists/"+id+"/tracks?fields=items(track(id))&limit="+"50"+"&offset="+str(i),
                                    headers={ 'authorization': "Bearer " + tkn })
                if req.status_code != 200:
                    raise RequestError(req.status_code)
                req_json = req.json()
                tmp_tracklist  = tmp_tracklist + [track['track']['id'] for track in req_json['items'] if track['track']!=None]
                i = i+50
            tracklst = tracklst+tmp_tracklist
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
        batch_size = 25
        batches = [tracks[i:(i+batch_size)] for i in range(0,len(tracks),batch_size)]
        props = []
        for batch in batches:
            trackStr = "%2C".join(batch)
            req = requests.get("https://api.spotify.com/v1/audio-features?ids="+trackStr,
                                headers={ 'authorization': "Bearer " + tkn })
            if req.status_code != 200:
                print(req)
                raise RequestError(req.status_code)
            req_json = req.json()
            props = props + req_json["audio_features"]
        if None in props:
            raise RequestError('Tracks are missing properties')
        props = pd.DataFrame.from_dict(props)
        return props

    def getUserPlaylist(self,clientID,tkn):
        req = requests.get("https://api.spotify.com/v1/me/playlists?limit=5",
                            headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            raise RequestError(req.status_code)
        req_Json = req.json()
        playlists = req_Json['items']
        if None in playlists:
            raise RequestError('To few playlists')
        return playlists

    def makeNewPlaylist(self, clientID, tkn, playlist_name, playlist_description):
        req = requests.get( "https://api.spotify.com/v1/me",
                            headers={ 'authorization': "Bearer " + tkn })
        if req.status_code != 200:
            print('An error getting user ID occured, error code:'+str(req))
            raise RequestError('could not get user id')
        req_Json = req.json()
        usr_id = req_Json['id']
        req = requests.post( 'https://api.spotify.com/v1/users/'+usr_id+'/playlists',
                            headers={ 'authorization': "Bearer " + tkn },
                            json={ 'name': playlist_name, 'description': playlist_description, 'public': True})
        if (not req.ok):
            print('An error creating playlist occured, error code:'+str(req))
            raise RequestError('Could not add tracks to playlist')
        req_Json = req.json()
        playlist_id = req_Json["id"]
        return playlist_id

    def addTracksToPlaylist(self, clientID, tkn, playlist_id, track_ids):
        batch_size = 25
        batches = [track_ids[i:(i+batch_size)] for i in range(0,len(track_ids),batch_size)]
        for batch in batches:
            track_uri = ["spotify:track:"+track_id for track_id in batch]
            req = requests.post( 'https://api.spotify.com/v1/playlists/'+playlist_id+"/tracks",
                                headers={ 'authorization': "Bearer " + tkn },
                                json={"uris": track_uri})
            if (not req.ok):
                raise RequestError('Could not add tracks to playlist')
        return playlist_id

    def moodFilter(self, clientID, tkn, word, user_playlists, n_neighbors = 6, threshold = None):
        searched_playlists = self.search(word, clientID, tkn)
        tracks_searched_playlists = self.getPlaylstTracks(searched_playlists, clientID,tkn)
        props_searched_playlists = self.getTrackProperties(tracks_searched_playlists, clientID, tkn)[self.properties]

        tracks_user_playlists = self.getAllPlaylstTracks(user_playlists, clientID, tkn)
        props_user_playlists = self.getTrackProperties(tracks_user_playlists, clientID, tkn)[self.properties]

        ## Normalize data  based on sample data
        props_searched_max = props_searched_playlists.max()
        nrm_props_searched_playlists = props_searched_playlists / props_searched_max
        nrm_props_user_playlists = props_user_playlists/ props_searched_max

        neigh = NearestNeighbors(n_neighbors)
        neigh.fit(nrm_props_searched_playlists)
        dist, ind = neigh.kneighbors(nrm_props_user_playlists)
        sum_dist = np.sum(dist, axis=1)/n_neighbors
        if threshold == None:
            threshold = np.median(sum_dist)

        idx = list(np.where(sum_dist < threshold)[0])
        tracks_with_mood = []
        for i in list(np.where(sum_dist < threshold)[0]):
            tracks_with_mood.append(tracks_user_playlists[i])
        # Delete duplicates
        tracks_with_mood = list(dict.fromkeys(tracks_with_mood))
        if None in tracks_with_mood:
            raise RequestError('Did not find a match for that word')
        return tracks_with_mood

    def filterPlaylists(self,client_id,tkn,word,user_playlists):
        print('creating filter')
        tracks_id = self.moodFilter(client_id, tkn, word, user_playlists)
        print('creating playlist')
        playlist_id = self.makeNewPlaylist(client_id, tkn, "A "+word+" playlist", "A "+word+" playlist based on your own music! Created through Filterfy! Hope you will enjoy it ;)")
        print('adding tracks to playlist')
        self.addTracksToPlaylist(client_id, tkn, playlist_id, tracks_id)
        return playlist_id

if __name__ == '__main__':
    fltr = SptfyApiHndler()
    word = 'party'

    client_id = '7681ae26c9b64f25ad800adbdf03ea58'
    tkn = "BQCQ2nz_OL2Qig4Aa6lNDAI0AMi1eAWINy0fxX4HXF15qlU7Rv920fjK_9MqhTVrSnfAmAw19ICiCv7juDqzqoDD-tXn8eg3IVHJbRW1lfW1N-BbwWn2S-vdFWAo4rfVbmc3YHGCrw4DXv6QRugCIdITzJLD2OGAW6taCuKceWaJRbEYSfFx5aY3FCkJz6w--wv8Oy8-kktzmNATFlzIY8gkHdJ4cPotVuFYbUlLHuv06ExmeWSBXDPcgiVKTNnLn9MwH34tTBkcGXDgE6Ga"
    #
    api = SptfyApiHndler()
    # playlist = api.filterPlaylists(client_id,tkn,'roadtrip',['69S6FLy6M07i3ops1GyDOF'])
    tracks = api.moodFilter(client_id,tkn,'roadtrip',['69S6FLy6M07i3ops1GyDOF'])
