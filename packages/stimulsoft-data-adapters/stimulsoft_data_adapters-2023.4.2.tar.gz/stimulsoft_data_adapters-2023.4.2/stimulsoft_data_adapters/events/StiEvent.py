from .StiEventArgs import StiEventArgs

class StiEvent:

### Private

    __handlers: list = None
    __name: str = None


### Properties

    @property
    def count(self):
        return len(self.__handlers or '')
    
    @property
    def name(self):
        return self.__name
    
    @property
    def handlers(self):
        return self.__handlers
    

### Override

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self
    
    def __isub__(self, handler):
        self.handlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for handler in self.handlers:
            if (callable(handler)):
                if isinstance(args, StiEventArgs):
                    args.event = self.name[2:]
                handler(*args, **keywargs)

    def __init__(self, name: str):
        self.__handlers = []
        self.__name = name
	