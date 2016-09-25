from flask import Flask, abort, request
from time import gmtime, strftime
import subprocess
import json
import os

def output_log(str):
    f=open(config['server']['log_path']+"log.txt",'a')
    f.write(str+'\n')
    f.close()
    return


with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__)

@app.route('/webhook/<hook_name>', methods=['POST'])
def webhook(hook_name):
    if config["webhooks"].get(hook_name)==None:
         abort(404)

    if config["webhooks"][hook_name]["type"]=="git@osc":
        post_data = json.loads(request.form['hook'])

        if post_data["password"]!=config["webhooks"][hook_name]["key"]:
            abort(403)
            
        time_str = strftime("%Y-%m-%d.%H.%M.%S", gmtime())
        output_log(time_str + "  " + hook_name)
        detail_log_path = os.path.abspath(config['server']['log_path']+time_str+".txt")
        cmd_line = "cd " + config["webhooks"][hook_name]["local_path"]
        cmd_line = cmd_line + "|git pull >"+detail_log_path;

        subprocess.Popen(cmd_line, shell=True)
    else:
        abort(403)






    return "Success"

if __name__ == "__main__":
    app.debug = config['server']['debug']
    app.run(host=config['server']['host'], port=config['server']['port'])
