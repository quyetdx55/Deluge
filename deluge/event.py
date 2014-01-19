#
# event.py
#
# Copyright (C) 2009 Andrew Resch <andrewresch@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#
#

"""
Event module.

This module describes the types of events that can be generated by the daemon
and subsequently emitted to the clients.

"""

known_events = {}


class DelugeEventMetaClass(type):
    """
    This metaclass simply keeps a list of all events classes created.
    """
    def __init__(cls, name, bases, dct):
        super(DelugeEventMetaClass, cls).__init__(name, bases, dct)
        if name != "DelugeEvent":
            known_events[name] = cls


class DelugeEvent(object):
    """
    The base class for all events.

    :prop name: this is the name of the class which is in-turn the event name
    :type name: string
    :prop args: a list of the attribute values
    :type args: list

    """
    __metaclass__ = DelugeEventMetaClass

    def _get_name(self):
        return self.__class__.__name__

    def _get_args(self):
        if not hasattr(self, "_args"):
            return []
        return self._args

    name = property(fget=_get_name)
    args = property(fget=_get_args)


class TorrentAddedEvent(DelugeEvent):
    """
    Emitted when a new torrent is successfully added to the session.
    """
    def __init__(self, torrent_id, from_state):
        """
        :param torrent_id: the torrent_id of the torrent that was added
        :type torrent_id: string
        :param from_state: was the torrent loaded from state? Or is it a new torrent.
        :type from_state: bool
        """
        self._args = [torrent_id, from_state]


class TorrentRemovedEvent(DelugeEvent):
    """
    Emitted when a torrent has been removed from the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class PreTorrentRemovedEvent(DelugeEvent):
    """
    Emitted when a torrent is about to be removed from the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class TorrentStateChangedEvent(DelugeEvent):
    """
    Emitted when a torrent changes state.
    """
    def __init__(self, torrent_id, state):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param state: the new state
        :type state: string
        """
        self._args = [torrent_id, state]


class TorrentQueueChangedEvent(DelugeEvent):
    """
    Emitted when the queue order has changed.
    """
    pass


class TorrentFolderRenamedEvent(DelugeEvent):
    """
    Emitted when a folder within a torrent has been renamed.
    """
    def __init__(self, torrent_id, old, new):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param old: the old folder name
        :type old: string
        :param new: the new folder name
        :type new: string
        """
        self._args = [torrent_id, old, new]


class TorrentFileRenamedEvent(DelugeEvent):
    """
    Emitted when a file within a torrent has been renamed.
    """
    def __init__(self, torrent_id, index, name):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param index: the index of the file
        :type index: int
        :param name: the new filename
        :type name: string
        """
        self._args = [torrent_id, index, name]


class TorrentFinishedEvent(DelugeEvent):
    """
    Emitted when a torrent finishes downloading.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class TorrentResumedEvent(DelugeEvent):
    """
    Emitted when a torrent resumes from a paused state.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        """
        self._args = [torrent_id]


class TorrentFileCompletedEvent(DelugeEvent):
    """
    Emitted when a file completes.
    """
    def __init__(self, torrent_id, index):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param index: the file index
        :type index: int
        """
        self._args = [torrent_id, index]


class TorrentStorageMovedEvent(DelugeEvent):
    """
    Emitted when the storage location for a torrent has been moved.
    """
    def __init__(self, torrent_id, path):
        """
        :param torrent_id: the torrent_id
        :type torrent_id: string
        :param path: the new location
        :type path: string
        """
        self._args = [torrent_id, path]


class CreateTorrentProgressEvent(DelugeEvent):
    """
    Emitted when creating a torrent file remotely.
    """
    def __init__(self, piece_count, num_pieces):
        self._args = [piece_count, num_pieces]


class NewVersionAvailableEvent(DelugeEvent):
    """
    Emitted when a more recent version of Deluge is available.
    """
    def __init__(self, new_release):
        """
        :param new_release: the new version that is available
        :type new_release: string
        """
        self._args = [new_release]


class SessionStartedEvent(DelugeEvent):
    """
    Emitted when a session has started.  This typically only happens once when
    the daemon is initially started.
    """
    pass


class SessionPausedEvent(DelugeEvent):
    """
    Emitted when the session has been paused.
    """
    pass


class SessionResumedEvent(DelugeEvent):
    """
    Emitted when the session has been resumed.
    """
    pass


class ConfigValueChangedEvent(DelugeEvent):
    """
    Emitted when a config value changes in the Core.
    """
    def __init__(self, key, value):
        """
        :param key: the key that changed
        :type key: string
        :param value: the new value of the `:param:key`
        """
        self._args = [key, value]


class PluginEnabledEvent(DelugeEvent):
    """
    Emitted when a plugin is enabled in the Core.
    """
    def __init__(self, plugin_name):
        self._args = [plugin_name]


class PluginDisabledEvent(DelugeEvent):
    """
    Emitted when a plugin is disabled in the Core.
    """
    def __init__(self, plugin_name):
        self._args = [plugin_name]
