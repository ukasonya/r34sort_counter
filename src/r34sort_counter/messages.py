from r34enumerate.constants import ENV_API_KEY, ENV_USER_ID


def pmain(message: str, both: bool = False) -> None:
    print(f"[!] {message} Run the following command{"s" if both else ""}")


def ptoken() -> None:
    print(f"  export {ENV_API_KEY}=<your-token>")


def puserid() -> None:
    print(f"  export {ENV_USER_ID}=<your-user-id>")
