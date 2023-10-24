def track_status(json):
    return render(['title', 'album', 'artist'], json)


def render(fields, json):
    return [json.get(f) for f in fields]


shuffle_modes = ['none', 'track', 'album']
repeat_modes = ['none', 'track', 'all']


def player_status(json):
    current_track = ""
    if json['playlist_tracks']:
        [current_track] = [t for t in json['playlist_loop']
                           if t['playlist index']
                           == int(json['playlist_cur_index'])]
        current_track = ' | '.join(track_status(current_track))
    return (f'[{json["player_name"]}] <{json["mode"]}>'
            f' vol:{json["mixer volume"]}%'
            + (f' s:{shuffle_modes[json["playlist shuffle"]]}'
                if json['playlist shuffle'] else '')
            + (f' r:{repeat_modes[json["playlist repeat"]]}'
                if json['playlist repeat'] else '')
            + f' {int(json.get("playlist_cur_index", -1))+1}'
            f'/{json["playlist_tracks"]} '
            + current_track)


def player_playlist(json):
    return [['>>' if t['playlist index'] == int(json['playlist_cur_index'])
             else t['playlist index'] + 1] + track_status(t)
            for t in json['playlist_loop']]


def track(json):
    return render(['id', 'title', 'album', 'artist', 'year'], json)


def album(json):
    return render(['id', 'album', 'artist', 'year'], json)


def artist(json):
    return (json['id'], json['artist'])
    return render(['id', 'artist'], json)
