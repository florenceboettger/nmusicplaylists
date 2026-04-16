import json
import math
from pathlib import Path

path = Path(__file__).resolve().parent / "data" / "Original" / "alltracks_s3.json"
datapath = Path(__file__).resolve().parent / "data" / "Splatoon 3" / "alltracks.json"

with path.open("r", encoding="utf8") as f:    
    alltracks = json.loads(''.join(f.readlines()))

    alltracks_old = None
    with datapath.open("r", encoding="utf8") as g:
        alltracks_old = json.loads(''.join(g.readlines()))

    export = {
        "uuid": alltracks["id"],
        "thumbnail": alltracks_old["thumbnail"],
        "introduction": alltracks_old["introduction"]
    }

    songlist = []
    for track in alltracks["tracks"]:
        newsong = {}
        split = track["name"].split(" / ", 1)
        newsong["name"] = split[0]
        newsong["formattedname"] = newsong["name"]
        if len(split) > 1:
            newsong["band"] = split[1]
            newsong["formattedband"] = split[1]
        milliDuration = track["media"]["payloadList"][0]["durationMillis"]
        minuteDuration = milliDuration // 60000
        secondDuration = math.ceil((milliDuration % 60000) / 1000)
        newsong["length"] = f"{minuteDuration}:{secondDuration:02d}"
        newsong["extend"] = track["media"]["payloadList"][0]["containsLoopableMedia"]
        newsong["uuid"] = track["id"]

        exists = False
        for old_track in alltracks_old["songlist"]:
            if old_track["name"] == newsong["name"] and (("band" not in old_track and "band" not in newsong) or (old_track["band"] == newsong["band"])):
                exists = True
                songlist.append(old_track)
                break
        
        if not exists:
            songlist.append(newsong)
        
    export["songlist"] = songlist
    
    with datapath.open("w", encoding="utf8") as g: 
        g.write(json.dumps(export, indent=4, ensure_ascii=False))