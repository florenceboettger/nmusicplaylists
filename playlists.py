from enum import Enum

class Game(Enum):
    NONE = ""
    SPLATOON2 = "Splatoon 2"
    SPLATOON3 = "Splatoon 3"

class PlaylistType(Enum):
    NONE = ""
    SPLATOON2 = "''Splatoon 2''"
    SPLATOON3 = "''Splatoon 3''"
    ARTISTS = "The artists of ''Splatoon''"
    
playlisttypes = {
    Game.SPLATOON2: PlaylistType.SPLATOON2,
    Game.SPLATOON3: PlaylistType.SPLATOON3
}

abbreviations = {
    Game.SPLATOON2: "S2",
    Game.SPLATOON3: "S3"
}

colors = {
    Game.NONE: "sitecolor-generic",
    Game.SPLATOON2: "sitecolor-s2",
    Game.SPLATOON3: "sitecolor-s3"
}

allplaylists = [
    PlaylistType.SPLATOON2.value,
    PlaylistType.SPLATOON3.value,
    PlaylistType.ARTISTS.value,
    "Match your mood",
    "Set the scene",
]

class Song:
    def __init__(self, props: dict, game: Game):
        self.name = props["name"]
        self.formattedname = props["formattedname"]
        self.band = props["band"] if "band" in props else "N/A"
        self.formattedband = props["formattedband"] if "formattedband" in props else "N/A"
        self.length = props["length"]
        self.extend = props["extend"]
        self.unlisted = props["unlisted"] if "unlisted" in props else False
        self.uuid = props["uuid"] if not self.unlisted and "uuid" in props else ""
        self.playlists = {k: [] for k in allplaylists}
        self.playlists["Match your mood"] = [] if (not "matchyourmood" in props) else props["matchyourmood"]
        self.playlists["Set the scene"] = [] if (not "setthescene" in props) else props["setthescene"]
        self.game = game

    def tojson(self, name: str) -> dict:
        output =  {
            "name": self.formattedname,
            "band": self.formattedband,
            "length": self.length,
            "extend": self.extend,
            "playlists": {k: [p for p in v if not p in [name, "All tracks", "Top tracks"]] for k, v in self.playlists.items() if len([p for p in v if not p in [name, "All tracks", "Top tracks"]]) > 0}
        }
        if name == "All tracks":
            output["uuid"] = self.uuid
        return output

class AllTracks():
    def __init__(self):
        self.songs = {}

    def addsongs(self, songs: list, game: Game):
        for songprops in songs:
            song = Song(songprops, game)
            if not AllTracks.makekey(song.name, song.band, song.game.value) in self.songs:
                self.songs[AllTracks.makekey(song.name, song.band, song.game.value)] = song

    @staticmethod
    def makekey(name, band, gamename) -> str:
        return f"Song: {name}, Band: {band}, Game: {gamename}"

class Playlist:
    def __init__(self, props: dict, name: str, alltracks: AllTracks, playlisttype: PlaylistType, game: Game):
        self.name = name
        self.type = playlisttype
        self.songs = []
        self.game = game
        self.totalgames = set()
        for songprops in props["songlist"]:
            band = songprops["band"] if "band" in songprops else "N/A"
            songgame = self.game if self.game != Game.NONE else Game(songprops["game"])
            if self.type == PlaylistType.ARTISTS and (band == "" or band == "N/A"):
                band = self.name if self.name != "Grizzco Industries" else "Grizzco"
            song = alltracks.songs[AllTracks.makekey(songprops["name"], band, songgame.value)]
            if self.type != PlaylistType.NONE and self.name != "All tracks" and self.name != "Top tracks":
                song.playlists[self.type.value].append(self.name)
            self.songs.append(song)
            self.totalgames.add(songgame)
        self.color = props["color"] if "color" in props else colors[self.game]
        self.hasbands = len([s for s in self.songs if s.band != "N/A"]) > 0        

    def setfeaturedplaylists(self):
        found = []
        for playlist in allplaylists:
                for song in self.songs:
                    if len([p for p in song.playlists[playlist] if not p in [self.name, "Top tracks", "All tracks"]]) > 0:
                        found.append(playlist)
                        break
        self.featuredplaylists = found

    def tojson(self) -> dict:
        return {
            "color": self.color,
            "featuredplaylists": self.featuredplaylists,
            "songlist": [song.tojson(self.name) for song in self.songs if not (song.unlisted and self.name == "All tracks")]
        }