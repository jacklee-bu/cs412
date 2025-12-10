# File: import_tab.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: Management command to import guitar tabs from text files

from django.core.management.base import BaseCommand
from project.models import Song, Tab


class Command(BaseCommand):
    """Management command to import a guitar tab from a text file."""

    help = 'Import a guitar tab from a text file'

    def add_arguments(self, parser):
        """Define command line arguments."""
        parser.add_argument('file', type=str, help='Path to the tab file')

    def handle(self, *args, **options):
        """Execute the import command."""
        filepath = options['file']

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            self.stderr.write(f'File not found: {filepath}')
            return

        # parse the file - metadata at top, tab content below
        lines = content.split('\n')
        metadata = {}
        tab_start = 0

        # read metadata lines (key: value format)
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('e|') or line.startswith('E|'):
                # reached the tab content
                tab_start = i
                break
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()

        # get tab content (everything after metadata)
        tab_content = '\n'.join(lines[tab_start:])

        # required fields
        title = metadata.get('title', metadata.get('song', ''))
        artist = metadata.get('artist', '')

        if not title or not artist:
            self.stderr.write('Error: title and artist are required')
            self.stderr.write('File format:')
            self.stderr.write('  title: Song Name')
            self.stderr.write('  artist: Artist Name')
            self.stderr.write('  ... other metadata ...')
            self.stderr.write('  [tab content]')
            return

        # get or create the song
        song, created = Song.objects.get_or_create(
            normalized_title=title.lower().strip(),
            normalized_artist=artist.lower().strip(),
            defaults={
                'title': title,
                'artist': artist,
                'album': metadata.get('album', ''),
                'year': int(metadata.get('year', 0)) or None,
            }
        )

        if created:
            self.stdout.write(f'Created song: {song}')
        else:
            self.stdout.write(f'Found existing song: {song}')

        # create the tab
        tab = Tab.objects.create(
            song=song,
            content=tab_content.strip(),
            chords_used=metadata.get('chords', metadata.get('chords_used', '')),
            strumming_pattern=metadata.get('pattern', metadata.get('strumming', '')),
            tuning=metadata.get('tuning', 'standard'),
            capo=int(metadata.get('capo', 0)),
            tempo=int(metadata.get('tempo', metadata.get('bpm', 0))) or None,
            source_url=metadata.get('source_url', metadata.get('url', '')),
            source_site=metadata.get('source', metadata.get('source_site', '')),
        )

        self.stdout.write(self.style.SUCCESS(f'Created tab #{tab.id} for {song}'))
