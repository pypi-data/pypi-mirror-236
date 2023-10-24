import math

import tui_toolkit as b
import squeeze_jrpc.queries as queries
import squeeze_jrpc.commands as commands

import squeeze_ctl.ui.render as render


primary_fg = (0x40, 0x6e, 0x8e)
secondary_fg = (0x8e, 0xa8, 0xc3)
primary_bg = (0x16, 0x19, 0x25)
secondary_bg = (0x23, 0x39, 0x5b)
accent = (0xcb, 0xf7, 0xed)


class Browse(b.App):
    def __init__(self, server, player_name):
        super().__init__(self.search_term_loop)
        self.server = server
        self.player_name = player_name

    def style_content(self, text, width):
        return self.term.color_rgb(*primary_fg)(
                self.term.on_color_rgb(*primary_bg)(text))

    def style_label(self, text, width):
        return self.term.color_rgb(*secondary_fg)(
                self.term.on_color_rgb(*secondary_bg)(
                    self.term.ljust(text, width)))

    def style_input(self, text, width):
        return self.term.color_rgb(*accent)(
                self.term.on_color_rgb(*primary_bg)(
                    self.term.ljust(text)))

    def initialise(self):
        split_col = math.floor(self.term.width * 2 / 3)
        ql = f'[{self.player_name}] Search for:'
        self.label_query = b.Text(
                self.term, 0, 0, len(ql), 1,
                text=ql,
                style=self.style_label)
        self.label_tracks = b.Text(
                self.term, split_col, 0, self.term.width, 1,
                text='Tracks:',
                style=self.style_label)
        self.tracks = b.HeadedTable(
                self.term, split_col, 1, self.term.width, self.term.height,
                headers=['Title:', 'Artist:'],
                style=self.style_content,
                style_focus=self.style_input,
                style_headers=self.style_label,
                formatter=(lambda track: [track.get('title'),
                                          track.get('artist')]))
        self.albums = b.HeadedTable(
                self.term, 0, 1, split_col, self.term.height,
                headers=['Album:', 'Artist:', 'Year:'],
                formatter=lambda album: [album.get('album'),
                                         album.get('artist'),
                                         album.get('year')],
                style=self.style_content,
                style_headers=self.style_label,
                style_focus=self.style_input,
                focus_listeners=[self.on_focus_album_changed])
        self.query = b.Input(
                self.term, self.label_query.width, 0,
                split_col - self.label_query.width, 1,
                change_listeners=[self.on_query_changed],
                style_focus=self.style_input,
                style=self.style_label)

    def layout(self):
        split_col = math.floor(self.term.width * 2 / 3)
        self.label_tracks.resize(x0=split_col, width=self.term.width)
        self.tracks.resize(
                x0=split_col, width=self.term.width,
                height=self.term.height)
        self.albums.resize(width=split_col, height=self.term.height)
        self.query.resize(width=split_col - self.label_query.width)
        with self.term.hidden_cursor():
            self.query.render()
            self.albums.render()
            self.tracks.render()
            self.label_tracks.render()
            self.label_query.render()

    def on_focus_album_changed(self, focus_album):
        if focus_album is None:
            self.tracks.set_contents([])
        else:
            self.tracks.set_contents(
                    queries.tracks(
                        self.server,
                        dict(
                            album_id=focus_album.get('id'),
                            sort='tracknum')))
        self.tracks.set_focus_index(None)
        self.tracks.render()

    def on_query_changed(self, query):
        album_list = []
        if len(query) > 1:
            album_list = queries.albums(self.server, dict(search=query))
        self.albums.set_contents(album_list)
        self.albums.render()

    def tracks_loop(self):
        with self.term.hidden_cursor():
            while not self.terminal_resized:
                match b.navigate(
                        self.tracks,
                        ['a', '+', 'p', '>', 'n', self.term.KEY_TAB]):
                    case 'a' | '+':  # add
                        tid = self.tracks.focus_item()['id']
                        commands.player_playlist_add(
                                self.server, self.player_name,
                                tracks=[tid])
                    case 'p' | '>':  # play
                        tid = self.tracks.focus_item()['id']
                        commands.player_playlist_play(
                                self.server, self.player_name,
                                tracks=[tid])
                    case 'n':  # insert to play next
                        tid = self.tracks.focus_item()['id']
                        commands.player_playlist_insert(
                                self.server, self.player_name,
                                tracks=[tid])
                    case '\t':
                        self.tracks.set_focus_index(None)
                        self.albums.set_focus_index(None)
                        return self.search_term_loop
            return self.tracks_loop

    def albums_loop(self):
        with self.term.hidden_cursor():
            while not self.terminal_resized:
                match b.navigate(
                        self.albums,
                        ['a', '+', 'p', '>', 'n', self.term.KEY_TAB]):
                    case 'a' | '+':  # add
                        album_id = self.albums.focus_item().get('id')
                        commands.player_playlist_add(
                                self.server, self.player_name,
                                album=album_id)
                    case 'p' | '>':  # play
                        album_id = self.albums.focus_item().get('id')
                        commands.player_playlist_play(
                                self.server, self.player_name,
                                album=album_id)
                    case 'n':  # insert to play next
                        album_id = self.albums.focus_item().get('id')
                        commands.player_playlist_insert(
                                self.server, self.player_name,
                                album=album_id)
                    case '\t':
                        self.tracks.set_focus_index(0)
                        return self.tracks_loop
            return self.albums_loop

    def search_term_loop(self):
        with self.term.hidden_cursor():
            self.query.render(True)
            self.albums.render()
            self.tracks.set_contents([])
            self.tracks.render()
            self.query.interact([self.term.KEY_TAB])
            self.query.render(False)
            if self.terminal_resized:
                return self.search_term_loop
            self.albums.set_focus_index(0)
            return self.albums_loop


# entrypoint
def browse(server, player_name):
    app = Browse(server, player_name)
    app.run()


def format_seconds(s):
    minutes, seconds = divmod(s, 60)
    return f' {minutes:2.0f}:{seconds:02.0f}'


def progress_bar(width, part, total):
    done = math.floor(width * (part / total))
    return ('█' * done) + (' ' * (width - done))


class Player(b.App):
    def __init__(self, server, player_name):
        super().__init__(self.playback_loop)
        self.server = server
        self.player_name = player_name

    def style_status(self, text, width):
        return self.term.color_rgb(*secondary_fg)(
                self.term.on_color_rgb(*secondary_bg)(
                    self.term.ljust(text, width)))

    def style_content(self, text, width):
        return self.term.color_rgb(*primary_fg)(
                self.term.on_color_rgb(*primary_bg)(
                    self.term.ljust(text, width)))

    def style_playing(self, text, width):
        return self.term.color_rgb(*accent)(text)

    def initialise(self):
        self.status = b.Text(
                self.term, 0, 0, self.term.width, 1, style=self.style_status)
        self.elapsed_time = b.Text(
                self.term, 0, 1, 7, 1, style=self.style_status)
        self.remaining_time = b.Text(
                self.term, self.term.width - 7, 1,
                self.term.width, 1, style=self.style_status)
        self.progress = b.Text(
                self.term, 7, 1,
                self.term.width - self.elapsed_time.width
                - self.remaining_time.width, 1,
                style=self.style_status)
        self.playlist = b.Table(
                self.term, 0, 2, self.term.width, self.term.height,
                style=self.style_content,
                style_focus=self.style_playing,
                formatter=lambda track: [track.get('playlist index') + 1,
                                         track.get('title'),
                                         track.get('album'),
                                         track.get('artist')])

    def layout(self):
        self.status.resize(width=self.term.width)
        self.remaining_time.resize(x0=self.term.width - 7)
        self.progress.resize(width=(
            self.term.width - self.elapsed_time.width
            - self.remaining_time.width))
        self.playlist.resize(width=self.term.width)
        self.playlist.resize(height=self.term.height)

    def playback_loop(self):
        with self.term.hidden_cursor(), self.term.cbreak():
            while not self.terminal_resized:
                status_data = commands.get_player_status(
                        self.server, self.player_name)
                self.status.set_text(render.player_status(status_data))
                duration = status_data.get('duration')
                elapsed = status_data.get('time')
                try:
                    self.elapsed_time.set_text(format_seconds(elapsed))
                    self.remaining_time.set_text(
                            format_seconds(duration - elapsed))
                    self.progress.set_text(
                            progress_bar(
                                self.progress.width, elapsed, duration))
                except TypeError:
                    self.elapsed_time.set_text(' --:-- ')
                    self.remaining_time.set_text(' --:-- ')
                    self.progress.set_text(' ')
                self.playlist.set_contents(status_data.get('playlist_loop'))
                try:
                    self.playlist.set_focus_index(
                            int(status_data.get('playlist_cur_index')))
                except TypeError:
                    self.playlist.set_focus_index(None)
                self.playlist.render()
                k = self.term.inkey(1)
                if k.is_sequence:
                    match k.code:
                        case self.term.KEY_LEFT:
                            commands.player_prev(self.server, self.player_name)
                        case self.term.KEY_RIGHT:
                            commands.player_next(self.server, self.player_name)
                        case self.term.KEY_TAB:
                            return self.edit_loop
                else:
                    match k:
                        case 'q':
                            return None
                        case ' ':
                            commands.player_pause(
                                    self.server, self.player_name)
                        case 'h':
                            commands.player_prev(self.server, self.player_name)
                        case 'l':
                            commands.player_next(self.server, self.player_name)
                        case '+':
                            commands.player_volume(
                                    self.server, self.player_name, "+2")
                        case '-':
                            commands.player_volume(
                                    self.server, self.player_name, "-2")
                        case 'r':
                            repeat_mode = status_data.get('playlist repeat')
                            repeat_mode = (0 if repeat_mode >= 2
                                           else repeat_mode + 1)
                            commands.player_repeat(
                                    self.server, self.player_name, repeat_mode)
                        case 's':
                            shuffle_mode = status_data.get('playlist shuffle')
                            shuffle_mode = (0 if shuffle_mode >= 2
                                            else shuffle_mode + 1)
                            commands.player_shuffle(
                                    self.server, self.player_name,
                                    shuffle_mode)
            return self.playback_loop

    def edit_loop(self):
        with self.term.hidden_cursor():
            playback_focus = self.playlist.style_focus
            self.playlist.style_focus = (
                    lambda text, width: self.term.reverse(text))
            k = b.navigate(
                    self.playlist,
                    [
                        self.term.KEY_BACKSPACE,
                        self.term.KEY_TAB,
                        self.term.KEY_ENTER])
            self.playlist.style_focus = playback_focus
            if self.terminal_resized:
                return self.playback_loop
            if k.is_sequence:
                match k.code:
                    case self.term.KEY_TAB:  # switch back to playback
                        pass
                    case self.term.KEY_ENTER:  # play selected track
                        commands.player_playlist_index(
                                self.server, self.player_name,
                                self.playlist.focus_index)
                    case self.term.KEY_BACKSPACE:  # delete track
                        commands.player_playlist_remove(
                                self.server, self.player_name,
                                self.playlist.focus_index)
            return self.playback_loop


# entrypoint
def player(server, player_name):
    p = Player(server, player_name)
    p.run()
