import os
from datetime import datetime
import json
from csv import DictReader

SHOW_DIR = 'static/shows/'
PLAYLIST_DIR = 'static/playlists/'

class Show():
    def __init__(self, show_file_path):
        self.datestring_format = '%Y-%m-%d'
        self.show_file_path = SHOW_DIR + show_file_path
        self.show_date = None
        self.show_creation = None
        self.title = None
        self.description = None
        self.show_type = None
        self.playlist_path = None
        self.playlist = None
        self.embed_url = None
        self.embed_code = None
        self.slug = show_file_path.split('.')[0]

        self._show_from_file()

    def _playlist_dict_from_file(self, playlist_path):
        songs = []

        with open(PLAYLIST_DIR + playlist_path, 'r') as f:
            reader = DictReader(f, delimiter='\t')

            for row in reader:
                songs_dict = {'album': row['Album'],
                              'artist': row['Artist'],
                              'name': row['Name'],
                              'year': row['Year'],
                              'genre': row['Genre']}
                songs.append(songs_dict)

        return songs

    def _make_embed_code(self):
        embed_width = 600
        embed_height = 600
        embed_frame_border = 0
        embed_template = '<iframe src="{url}" width="{width}" \
                height="{height}" frameborder="{frame_border}" \
                allowtransparency="true" allow="encrypted-media">\
                    </iframe>'.format(
                        url=self.embed_url,
                        height=embed_height,
                        width=embed_width,
                        frame_border=embed_frame_border
                    )

        return embed_template

    def _show_from_file(self):
        with open(self.show_file_path, 'rU') as f:
            show_dict = json.load(f)
            self.show_date = datetime.strptime(
                show_dict.get('show_date'),
                self.datestring_format
            )
            self.show_creation = self.show_date  # same value for now
            self.title = show_dict.get('title')
            self.description = show_dict.get('description')
            self.show_type = show_dict.get('show_type')
            self.playlist_path = show_dict.get('playlist')
            self.embed_url = show_dict.get('embed_url')

        if self.embed_url:
            self.embed_code = self._make_embed_code()
        if self.playlist_path:
            self.playlist = self._playlist_dict_from_file(self.playlist_path)

    def to_dict(self):
        return {
            'show_date': self.show_date,
            'show_creation': self.show_creation,
            'title': self.title,
            'description': self.description,
            'show_type': self.show_type,
            'playlist': self.playlist,
            'slug': self.slug,
            'embed_url': self.embed_url,
            'embed_code': self.embed_code
        }


def get_show_from_slug(shows, slug):
    for show in shows:
        if show.slug == slug:
            return show

    return None


def get_shows():
    shows = []
    shows_dir = os.listdir(SHOW_DIR)

    for show_file in shows_dir:
        new_show = Show(show_file)
        shows.append(new_show)

    return sorted(  # sort by show_date key, desc
        shows,
        key=lambda show: show.show_date,
        reverse=True
    )
