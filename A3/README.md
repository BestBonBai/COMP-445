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
- logging

### list files:
- httpc.py
- HttpClient.py
- httpfs.py
- HttpServer.py
- FileManager.py
- config.py
- packet.py
- Window.py
- UdpLibrary.py
- [router]
    - router (Need to Install Go)
- [data]

### Usage of Assignment 3
1. Step 1: Run the router on the same or different host
   - See the router's README
   ### Test cases
   - run `./router`
   - run ` ./router --port=3000 --drop-rate=0.2 --max-delay=10ms --seed=1 `



2. Step 2: Run the server
   run `python httpfs.py`, follow the prompt (`httpfs`), input one of the following test codes:
    - `httpfs` ( empty line uses default parameters)
    - `httpfs -v`
    - `httpfs -v -p 8080`
    - `httpfs -v -p 8080 -d data`

3. Step 3: Run the client
   run `python httpc.py`, follow the prompt (`httpc`), input one of the following test codes:
   - **NOTE** You need to send your msg when `httpfs` is listening port instead of **TimeOut**
## Some Test Cases of HttpClient
### Basic Get
- get -v 'http://localhost:8080/get?course=networking&assignment=1'
- get -v -h key1:value1 'http://localhost:8080/get?course=networking&assignment=1'

### Get File Manager
- get 'http://localhost:8080/'
- get -v 'http://localhost:8080/'
- get -v 'http://localhost:8080/foo' (Server uses default dir `data`)
- get -v 'http://localhost:8080/../README.md' (Test Secure Access: Server uses default dir `data`)[Method : Check path is correct]

### Post File Manager
- post -h Content-Type:application/json -d '{"Assignment": 2}' http://localhost:8080/bar

#### Test: Invalid woring directory
- post -h Content-Type:application/json -d '{"Assignment": 2}' http://localhost:8080/../bbb
#### Test: File Not Found Error, even through in valid working directory.
- post -h Content-Type:application/json -d '{"Assignment": 2}' http://localhost:8080/data3/bbb

### Get different Content Type
- get -h Content-Type:application/json 'http://localhost:8080/'

### Content-Disposition
- get -v -h Content-Disposition:inline 'http://localhost:8080/download'
