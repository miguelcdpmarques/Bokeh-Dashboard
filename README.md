# Bokeh Dashboard

This repo contains an example of the implementation of a Python dashboard using the Bokeh library. It is deployed using a simple Flask app. For styling, Bootstrap was used as a convenient and practical way to add attractive layout to Flask apps.



## Running the Dashboard

There are only a few steps required to run this implementation of a Bokeh dashboard on your local machine. The steps are the following:

1. Clone this repo
2. Make sure you have a virtual environment with <em>flask</em> and <em>bokeh</em> installed.
2. Open two windows of the command terminal (or equivalent for your OS) in the directory of this project, using the virtual environment from the previous step.
3. In the first window run the command "bokeh serve --allow-websocket-origin=127.0.0.1:5000 res_operacionais.py"
4. In the second window run the command "python app.py"
5. Finally, open the localhost - usually at http://127.0.0.1:5000/


