import time
from dataclasses import dataclass, field
from flask import Flask, jsonify

app = Flask(__name__)

@dataclass
class Lap:
    lap_index:int
    lap_elapsed_ms:int
    total_elapsed_ms:int

@dataclass
class Timer:
    state:str="stopped"
    start_ts:float|None=None
    elapsed_ms:int=0
    laps:list=field(default_factory=list)

    def now(self):
        if self.state!="running" or self.start_ts is None:
            return self.elapsed_ms
        return int((time.time()-self.start_ts)*1000)

T=Timer()

@app.get("/health")
def health():
    return jsonify({"status":"ok"}),200

@app.get("/timer")
def get_timer():
    return jsonify({"state":T.state,"elapsed_ms":T.now(),"laps":[l.__dict__ for l in T.laps]}),200

@app.post("/timer/start")
def start():
    if T.state=="running":
        return jsonify({"error":"ALREADY_RUNNING"}),409
    T.state="running"; T.start_ts=time.time(); T.elapsed_ms=0; T.laps=[]
    return jsonify({"state":"running","elapsed_ms":0}),200

@app.post("/timer/stop")
def stop():
    if T.state!="running":
        return jsonify({"error":"ALREADY_STOPPED"}),409
    T.elapsed_ms=T.now(); T.state="stopped"; T.start_ts=None
    return jsonify({"state":"stopped","elapsed_ms":T.elapsed_ms}),200

@app.post("/timer/lap")
def lap():
    if T.state!="running":
        return jsonify({"error":"NOT_RUNNING"}),409
    total=T.now()
    lap_elapsed= total if not T.laps else total-T.laps[-1].total_elapsed_ms
    idx=len(T.laps)+1
    T.laps.append(Lap(idx,lap_elapsed,total))
    return jsonify({"lap_index":idx,"lap_elapsed_ms":lap_elapsed,"total_elapsed_ms":total}),201

@app.post("/timer/reset")
def reset():
    if T.state=="running":
        return jsonify({"error":"CANNOT_RESET_WHILE_RUNNING"}),409
    T.state="stopped"; T.start_ts=None; T.elapsed_ms=0; T.laps=[]
    return jsonify({"state":"stopped","elapsed_ms":0,"laps":[]}),200
