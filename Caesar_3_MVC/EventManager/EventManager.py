from EventManager.allEvent import TickEvent
from weakref import WeakKeyDictionary


class EventManager(object):
    """
    We coordinate communication between the Model, View, and Controller.
    """
    
    def __init__(self):
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        """ 
        Adds a listener to our spam list. 
        It will receive Post()ed events through it's notify(event) call. 
        """
        
        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        """ 
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        
        if listener in self.listeners.keys():
            del self.listeners[listener]
        
    def Post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """
        
        if not isinstance(event, TickEvent):
            # print the event (unless it is TickEvent)
            print(str(event))
        for listener in self.listeners.keys():
            listener.notify(event)