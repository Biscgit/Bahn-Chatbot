# Deutsche Bahn ChatBot

---
Quick overview of this Chatbot

### Functionality:
The bot's purpose is to give information about trains and routes.
It is connected to the DB-api to get access to real time data.
It can be expanded via the files in `app/language/`. 
Since the requests are quite complex, having only a simple json is not enough,
but instead patterns and responses can be added in the above-mentioned files.
The bot first analyzes the message for persistent information with `memorypatterns.py`
to update the chat data and then the action that corresponds to the message with 
`messagepatterns.py`.

Chatdata is stored for each user and is empty at the beginning. 
Through conversation, it gets updated, or the bot asks if something hasn't been provided yet
By sending `bye` (or `clear`, `reset`, ...) the memory for that chat gets reset.

The patterns work with regex and tokens to return a message which here is represented with multiple
messages that get returned with collision resistance.
Most messages are generated during runtime (i.e. filled with results and data)
It can also repeat tasks with different information which gets checked before returning a message. 

Check descriptions above functions for more detailed information on how they work 
as well as the examples below.

*Note: when typing exact station names, be careful with upper and lowercase because the api cannot
differentiate between them sadly. 
When using city names (i.e. Plattling) I implemented a fix so that it works with lowercase too.*

### Design
The design is responsive and functional.
The colors are inspired by the ICE train with colors mostly from [official DB colors](
https://marketingportal.extranet.deutschebahn.com/marketingportal/Marke-und-Design/Basiselemente/Farbe).
It has small details like the shadows on messages and overflow as well as the top bar with clickable urls.

### Setup:
- install `python 3.11 or higher` (preferably in `venv`)
- install packages `python3.11 -m pip install -r requirements.txt`
- create an DB api account ([tutorial](`https://developers.deutschebahn.com/db-api-marketplace/apis/start`))
- create an applications with `Timetables API` (free) and save id and key
- fill in DB-Api credentials [here](config/DBapi.toml) (`config/DBapi.toml`)
- run program with `python3.11 main.py`
- navigate to website [here](http://127.0.0.1:8000) (also in logging messages)

### Example questions (conversation in order):
- hello!
- what can you do?
- show me the route of RE3 
- \> Plattling
- How can I get from Passau to Deggendorf?
- Can I bring dogs with me?
- bgiejpfoejgüp
- Which trains leave from Passau at 5pm?
- and from Plattling?
- and right now?
- show me the distance to Berlin
- show the route of WBARB35
- how can i get from Plattling to München?
- reset
- how can I get to Düsseldorf?
- \> Köln
- give me a train fact
- another one
- bye!

### Note
Backend needs some cleanup and isn't perfect.
This should not be used as a base for further projects!
