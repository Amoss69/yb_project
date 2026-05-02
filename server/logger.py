from datetime import datetime

ShowLogger = True

LOG_FILE = "server.log"

def log(direction, client, message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #long messages so the log stays readable
    short_msg = message[:100]
    if len(message) > 100:
        short_msg += "..."

    line = f"{time} | {direction} | {client} | {short_msg}"

    # writing to the file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    if ShowLogger == True:
        print(line)
