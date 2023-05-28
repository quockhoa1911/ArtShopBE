from threading import Thread


class Multi_Thread(Thread):

    # kwargs is dict , **kwargs unpack dict-> get key value -> param of function is key,value
    def __init__(self, target, **kwargs):
        Thread.__init__(self)
        self._target = target
        self._kwargs = kwargs

    def run(self) -> None:
        self._target(**self._kwargs)
        del self._target, self._kwargs
