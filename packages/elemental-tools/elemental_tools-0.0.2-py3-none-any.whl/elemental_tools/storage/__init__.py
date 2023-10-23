class cache:
    mem = {}

    def store(self, owner, request):
        self.mem[owner] = request

    def read(self, owner):
        return self.mem[owner]

