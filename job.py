class Job:
    def __init__(self, email, password, platform, photo_identifier, photo_path):
        self.email = email
        self.password = password
        self.platform = platform
        self.photo_identifier = photo_identifier
        self.photo_path = photo_path
        self.tags = []
