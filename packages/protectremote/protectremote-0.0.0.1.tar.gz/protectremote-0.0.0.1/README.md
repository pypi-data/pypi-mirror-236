# ProtectRemote

next-gen security solution for remote workers

## Install 

```
pip install protectremote
```

## Usage


### FLASK

#### Protect all routes

```python
from flask import Flask
from protectremote import ProtechRemoteMiddleware

app = Flask(__name__)

app.wsgi_app = ProtechRemoteMiddleware(app.wsgi_app)


@app.route('/')
def public():
    return 'Hello'


@app.route('/secured')
def secured():
    return 'secured'

 
if __name__ == '__main__':  
   app.run()

```


#### Protect specific route only


```python
from flask import Flask
from protectremote import pr_access

app = Flask(__name__)


@app.route('/')
def public():
    return 'Hello'


@app.route('/secured')
@pr_access()
def secured():
    return 'secured'

 
if __name__ == '__main__':  
   app.run()

```

### DJANGO



