import click
import time
from tabulate import tabulate
import tomllib
import os.path

import squeeze_jrpc.commands as commands
import squeeze_jrpc.queries as queries

import squeeze_ctl
import squeeze_ctl.ui.tui as tui
import squeeze_ctl.ui.render as render


player_name = None
server = None


@click.group()
@click.version_option(version=squeeze_ctl.__version__)
@click.option('-h', '--host', type=str)
@click.option('-p', '--port', type=int)
@click.option('-c', '--config-file', default='~/.squeeze-ctl.toml')
def cli_main(host, port, config_file):
    global server
    if not host or not port:
        with open(os.path.expanduser(config_file), mode='rb') as f:
            cfg = tomllib.load(f)
        host = host if host else cfg['server']['host']
        port = port if port else cfg['server']['port']
    server = (host, port)


@cli_main.command(help='list the available players')
def players():
    print(commands.get_players(server))


@cli_main.group(help='control a player')
@click.argument('name')
def player(name):
    global player_name
    player_name = name


@player.command(help='browse your music library')
def browse():
    tui.browse(server, player_name)


@player.command(name='player-ui', help="monitor and control a player")
def player_ui():
    tui.player(server, player_name)


@player.command(help='show the player status')
def status():
    show_status()


@player.command(help='monitor the player status and playlist')
@click.option('-i', '--interval', default=1, help='polling interval (seconds)')
def monitor(interval):
    max_line_length = 0
    while True:
        s = render.player_status(
                commands.get_player_status(server, player_name))
        s += (' ' * (max_line_length - len(s)))
        max_line_length = max(max_line_length, len(s))
        print(s, end='\r')
        time.sleep(interval)


@player.command(help='show the current playlist')
def playlist():
    show_playlist()


@player.command(help='pause/unpause playback')
def pause():
    commands.player_pause(server, player_name)
    show_status()


@player.command(help='play the previous track from the current playlist')
def prev():
    commands.player_prev(server, player_name)
    show_status()


@player.command(help='play the next track from the current playlist')
def next():
    commands.player_next(server, player_name)
    show_status()


@player.command(help='play the specified track from the current playlist')
@click.argument('index', type=int)
def index(index):
    commands.player_playlist_index(server, player_name, index - 1)
    show_status()


@player.command(help='turn the volume up')
def louder():
    commands.player_volume(server, player_name, '+2')
    show_status()


@player.command(help='set the player volume (0..100%)')
@click.argument('volume', type=int)
def volume(volume):
    commands.player_volume(server, player_name, volume)
    show_status()


@player.command(help='turn the volume down')
def shush():
    commands.player_volume(server, player_name, '-2')
    show_status()


shuffle_modes = {'off': 0, 'track': 1, 'album': 2}


@player.command(help="set playlist shuffle mode")
@click.argument('mode', type=click.Choice(['off', 'track', 'album']))
def shuffle(mode):
    commands.player_shuffle(server, player_name, shuffle_modes[mode])
    show_status()


repeat_modes = {'off': 0, 'track': 1, 'all': 2}


@player.command(help="set playlist repeat mode")
@click.argument('mode', type=click.Choice(['off', 'track', 'all']))
def repeat(mode):
    commands.player_repeat(server, player_name, repeat_modes[mode])
    show_status()


@player.command(help="remove track from playlist")
@click.argument('index', type=int)
def remove(index):
    commands.player_playlist_remove(server, player_name, index - 1)
    show_playlist()


@player.command(help="add things to the playlist")
@click.option('-t', '--track', type=int, multiple=True, help='track id')
@click.option('-a', '--album', type=int, help='album id')
@click.option('-A', '--artist', type=int, help='artist id')
def add(track, album, artist):
    n = commands.player_playlist_add(
            server, player_name, tracks=track, album=album, artist=artist)
    show_playlist()
    print(f'{n} tracks added')


@player.command(help="replace the playlist and play")
@click.option('-t', '--track', type=int, multiple=True, help='track id')
@click.option('-a', '--album', type=int, help='album id')
@click.option('-A', '--artist', type=int, help='artist id')
def play(track, album, artist):
    n = commands.player_playlist_play(
            server, player_name, tracks=track, album=album, artist=artist)
    show_playlist()
    print(f'{n} tracks added')
    show_status()


@player.command(help="insert to play next")
@click.option('-t', '--track', type=int, multiple=True, help='track id')
@click.option('-a', '--album', type=int, help='album id')
@click.option('-A', '--artist', type=int, help='artist id')
def playnext(track, album, artist):
    n = commands.player_playlist_playnext(
            server, player_name, tracks=track, album=album, artist=artist)
    show_playlist()
    print(f'{n} tracks added')
    show_status()


# Query music library

@cli_main.command(help='find albums')
@click.option('-s', '--search', type=str, help='string search term')
@click.option('-y', '--year', type=int, help='year to search')
@click.option('-A', '--artist', type=int, help='artist id to search')
@click.option('-S', '--sort',
              type=click.Choice(['album', 'new', 'artistalbum', 'yearalbum',
                                 'yearartistalbum', 'random']),
              default='album', help='results order')
def albums(search, year, artist, sort):
    params = dict(sort=sort)
    if search:
        params['search'] = search
    if year:
        params['year'] = year
    if artist:
        params['artist_id'] = artist
    result = queries.albums(server, params)
    print(tabulate([render.album_query(a) for a in result],
                   headers=['id', 'album', 'artist', 'year']))


@cli_main.command(help='find tracks')
@click.option('-s', '--search', type=str, help='string search term')
@click.option('-y', '--year', type=int, help='year to search')
@click.option('-A', '--artist', type=int, help='artist id to search')
@click.option('-a', '--album', type=int, help='album id to search')
def tracks(search, year, artist, album):
    params = dict()
    if search:
        params['search'] = search
    if year:
        params['year'] = year
    if artist:
        params['artist_id'] = artist
    if album:
        params['album_id'] = album
    result = queries.tracks(server, params)
    print(tabulate([render.track(a) for a in result],
                   headers=['id', 'track', 'album', 'artist', 'year']))


@cli_main.command(help='find artists')
@click.option('-s', '--search', type=str, help='string search term')
@click.option('-y', '--year', type=int, help='year to search')
def artists(search, year):
    params = {}
    if search:
        params['search'] = search
    if year:
        params['year'] = year
    result = queries.artists(server, params)
    print(tabulate([render.artist(a) for a in result],
                   headers=['id', 'name']))


@cli_main.command(help='recntly added albums')
def newmusic():
    result = queries.albums(server, dict(sort='new'))
    print(tabulate([render.album(a) for a in result],
                   headers=['id', 'album', 'artist']))


# TODO: query music library

# helpers
def show_status():
    print(render.player_status(
        commands.get_player_status(server, player_name)))


def show_playlist():
    print(tabulate(
        render.player_playlist(
            commands.get_player_status(server, player_name)),
        headers=['', 'Title', 'Album', 'Artist']))
