from firebase_admin import db
from utils.firebase.firebase_decorators import log_firebase_operation

class ReferenceWrapper:
    def __init__(self, path: str, app):
        self._ref = db.reference(path, app=app)
        self._path = path
        self._app = app

    @log_firebase_operation
    def get(self):
        return self._ref.get()

    @log_firebase_operation
    def set(self, value):
        return self._ref.set(value)

    @log_firebase_operation
    def update(self, value):
        return self._ref.update(value)

    @log_firebase_operation
    def delete(self):
        return self._ref.delete()

    def child(self, path_segment: str):
        return ReferenceWrapper(f"{self._path}/{path_segment}", app=self._app)

    def push(self, value=None):
        if value:
            @log_firebase_operation
            def push_op():
                return self._ref.push(value)
            return push_op()
        return self._ref.push()

