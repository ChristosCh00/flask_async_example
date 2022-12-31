from flaskasync import app
import threading
import limiter

thread=threading.Thread(target=limiter.limit_wrapper)
thread.start()



if __name__== '__main__':
    app.run()