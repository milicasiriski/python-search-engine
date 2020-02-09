from util.set import MySet


class RankValues:
    def __init__(self, value):
        self._old_value = value
        self._new_value = 0

    @property
    def old_value(self):
        return self._old_value

    @old_value.setter
    def old_value(self, value):
        self._old_value = value

    @property
    def new_value(self):
        return self._new_value

    @new_value.setter
    def new_value(self, value):
        self._new_value = value
