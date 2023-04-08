from EventManager.Event import Event


class LoadSave(Event):
    def __init__ (self, saveName):
        self.saveName = saveName
        self.name = "Exit event"

class ExitEvent(Event):
    """
    Exit event.
    ExitEvent exit the game.
    ExitEvent is not QuitEvent.
    """
    
    def __init__ (self):
        self.name = "Exit event"

class QuitEvent(Event):
    """
    Quit event.
    QuitEvent change state to STATE_QUIT.
    QuitEvent is not ExitEvent.
    """
    
    def __init__ (self):
        self.name = "Quit event"
    
class LoadEvent(Event):
    def __init__ (self):
        self.name = "Loadevent"

class JoinIPEvent(Event):
    def __init__ (self):
        self.name = "JoinIPEvent"

class JoinLocalNetworkEvent(Event):
    def __init__ (self):
        self.name = "JoinLocalNetworkEvent"

class TickEvent(Event):
    """
    Tick event.
    """
    
    def __init__ (self):
        self.name = "Tick event"
    
    
class InputEvent(Event):
    """
    Keyboard or mouse input event.
    """
    
    def __init__(self, unicodechar, clickpos):
        self.name = "Input event"
        self.char = unicodechar
        self.clickpos = clickpos
    def __str__(self):
        return '%s, char=%s, clickpos=%s' % (self.name, self.char, self.clickpos)
    
    
class InitializeEvent(Event):
    """
    Tells all listeners to initialize themselves.
    This includes loading libraries and resources.
    
    Avoid initializing such things within listener __init__ calls 
    to minimize snafus (if some rely on others being yet created.)
    """
    
    def __init__ (self):
        self.name = "Initialize event"


class StateChangeEvent(Event):
    """
    Change the model state machine.
    Given a None state will pop() instead of push.
    """
    
    def __init__(self, state):
        self.name = "State change event"
        self.state = state
    def __str__(self):
        if self.state:
            return '%s pushed %s' % (self.name, self.state)
        else:
            return '%s popped' % (self.name, )