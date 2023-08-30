from dashboard.dash_app import dash_app, server

if __name__ == "__main__":
    dash_app.run(debug=False, host='0.0.0.0', port=8050)