import fastapi
from fastapi import FastAPI, Request, HTTPException
from supabase import create_client, Client
import json
from dotenv import load_dotenv
import supabase,os



load_dotenv('.env')

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)
app = FastAPI()



def load_json():
    with open('highscores.json','r') as f:
        data = json.load(f)
    return data

def dump_json(dat):
    with open('highscores.json','w') as f:
         json.dump(dat, f, indent=4)


scores = load_json()

@app.get("/")
async def root():
    resp =  supabase.from_('profiles').select("*").execute()
    profiles = resp.model_dump()['data']
    sorted_profiles = sorted(profiles, key=lambda x: x['highscore'], reverse=True)
    score_str = ""
    for profile in sorted_profiles:
        usr  = profile["username"]
        hscr = profile["highscore"]
        score_str += f"{usr}:{hscr}\n\n"
    return {"scoreStr":score_str}


@app.post('/update')
async def update_score(request:Request):
    profile  = await request.json()
    resp =  supabase.from_('profiles').select("*")\
    .eq('username',profile['name']).execute()
    profiles = resp.model_dump()['data']
    print(profiles)

    
    if len(profiles) == 0:
        supabase.from_('profiles').insert({
            "username":profile['name'],
            "highscore":profile['score']
        }).execute()
    else:
        prof = profiles[0]
        if prof['highscore'] < profile['score']:
             supabase.from_('profiles').update({'highscore': profile['score']}).eq('id', prof['id']).execute()
    return {"msg":"Score updated"}

       # if scores['highscores'][profile['name']] < profile['score']:
       #     scores['highscores'][profile['name']] = profile['score']
       #     dump_json(scores)
       # return {"msg":"Score Updated"}


    

    # {name:"Shao","score":0}