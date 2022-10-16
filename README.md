# buro

Launch:
    1) python ./src/device_server.py
    2) python ./src/rest_api_server_main.py

        Then can be called commands:

        curl http://0.0.0.0:5555/get_values/1
        curl -X POST http://0.0.0.0:5555/start_channel/1/100.1/220.1
        curl http://0.0.0.0:5555/get_values/1
        curl -X POST http://0.0.0.0:5555/disable/1

Tests 
    pytest
