import threading, Queue
import time

__author__ = 'Maxime'


class RequestHandler(object):
    def __init__(self, config):
        self.config = config
        self.post_queue = Queue.Queue()
        self.kill_switch = threading.Event()
        self.post_thread = threading.Thread(name='innerthread',
                                            target=self.do_long_action)
        self.post_thread.start()

    def post(self, action):
        self.post_queue.put(action)

    def do_long_action(self):
        while not self.kill_switch.isSet():
            try:
                elem = self.post_queue.get(True, timeout=2)
                print "Action started", self.config['name'], elem
                time.sleep(10)
                print "Action ended", self.config['name'], elem
            except Queue.Empty:
                pass
        print "I", self.config['name'], "got killed!"
    def stop(self):
        print "Killing thread", self.config['name']
        self.kill_switch.set()



class Dispatcher(object):
    def __init__(self, configs):
        self.dispatch = {}
        for config in configs:
            self.dispatch[config['name']] = RequestHandler(config)

    def post(self, postvars):
        print postvars
        if postvars['test'][0] == 'stop':
            self.dispatch[postvars['name'][0]].stop()
        self.dispatch[postvars['name'][0]].post(postvars['test'][0])
        return postvars['test']
