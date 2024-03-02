class moderationResponse:
    def __init__(self, code: int, message: str, isViolated: bool, isBanned: bool, reproducedContent: str, reason) -> None:
        self.code = code
        self.message = message
        self.isViolated = isViolated
        self.isBanned = isBanned
        self.reproducedContent = reproducedContent
        self.reason = reason