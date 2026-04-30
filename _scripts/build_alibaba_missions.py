"""Generate all mission folders + localisation lines for the Mariana-POV Ali Baba game.

Mission map (after current Mission 1, which is the forest scene):
  M1: forest_outside_cave    - Scene 1 part 1: thieves arrive, Open Sesame   (already authored)
  M2: cave                   - Scene 1 part 2: take gold, agree to silence
  M3: alibaba_house          - Scene 2 part 1: Qasim has discovered the coin
  M4: cave                   - Scene 2 part 2: find Qasim's body
  M5: alibaba_house          - Scene 2 part 3: stage the funeral, hire cobbler
  M6: courtyard_night        - Scene 3 + CHOICE 1 (fire vs trick) + epilogue
  M7: dining_hall            - Scene 4 + CHOICE 2 (Mariana's reply after kill)
  M8: alibaba_house          - Ending + CHOICE 3 (Mariana's reply to wedding)
"""
import os, csv

ROOT = "data/map/preset/1"

def write_csv(path, rows, quote_all=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        q = csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL
        w = csv.writer(f, quoting=q)
        for r in rows:
            w.writerow(r)

EVENT_HDR = ["ID","Text ID","Object","Animation","Type","Trigger","Property"]
CHAR_HDR  = ["Object ID","ID","Camera","Scene","POS","Ground Y POS","Direction","Stage Property"]
OBJ_HDR   = ["ID","Object","Type","POS","Property"]

# helper to build a dialogue event row
def line(key, speaker_obj, portrait, side, speaker_name, timer=5, trigger="", final_interact=None):
    parts = [
        f"timer:{timer}",
        "hold",
        "wait",
        "voice:(Parchment_write;3000;0)",
        f"portrait:{portrait}",
        f"side:{side}",
        f"speaker:{speaker_name}",
    ]
    if final_interact:
        parts = [
            "interact",
            f"start mission:{final_interact}",
            "voice:(Parchment_write;3000;0)",
            f"portrait:{portrait}",
            f"side:{side}",
            f"speaker:{speaker_name}",
        ]
    return ["", key, speaker_obj, "Default", "", trigger, ",".join(parts)]

def music(name="Bluedream"):
    return ["event", "", name, "", "music", "start,all", ""]

def fade_in():
    return ["", "", "camera", "blackout", "cutscene", "", "timer:1,instant fade,wait,fade"]

def fade_out_keep_black():
    return ["", "", "camera", "blackout", "cutscene", "", "timer:2,no auto fade out,wait"]

def end_game():
    return ["", "", "game", "", "end", "", ""]

def choice(key_actor, choice_a, choice_b):
    """Create the choice popup event. Selectable A or B. After click, branch by Trigger='yes'/'no'."""
    return ["", "", key_actor, "Default", "", "",
            f"select:choice,choice_a:{choice_a},choice_b:{choice_b}"]

# ==================== MISSION 2: Cave - take gold ====================
m2_chars = [
    ["Mariana","Trina",1,1,"1300,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"1900,1400","","Right","idle:Default,set layer:2"],
]
m2_events = [EVENT_HDR, music(), fade_in(),
    line("m2/1", "Alibaba", "alibaba_neutral",  "right", "Ali Baba", 6),
    line("m2/2", "Mariana", "marianna_decisive", "left", "Marjana",  7),
    line("m2/3", "Alibaba", "alibaba_neutral",  "right", "Ali Baba", 4),
    line("m2/4", "Mariana", "marianna_neutral", "left", "Marjana",   6),
    line("m2/5", "Alibaba", "alibaba_worried",  "right", "Ali Baba", 5),
    line("m2/6", "Mariana", "marianna_wary",    "left", "Marjana",   7),
    fade_out_keep_black(),
    line("m2/end", "Alibaba", "alibaba_neutral", "right", "Ali Baba", final_interact="3"),
]

# ==================== MISSION 3: Alibaba house - Qasim threat ====================
m3_chars = [
    ["Mariana","Trina",1,1,"1100,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"1500,1400","","Right","idle:Default,set layer:2"],
    ["Qasim","Godrick",1,1,"2400,1400","","Left","idle:Default,set layer:2"],
]
m3_events = [EVENT_HDR, music(), fade_in(),
    line("m3/1", "Alibaba", "alibaba_worried", "right", "Ali Baba", 6),
    line("m3/2", "Mariana", "marianna_wary",   "left",  "Marjana",  4),
    line("m3/3", "Alibaba", "alibaba_worried", "right", "Ali Baba", 6),
    line("m3/4", "Mariana", "marianna_wary",   "left",  "Marjana",  5),
    line("m3/5", "Alibaba", "alibaba_worried", "right", "Ali Baba", 4),
    line("m3/6", "Mariana", "marianna_decisive","left", "Marjana",  4),
    line("m3/7", "Alibaba", "alibaba_worried", "right", "Ali Baba", 4),
    line("m3/8", "Mariana", "marianna_decisive","left", "Marjana",  4),
    fade_out_keep_black(),
    line("m3/end", "Alibaba", "alibaba_worried", "right", "Ali Baba", final_interact="4"),
]

# ==================== MISSION 4: Cave - find Qasim's body ====================
m4_chars = [
    ["Mariana","Trina",1,1,"1100,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"1500,1400","","Right","idle:Default,set layer:2"],
]
m4_events = [EVENT_HDR, music(), fade_in(),
    line("m4/1", "Alibaba", "alibaba_worried", "right", "Ali Baba", 5),
    line("m4/2", "Mariana", "marianna_decisive","left", "Marjana",  6),
    line("m4/3", "Alibaba", "alibaba_worried", "right", "Ali Baba", 4),
    line("m4/4", "Mariana", "marianna_neutral", "left",  "Marjana",  7),
    line("m4/5", "Alibaba", "alibaba_grateful","right", "Ali Baba", 5),
    line("m4/6", "Mariana", "marianna_neutral", "left",  "Marjana",  4),
    fade_out_keep_black(),
    line("m4/end", "Alibaba", "alibaba_worried", "right", "Ali Baba", final_interact="5"),
]

# ==================== MISSION 5: Alibaba house - funeral staging ====================
m5_chars = [
    ["Mariana","Trina",1,1,"1100,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"1500,1400","","Right","idle:Default,set layer:2"],
    ["Tailor","Miquella_doll",1,1,"2400,1400","","Left","idle:Default,set layer:2"],
]
m5_events = [EVENT_HDR, music(), fade_in(),
    line("m5/1", "Mariana", "marianna_decisive","left", "Marjana",   6),
    line("m5/2", "Alibaba", "alibaba_worried", "right", "Ali Baba",  3),
    line("m5/3", "Mariana", "marianna_decisive","left", "Marjana",   6),
    line("m5/4", "Tailor",  "tailor_neutral",  "right", "Baba Mustafa", 5),
    line("m5/5", "Mariana", "marianna_neutral", "left",  "Marjana",   6),
    line("m5/6", "Alibaba", "alibaba_grateful","right", "Ali Baba",  4),
    line("m5/7", "Mariana", "marianna_neutral", "left",  "Marjana",   4),
    fade_out_keep_black(),
    line("m5/end", "Mariana", "marianna_neutral", "left", "Marjana", final_interact="6"),
]

# ==================== MISSION 6: Courtyard - oil jars + CHOICE 1 ====================
# Setup: Mariana is in the courtyard at night. The Captain (disguised) is asleep upstairs.
# A jar whispers "Is it time?". Player chooses A: bluff "Not yet, soon" or B: stay silent and go upstairs.
# Both branches converge at morning.
m6_chars = [
    ["Mariana","Trina",1,1,"1500,1400","","Right","idle:Default,set layer:2"],
    ["Thief","Rabbit_servant",1,1,"2000,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"2700,1400","","Left","idle:Default,set layer:2"],
    ["Captain","Rabbit_leader",1,1,"3100,1400","","Left","idle:Default,set layer:2"],
]
m6_events = [EVENT_HDR, music(), fade_in(),
    # Pre-choice setup
    line("m6/1", "Mariana", "marianna_neutral", "left", "Marjana", 6),
    line("m6/2", "Mariana", "marianna_wary",   "left", "Marjana", 5),
    line("m6/3", "Thief",   "standard_thief_neutral", "right", "Voice in jar", 3),
    line("m6/4", "Mariana", "marianna_wary",   "left", "Marjana", 4),
    # The choice itself
    choice("Mariana", "Whisper: 'Not yet. Soon.'", "Stay silent. Walk away."),
    # ---------- BRANCH A (yes): bluff + fire ----------
    line("m6/A1", "Mariana", "marianna_decisive","left", "Marjana", 4, trigger="yes"),
    line("m6/A2", "Thief",   "standard_thief_neutral", "right", "Voice in jar", 4, trigger="yes"),
    line("m6/A3", "Thief",   "standard_thief_angry", "right", "Another voice", 4, trigger="yes"),
    line("m6/A4", "Mariana", "marianna_decisive","left", "Marjana", 7, trigger="yes"),
    line("m6/A5", "Mariana", "marianna_decisive","left", "Marjana", 6, trigger="yes"),
    line("m6/A6", "Thief",   "standard_thief_angry", "right", "Thief", 4, trigger="yes"),
    line("m6/A7", "Mariana", "marianna_decisive","left", "Marjana", 7, trigger="yes"),
    # ---------- BRANCH B (no): trick + captain kills his own ----------
    line("m6/B1", "Mariana", "marianna_wary",   "left", "Marjana", 4, trigger="no"),
    line("m6/B2", "Mariana", "marianna_decisive","left", "Marjana", 5, trigger="no"),
    line("m6/B3", "Captain", "chief_thief_menacing","right","Captain (Khawaja Husain)", 4, trigger="no"),
    line("m6/B4", "Mariana", "marianna_decisive","left", "Marjana", 8, trigger="no"),
    line("m6/B5", "Captain", "chief_thief_menacing","right","Captain", 4, trigger="no"),
    line("m6/B6", "Mariana", "marianna_decisive","left", "Marjana", 6, trigger="no"),
    line("m6/B7", "Captain", "chief_thief_menacing","right","Captain", 5, trigger="no"),
    # ---------- Convergence (morning) ----------
    line("m6/C1", "Alibaba", "alibaba_worried", "right", "Ali Baba", 5),
    line("m6/C2", "Mariana", "marianna_decisive","left", "Marjana", 4),
    line("m6/C3", "Alibaba", "alibaba_grateful","right", "Ali Baba", 5),
    line("m6/C4", "Mariana", "marianna_neutral", "left",  "Marjana", 6),
    line("m6/C5", "Alibaba", "alibaba_grateful","right", "Ali Baba", 4),
    line("m6/C6", "Mariana", "marianna_neutral", "left",  "Marjana", 5),
    fade_out_keep_black(),
    line("m6/end", "Mariana", "marianna_neutral", "left", "Marjana", final_interact="7"),
]

# ==================== MISSION 7: Dining hall + CHOICE 2 ====================
m7_chars = [
    ["Mariana","Trina",1,1,"1100,1400","","Right","idle:Default,set layer:2"],
    ["Abdullah","Trina_kid",1,1,"1500,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"2000,1400","","Left","idle:Default,set layer:2"],
    ["Son","Miquella_kid",1,1,"2300,1400","","Left","idle:Default,set layer:2"],
    ["Captain","Rabbit_leader",1,1,"2700,1400","","Left","idle:Default,set layer:2"],
]
m7_events = [EVENT_HDR, music(), fade_in(),
    line("m7/1", "Mariana", "marianna_neutral", "left", "Marjana", 6),
    line("m7/2", "Captain", "chief_thief_neutral","right","Khawaja Husain", 4),
    line("m7/3", "Mariana", "marianna_wary",    "left", "Marjana", 5),
    line("m7/4", "Alibaba", "alibaba_grateful", "right","Ali Baba", 5),
    line("m7/5", "Mariana", "marianna_decisive","left", "Marjana", 4),
    line("m7/6", "Mariana", "marianna_decisive","left", "Marjana", 7),  # the strike
    line("m7/7", "Alibaba", "alibaba_worried",  "right","Ali Baba", 4),
    # CHOICE 2
    choice("Mariana", "Open his robe. Look at the dagger.", "I killed the man who murdered your brother."),
    line("m7/A1", "Mariana", "marianna_decisive","left", "Marjana", 5, trigger="yes"),
    line("m7/B1", "Mariana", "marianna_decisive","left", "Marjana", 5, trigger="no"),
    # Both converge
    line("m7/C1", "Alibaba", "alibaba_grateful", "right","Ali Baba", 4),
    line("m7/C2", "Mariana", "marianna_neutral",  "left","Marjana",  4),
    fade_out_keep_black(),
    line("m7/end", "Alibaba", "alibaba_grateful", "right", "Ali Baba", final_interact="8"),
]

# ==================== MISSION 8: Alibaba house - ending + CHOICE 3 ====================
m8_chars = [
    ["Mariana","Trina",1,1,"1300,1400","","Right","idle:Default,set layer:2"],
    ["Alibaba","Miquella",1,1,"2200,1400","","Left","idle:Default,set layer:2"],
]
m8_events = [EVENT_HDR, music(), fade_in(),
    line("m8/1", "Alibaba", "alibaba_grateful", "right","Ali Baba", 5),
    line("m8/2", "Alibaba", "alibaba_grateful", "right","Ali Baba", 8),
    line("m8/3", "Mariana", "marianna_neutral",  "left", "Marjana",  4),
    line("m8/4", "Alibaba", "alibaba_grateful", "right","Ali Baba", 8),
    # CHOICE 3
    choice("Mariana", "I accept. Because this is home.", "I was already family. But yes."),
    line("m8/A1", "Mariana", "marianna_decisive","left", "Marjana", 5, trigger="yes"),
    line("m8/B1", "Mariana", "marianna_decisive","left", "Marjana", 5, trigger="no"),
    # Both converge
    line("m8/C1", "Alibaba", "alibaba_grateful", "right","Ali Baba", 3),
    line("m8/C2", "Mariana", "marianna_neutral",  "left","Marjana",  6),
    fade_out_keep_black(),
    end_game(),
]

# ==================== bg map ====================
mission_bg = {
    "2": "Cave",
    "3": "Alibaba_house",
    "4": "Cave",
    "5": "Alibaba_house",
    "6": "Courtyard_night",
    "7": "Dining_hall",
    "8": "Alibaba_house",
}

mission_data = {
    "2": (m2_chars, m2_events),
    "3": (m3_chars, m3_events),
    "4": (m4_chars, m4_events),
    "5": (m5_chars, m5_events),
    "6": (m6_chars, m6_events),
    "7": (m7_chars, m7_events),
    "8": (m8_chars, m8_events),
}

for m, (chars, events) in mission_data.items():
    base = f"{ROOT}/{m}/1"
    write_csv(f"{base}/object_pos.csv", [OBJ_HDR, [1, mission_bg[m], "scene:1", "1", ""]])
    write_csv(f"{base}/character_pos.csv", [CHAR_HDR] + chars)
    write_csv(f"{base}/event.csv", events)
    print(f"Mission {m}: bg={mission_bg[m]}, chars={len(chars)}, events={len(events)-1}")
print("missions written")
