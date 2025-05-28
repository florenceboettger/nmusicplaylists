import json
import math
from pathlib import Path

path = Path("...")

with path.open("r", encoding="utf8") as f:    
    alltracks = json.loads(''.join(f.readlines()))
    export = {
        "uuid": alltracks["id"],
        "thumbnail": "",
        "introduction": ""
    }

    songlist = []
    for track in alltracks["tracks"]:
        newsong = {}
        split = track["name"].split(" / ", 1)
        newsong["name"] = split[0]
        if len(split) > 1:
            newsong["band"] = split[1]
            newsong["formattedband"] = split[1]
        newsong["formattedname"] = newsong["name"]
        newsong["id"] = track["id"]
        newsong["extend"] = track["media"]["payloadList"][0]["containsLoopableMedia"]
        milliDuration = track["media"]["payloadList"][0]["durationMillis"]
        minuteDuration = milliDuration // 60000
        secondDuration = math.ceil((milliDuration % 60000) / 1000)
        newsong["length"] = f"{minuteDuration}:{secondDuration:02d}"
        songlist.append(newsong)
        
    export["songlist"] = songlist

    datapath = Path(__file__).resolve().parent / "data" / "Splatoon" / "alltracks.json"

    with datapath.open("w", encoding="utf8") as g:        
        g.write(json.dumps(export, indent=4, ensure_ascii=False))