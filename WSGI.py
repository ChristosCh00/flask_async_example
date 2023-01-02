from flaskasync import app
import threading
import limiter
import atexit 
import time

def close_thread(thread):
    limiter.stop_event.set()
    time.sleep(0.1)# just giving it some time to gracefully stop and print the message


if __name__== '__main__':

    thread=threading.Thread(target=limiter.limit_wrapper,daemon=True)
    thread.start()
    
    atexit.register(close_thread, thread)
    app.run()
    