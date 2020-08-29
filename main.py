from flask import Flask, request, jsonify
import json,traceback,os
from Services import ConnectionHandler
from concurrent.futures import ThreadPoolExecutor, wait
from Services.FileUtils import fileToJson

app = Flask(__name__)


def rsync(machine_details, copy_from,copy_to):
    connect_handler = ConnectionHandler.ConnectionHandler(machine_details)
    return connect_handler.rsync(copy_from,copy_to)


@app.route('/copy', methods = ['POST'])
def run_command():
    try:
        
        #GET DATEILS
        data = request.get_json()
        avl_machines = fileToJson("targets.json")
        machine_list = data.get("machine_list",[])
        copy_from = data.get("copy_from")
        copy_to = data.get("copy_to")

        #get machines
        for index,machine in enumerate(machine_list):
            found = False
            for mc in avl_machines:
                if mc["machine_name"] == machine:
                    machine_list[index] = mc
                    found = True
            if not found: raise Exception("Declaration not found for "+machine)
            
        #RUN COMMAND             
        pool = ThreadPoolExecutor(5)
        futures = []
        for index,machine in enumerate(machine_list):            
            machine_list[index]["future"]=pool.submit(rsync,machine,copy_from,copy_to)
            futures.append(machine_list[index]["future"])
        wait(futures)
        
        #GENERATE RESULTS        
        for index,machine in enumerate(machine_list):
            if machine_list[index]["future"].exception():
                machine_list[index]["result"]="failed"
                machine_list[index]["result_message"]=str(machine_list[index]["future"].exception())
                machine_list[index]["compare"]="NA"
            else:
                machine_list[index]["result"]="success"
                machine_list[index]["result_message"]=machine_list[index]["future"].result()
                machine_list[index]["compare"]="NA"
            machine_list[index].pop("future")
        
        #RETURN RESULTS    
        return json.dumps({"result":"success","machine_list":machine_list}), 200
    except Exception as e:  # catch *all* exceptions
        traceback.print_exc()
        return jsonify({"result": "failed", "message": str(e)}), 404
    
    

if __name__ == '__main__':
    app.run(port=1012,host='0.0.0.0')