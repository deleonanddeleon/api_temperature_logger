# api_isp_outage_logger
## ISP Outage Logger API in Python Flask with MongoDB

- API for logging ISP outages, replaces json-server
- Gunicorn is a popular WSGI server for running Python web applications, and Flask is a lightweight web framework for Python. 
- The Flask app runs in a virtual environment with a WSGI entry point
- Gunicorn is bound to a network socket (Unix sockets do not appear to work with GCP)
- nginx is configured to run as a reverse proxy
- MongoDB is the database
- systemd service ensures there is persistence through server reboots