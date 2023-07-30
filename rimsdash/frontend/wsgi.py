from frontend.user_app import app, server

if __name__ == "__main__":
    app.run_server(debug=False, dev_tools_hot_reload=False, host='0.0.0.0', port=8050)