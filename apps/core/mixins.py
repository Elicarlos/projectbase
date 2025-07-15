class OwnedByUserMixin:
    def is_owner(self, user):
        return self.user == user
