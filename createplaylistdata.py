import json
from playlists import *
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

games = [
    Game.SPLATOON,
    Game.SPLATOON2,
    Game.SPLATOON3]

playlists = {}
alltracks = AllTracks()

datapath = Path(__file__).resolve().parent / "data"

for game in games:
    playlists[game.value] = {}
    gamepath = datapath / game.value
    with (gamepath / "alltracks.json").open("r", encoding="utf8") as f:
        alltracksplaylistprops = json.loads(''.join(f.readlines()))
        alltracks.addsongs(alltracksplaylistprops["songlist"], game)
for game in games:
    gamepath = datapath / game.value
    if (gamepath / "alltracks.json").exists():
        with (gamepath / "alltracks.json").open("r", encoding="utf8") as f:
            alltracksplaylistprops = json.loads(''.join(f.readlines()))
            playlists[game.value]["All tracks"] = Playlist(alltracksplaylistprops, "All tracks", alltracks, playlisttypes[game], game)
    if (gamepath / "toptracks.json").exists():
        with (gamepath / "toptracks.json").open("r", encoding="utf8") as f:
            toptracksplaylistprops = json.loads(''.join(f.readlines()))
            playlists[game.value]["Top tracks"] = Playlist(toptracksplaylistprops, "Top tracks", alltracks, playlisttypes[game], game)
    if (gamepath / "mainplaylists.json").exists():
        with (gamepath / "mainplaylists.json").open("r", encoding="utf8") as f:
            mainplaylistsprops = json.loads(''.join(f.readlines()))
            for name, playlistprops in mainplaylistsprops["playlists"].items():
                playlists[game.value][name] = Playlist(playlistprops, name, alltracks, playlisttypes[game], game)

    if (gamepath / "unlistedtracks.json").exists():
        unlistedtracksplaylistprops = None
        with (gamepath / "unlistedtracks.json").open("r", encoding="utf8") as f:          
            unlistedtracksplaylistprops = json.loads(''.join(f.readlines()))
            playlists[game.value]["Removed tracks"] = Playlist(unlistedtracksplaylistprops, "Removed tracks", alltracks, playlisttypes[game] if game in playlisttypes else PlaylistType.NONE, game)

playlists["Misc"] = {}
with (datapath / "Misc" / "artistsplaylists.json").open("r", encoding="utf8") as f:
    artistsplaylistprops = json.loads(''.join(f.readlines()))
    for name, playlistprops in artistsplaylistprops["playlists"].items():
        playlists["Misc"][name] = Playlist(playlistprops, name, alltracks, PlaylistType.ARTISTS, Game.NONE)

with (datapath / "Misc" / "miscplaylists.json").open("r", encoding="utf8") as f:
    miscplaylistprops = json.loads(''.join(f.readlines()))
    for name, playlistprops in miscplaylistprops["playlists"].items():
        playlists["Misc"][name] = Playlist(playlistprops, name, alltracks, PlaylistType.NONE, Game.NONE)

outputpath = Path(__file__).resolve().parent / "output"
outputpath.mkdir(parents=True, exist_ok=True)

for playlistset, gameplaylists in playlists.items():
    for playlist in gameplaylists.values():
        playlist.setfeaturedplaylists()
    with (outputpath / f"{playlistset}.json").open("w", encoding="utf8") as f:
        f.write(json.dumps({k: p.tojson() for k, p in gameplaylists.items()}, indent=4, ensure_ascii=False))
