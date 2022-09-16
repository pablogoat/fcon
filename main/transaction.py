class transaction():
    debtor = ''
    collector = ''
    value = ''

    def __init__(self, debtor, value, collector):
        self.debtor = debtor
        self.collector = collector
        self.value = value


