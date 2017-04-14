#!flask/bin/python
from app import app

import sys
sys.path.insert(0, "/app/")


from app import app
application = app
if __name__ == '__main__':
	application.run(host='0.0.0.0', threaded = True)
