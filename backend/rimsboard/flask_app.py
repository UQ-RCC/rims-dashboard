"""Initialize Flask app."""
from flask import Flask, jsonify, request

"""
Base app as vanilla flask
with dash app nested inside
"""

import rimsboard.usergather as gather
import rimsboard.rims as rims
import rimsboard.collate as collate

"""Construct core Flask application with embedded Dash app."""
app = Flask(__name__, instance_relative_config=False)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>rimsboard home - backend for rims dashboard</h1>
                <p>A flask api implementation for collating rims data.   </p>'''

@app.route('/api/v1/userlist', methods=['GET'])
def api_getuserlist():

    userlist=collate.populate_userdropdown()

    return jsonify(userlist)

@app.route('/api/v1/getstate', methods=['GET'])
def api_getstate():

    if 'login' in request.args:
        user_login = str(request.args['login'])
    else:
        return "Error: No login field provided. Please specify a login id."
    
    state_core, state_access, state_project = collate.dash_state(user_login)
    
    #TODO not sure i can jsonify a tuple like this
    return jsonify(state_core, state_access, state_project)

@app.route('/api/v1/getuserprojects', methods=['GET'])
def api_getuserprojects():

    if 'login' in request.args:
        user_login = str(request.args['login'])
    else:
        return "Error: No login field provided. Please specify a login id."
    
    user_projects = rims.get_user_projects(user_login)
    
    return jsonify(user_projects)


@app.route('/api/v1/getprojectdetails', methods=['GET'])
def api_getprojectdetails():

    if 'project_num' in request.args:
        project_num = str(request.args['project_num'])
    else:
        return "Error: No login field provided. Please specify a login id."
    
    project_info_df = gather.gather_projectdetails(project_num)
    
    project_info = project_info_df.to_dict('records')

    #TODO: modified -> does not return df anymore, match to dash_app
    return jsonify(project_info)


def entry_dev():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    app.run()