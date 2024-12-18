from dotenv import load_dotenv
from . import overlay


def main():
    load_dotenv()  # take environment variables
    overlay.main()
