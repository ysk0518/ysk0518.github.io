#!/usr/bin/env python3
import subprocess
import urllib
import urllib.request
import json
import time
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

api_url ="https://nityc-nyuta.work/procon30-battle-api"
battle_id = ""
token = ""
output_dir = "./test_dir"
turns = 0
max_turn = 0

def get_data_from_stdin():
    global battle_id, token
    print("Battle ID : ", end="")
    battle_id = input()
    print("Token : ", end="")
    token = input()
    print()

def get_data():
    global battle_id,token,output_dir
    get_battle = urllib.request.Request(url=api_url+"/battle/"+str(battle_id))
    get_matche = urllib.request.Request(url=api_url+"/matches/"+str(battle_id), headers={"Authorization": token})
    post_matches = urllib.request.Request(url=api_url+"/matches", headers={"Authorization": token})
    try:
        res_get_battle = urllib.request.urlopen(get_battle).read().decode()
        res_get_matches = urllib.request.urlopen(get_matche).read().decode()
        res_post_matches = urllib.request.urlopen(post_matches).read().decode()
        res_post_matches = list(filter(lambda n: n["id"] == int(battle_id), json.loads(res_post_matches)))[0]
    except Exception as e :
        print("Errorじゃ、ボケ！！ : ",e)
        return
    res_get_battle = json.loads(res_get_battle)
    res_get_matches = json.loads(res_get_matches)
    res_get_battle.update(res_post_matches)
    with open(output_dir+"/battle.json", "w") as f:
        f.write(json.dumps(res_get_battle))
    with open(output_dir+"/game.json", "w") as f:
        f.write(json.dumps(res_get_matches))

    return res_get_battle, res_get_matches

def master_process():
    # Setup data
    global turns,max_turn
    print("[INFO] データ取得中...")
    battle_data, match_data = get_data()
    teamA = battle_data["teamID"]
    teamB = battle_data["teamA"] if battle_data["teamB"] == teamA else battle_data["teamB"]
    turns = match_data["turn"]
    max_turn = battle_data["turns"]
    cpu_limit = "80"
    mem_limit = "5120000"
    command = ["./simple-master.py", battle_id, token]
    res = subprocess.run(command, stdout=subprocess.PIPE)

if __name__ == "__main__":
    get_data_from_stdin()
    while (1):
        if turns <= max_turn:
            master_process()
            time.sleep(5)
        else:
            break
