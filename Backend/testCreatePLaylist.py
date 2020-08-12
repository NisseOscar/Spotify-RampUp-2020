import requests
import json
from RequestError import RequestError

def testCreatePlaylist(tkn):

    ### GET USER ID
    req = requests.get( "https://api.spotify.com/v1/me",
                            headers={ 'authorization': "Bearer " + tkn })
    if req.status_code != 200:
        raise RequestError('something went wrong')
    req_Json = req.json()
    usr_id = req_Json['id']
    req = requests.post( 'https://api.spotify.com/v1/users/'+usr_id+'/playlists',
                            headers={ 'authorization': "Bearer " + tkn },
                            json={ 'name': 'Flifterfy Playlist', 'description': 'En första lists', 'public': False})
    if (not req.ok):
        raise RequestError('something went wrong')

if __name__ == '__main__':
    tkn = 'BQCqFcKIc7Lt0FDKLC8R6ZvCbXn1Or_iYPih0Am_3_E_XpGwDptOWL0cKUjN2ZCEp31yxGyiUKQ-Qd1fWZ459dosFNW1Dh579Bj1Nd_Stwwx55dbyYJ5K-1SdXFrlwKoCJ4b1HM0i0wGENiCeBABK6_AQ3WoJzb2LIt77WLSSlhUY9P6NKIILwwUm4jiZvaCrCz-2-gEe2MJg4I5_1eeDjuZxxjnbjVtT-qW4zp43IKAdXpyw92K-y4DtWLctA'
    testCreatePlaylist(tkn)
