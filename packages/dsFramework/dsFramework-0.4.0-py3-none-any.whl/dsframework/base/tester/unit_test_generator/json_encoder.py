from json import JSONEncoder


class SanitizerEncoder(JSONEncoder):

    def default(self, obj):

        if isinstance(obj, set):
            return list(obj)

        if type(obj).__name__ == 'Pattern':
            return {'pattern': obj.pattern}

        if hasattr(obj, '__dict__'):
            return obj.__dict__

        return super().default(obj)
