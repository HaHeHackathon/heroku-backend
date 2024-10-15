import datetime

headers = {"DB-Client-Id": "78f5e6d753d9110fad7d552f77faf349",
"DB-Api-Key": "10b8b934a69e7b096286e18e057df47b"}


current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

params = {"timeStart": current_time}