"""Initialize Flask app."""
from flask import Flask, jsonify, request
from flask_cors import CORS

import sys
import rimsboard.usergather as gather
import rimsboard.rims as rims
import rimsboard.collate as collate

"""Construct core Flask application with embedded Dash app."""
app = Flask(__name__, instance_relative_config=False)
CORS(app)

#prevent flask.jsonify reordering dicts
# we are passing into python atm, dicts should retain order
app.json.sort_keys = False

print("START", file=sys.stderr)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>rimsboard home - backend for rims dashboard</h1>
                <p>A flask api implementation for collating rims data.   </p>'''

@app.route('/api/v1/userlist', methods=['GET'])
def api_getuserlist():

    userlist=collate.populate_userdropdown()

    return jsonify(userlist)

@app.route('/api/v1/state', methods=['GET'])
def api_getstate(): #expects user_login

    try:
        print("received call for state", file=sys.stderr)
        if 'login' in request.args:
            print(str(request.args['login']), file=sys.stderr)
            user_login = str(request.args['login'])
        else:
            return "Error: No login field provided. Please specify a login id."
        
        state = collate.state_from_user(user_login)  #dict
        print(state)
    
        return jsonify(state)
    
    except:
        return f"Error: could not generate state for login {user_login}."

@app.route('/api/v1/userprojects', methods=['GET'])
def api_getuserprojects():  #expects user_login

    print(f"received: {request.args}")    

    if 'login' in request.args:
        user_login = str(request.args['login'])
    else:
        return "Error: No login field provided. Please specify a login id."
    
    user_projects = rims.get_user_projects(user_login)
    
    return jsonify(user_projects)

@app.route('/api/v1/projectdetails', methods=['GET'])
def api_getprojectdetails():    #expects project_number

    print(f"received: {request.args}")    

    if 'project_number' in request.args:
        project_number = int(request.args['project_number'])
        print(f"received: {project_number}")            
    else:
        return "Error: No login field provided. Please specify a login id."
    
    #here we create a df from a json then convert back to dict-list after
    #should just drop the df intermediary
    project_info_df = gather.gather_projectdetails(project_number)
    
    project_info = project_info_df.to_dict('records')

    return jsonify(project_info)

def check_inputs():
    userlist=collate.populate_userdropdown()
    user_login='myusername'
    user_projects = rims.get_user_projects(user_login)
    #state_core, state_access, state_project = collate.dash_state(user_login)
    states = collate.dash_state(user_login)
    project_number=user_projects[0]
    project_info_df = gather.gather_projectdetails(project_number)
    project_info = project_info_df.to_dict('records')

def entry_dev():
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    entry_dev()
    #app.run()