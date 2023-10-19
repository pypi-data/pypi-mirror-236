import subprocess


class PackagingError(Exception):
    pass


def test():
    try:
        subprocess.run(["pip", "balkfds"], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise PackagingError("Unable to package") from e


if __name__ == "__main__":
    test()
