from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets.library import Item
from beets.mediafile import MediaFile
from beets.util import syspath
from beets import ui


FIELDS = ['length', 'bitrate', 'format', 'samplerate', 'bitdepth', 'channels']


class ReloadAudioMetadata(BeetsPlugin):
    def commands(self):
        reload_command = Subcommand('reload', help='reload audio data (length, format, etc.) from files')
        reload_command.parser.add_album_option()
        reload_command.parser.add_option(
            '-n', '--dry-run',
            dest='dry_run',
            action='store_true',
            help="don't do anything"
        )
        reload_command.func = self._reload_command
        return [reload_command]

    def _reload_command(self, lib, opts, args):
        if opts.album:
            selection = [item for album in lib.albums(ui.decargs(args)) for item in album.items()]
        else:
            selection = lib.items(ui.decargs(args))
        for item in selection:
            mf = MediaFile(syspath(item.path))
            update = {}
            for field in FIELDS:
                v = getattr(mf, field)
                if item[field] != v:
                    update[field] = v
            if update:
                print(f"{item.artist} - {item.title}:")
                for k, v in update.items():
                    print(f"  {k}: {item[k]} -> {v}")
                    if not opts.dry_run:
                        item[k] = v
                if not opts.dry_run:
                    item.store()

