class JSMessage(object):
    @staticmethod
    def success(message, success=True):
        return {'alert_type': 'alert-success', 'message': message, 'success': success}

    @staticmethod
    def error(message, success=True):
        return {'alert_type': 'alert-warning', 'message': message, 'success': success}
