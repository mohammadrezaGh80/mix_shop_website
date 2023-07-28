class SearchHistory:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        search_history = self.session.get("search_history")
        if not search_history:
            search_history = self.session["search_history"] = {}
        self.search_history = search_history

    def add(self, title):
        if self.search_history:
            self.search_history = {"0": title} | {str(index): value for index, value in
                                                  list(enumerate([value for value in self.search_history.values() if
                                                                  value != title], 1))}
            self.session["search_history"] = self.search_history
        else:
            self.search_history["0"] = title
        self.save()

    def clear(self):
        del self.session["search_history"]

    def save(self):
        self.session.modified = True

    def __len__(self):
        return len(self.search_history.keys())

    def __iter__(self):
        for title in self.search_history.values():
            yield title
