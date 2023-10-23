class ResourceError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg

    
a = 1
raise ResourceError(f"error{a}")