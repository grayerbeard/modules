# This app renders an index page and several other pages
# to allow settings to be changes or
# information to be displayed
# The Pages are
#   Index
#   Mode Selection
#   Control Parameter Editing
#   Schedule Editing
#   Display Current System Status
#   Display Logging Data with Recent Data as a Table

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', message='Welcome to my app!')

@app.route('/set_mode', methods=['POST'])
def set_mode():
    # Get the selected mode from the form data
    mode = request.form['mode']
    
    # Save the selected mode to the YAML data
    config_data['Current Mode'] = mode
    
    # Save the updated YAML data to a file
    with open('config.yaml', 'w') as file:
        yaml.dump(config_data, file)
    
    # Redirect to a page that displays the current mode
    return redirect(url_for('current_mode'))

@app.route('/parameters', methods=['GET', 'POST'])
def edit_control_parameters():
    parameters = config_data['Control Parameters']
    
    if request.method == 'POST':
        # Update the control parameters in the YAML data
        for key in parameters.keys():
            if key in request.form:
                parameters[key] = int(request.form[key])
        
        # Save the updated YAML data to a file
        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)
        
        # Return a message indicating that the parameters were updated
        return 'Control parameters updated'
    else:
        # Render the form for editing the control parameters
        return render_template('control_parameters.html', parameters=parameters)

@app.route('/schedule', methods=['GET', 'POST'])
def edit_control_parameters():
    parameters = config_data['Control Parameters']
    
    if request.method == 'POST':
        # Update the control parameters in the YAML data
        for key in schedule.keys():
            if key in request.form:
                parameters[key] = int(request.form[key])
        
        # Save the updated YAML data to a file
        with open('config.yaml', 'w') as file:
            yaml.dump(config_data, file)
        
        # Return a message indicating that the parameters were updated
        return 'Schedule updated'
    else:
        # Render the form for editing the control parameters
        return render_template('schedule.html', parameters=parameters)

@app.route('/status', methods=['GET', 'POST'])
def edit_control_parameters():

return render_template('status.html', data = data)

if __name__ == '__main__':
    app.run()
