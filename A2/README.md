### Required Environment
- python 3.7

### lists of libaries
- socket
- argparse
- cmd
- sys
- re
- urllib.parse
- json
- threading

### list files:
- httpc.py
- HttpClient.py
- httpfs.py
- HttpServer.py
- FileManager.py

### Usage of Assignment 2
1. `cd` into the folder `A2`
2. run `python httpfs.py`, follow the prompt (`httpfs`), input one of the following test codes:
    - `httpfs` ( empty line uses default parameters)
    - `httpfs -v -p 8080`
    - `httpfs -v -p 8080 -d data`
3. add new terminal, `cd` into the folder `A1`, run `python httpc.py`, follow the prompt (`httpc`), input one of the following test codes:
    - get 'http://localhost:8080/'
    - get -v 'http://localhost:8080/'
    - get -h Content-Type:application/json 'http://localhost:8080/'
    - get -h Content-Type:text/xml 'http://localhost:8080/'

    - get -v 'http://localhost:8080/foo'
    - get -h Content-Disposition:inline 'http://localhost:8080/filename'
    - get -v -h 'http://localhost:8080/../foo'
    - get -h Content-Disposition:inline 'http://localhost:8080/filename'

    - post -h Content-Type:application/json -d '{"": "somethingelse"}' http://localhost:8080/bar