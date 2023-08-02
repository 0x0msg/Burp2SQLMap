# Burp2SQLMap

This tool is developed with help of ChatGPT 3.5 from OpenAI. The intention of developing this plugin was to satisfy a requirement where we need to regularly scan different endpoint in SQLMap and everytime we had to save the file and run it. 

With this, just sending the request will run sqlmap automaticall.

Please note, if you wish to change the arguments of sqlmap, change it in sql.py file.

Steps to run the tool:

1.) Load burp_plugin.py in Burp Suite. Make sure Jython is configured
2.) Run the server.py file i.e; python3 server.py
3.) Send the request to the loaded plugin and you should have sqlmap running

Pre-requisite:
1.) SQLMap installed on the machine and accessible from command line from anywhere
2.) Python 3
