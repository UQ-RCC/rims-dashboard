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

@app.route('/rapi/v1/userlist', methods=['GET'])
def api_getuserlist():

    userlist=collate.populate_userdropdown()

    return jsonify(userlist)


@app.route('/rapi/v1/userprojects', methods=['GET'])
def api_getuserprojects():  #expects user_login

    print(f"received: {request.args}")    

    if 'login' in request.args:
        user_login = str(request.args['login'])
    else:
        return "Error: No login field provided. Please specify a login id."
    
    user_projects = rims.get_user_projects(user_login)
    
    return jsonify(user_projects)

@app.route('/rapi/v1/projectdetails', methods=['GET'])
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




@app.route('/rapi/v1/userstate', methods=['GET'])
def api_getuserstate(): #expects user_login

    try:
        print("received call for user state", file=sys.stderr)
        if 'login' in request.args:
            print(str(request.args['login']), file=sys.stderr)
            user_login = str(request.args['login'])
        else:
            return "Error: No login field provided. Please specify a login id."
        
        result = collate.get_user_indicators(user_login)  #dict
    
        print(result)

        return jsonify(result)
    
    except:
        return f"Error: could not generate user state for login {user_login}."

@app.route('/rapi/v1/allprojectstates', methods=['GET'])
def api_getallprojectstates(): 

    try:
        print("received call for all project states", file=sys.stderr)
        
        result = collate.get_all_project_states()  #list of dicts
    
        return jsonify(result)
    
    except:
        return f"Error: could not generate project states."


@app.route('/rapi/v1/userprojectstates', methods=['GET'])
def api_getuserprojectstates(): #expects user_login

    try:
        print("received call for user project states", file=sys.stderr)
        if 'login' in request.args:
            print(str(request.args['login']), file=sys.stderr)
            user_login = str(request.args['login'])
        else:
            return "Error: No login field provided. Please specify a login id."
        
        result = collate.get_user_project_indicators(user_login)  #dict
    
        return jsonify(result)
    
    except:
        return f"Error: could not generate project states for login {user_login}."


@app.route('/rapi/v1/defaultuserstate', methods=['GET'])
def api_defaultuserstate():

    try:
        result = collate.get_default_user_indicator()  #dict

        return jsonify(result)
    
    except:
        return f"Error: could not generate default user state."


@app.route('/rapi/v1/defaultuserprojectstates', methods=['GET'])
def api_defaultprojectstates():

    try:
        result = [ collate.get_default_project_indicator() ] #dict
       # result.append(collate.get_default_project_indicator())  

        return jsonify(result)
    
    except:
        return f"Error: could not generate default project states."

@app.route('/rapi/v1/defaultprojectstate', methods=['GET'])
def api_defaultprojectstate():

    try:
        result = collate.get_default_project_indicator()  #dict

        return jsonify(result)
    
    except:
        return f"Error: could not generate default project state."


@app.route('/rapi/v1/checkadminbyemail', methods=['GET'])
def api_adminstatusbyemail(): #expects email

    try:
        print("received admincheck request", file=sys.stderr)

        if 'email' in request.args:
            print(f"recived args: {str(request.args['email'])}", file=sys.stderr)
            email = str(request.args['email'])
        else:
            return "Error: No email field provided. Please specify an email."

        _login = collate.user_from_email(email)['login']
        print(f"user {_login}")
        result = collate.admin_status(_login)  #dict

        print(f"returning {result}")

        return jsonify(result)
    
    except:
        return f"Error: could not check admin status for email {email}"

@app.route('/rapi/v1/userfromemail', methods=['GET'])
def api_userbyemail(): #expects email

    try:
        print("received login name request", file=sys.stderr)

        if 'email' in request.args:
            print(f"recived args: {str(request.args['email'])}", file=sys.stderr)
            email = str(request.args['email'])
        else:
            return "Error: No email field provided. Please specify an email."

        result = collate.user_from_email(email)  #dict

        print(f"returning {result}")

        return jsonify(result)
    
    except:
        return f"Error: could not check admin status for email {email}"




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