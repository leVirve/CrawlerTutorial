class Push():

    def __init__(self, **kwargs):
        self.author = kwargs.get('author')
        self.content = kwargs.get('content')
        self.datetime = kwargs.get('datetime')
        self.push = kwargs.get('push')

    def __str__(self):
        return '<Push> %s %s' % (self.push, self.author)


class Post():

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.author = kwargs.get('author')
        self.title = kwargs.get('title')
        self.full_datetime = kwargs.get('full_datetime')
        self.content = kwargs.get('content')
        self.ip = kwargs.get('ip')
        self.comments = kwargs.get('comments')

    def __str__(self):
        return '<Post> %s' % (self.title)


class PostMeta():

    fields = ['push', 'mark', 'title', 'date', 'author', 'link', 'filename']

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.fields:
                setattr(self, k, v)

    def __str__(self):
        return '<PostMeta> %s' % (self.title)
