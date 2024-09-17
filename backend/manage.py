import sys
from uvicorn import run
from fastapi_app.app import init_db


def start():
    run("fastapi_app.app.main:app", host="127.0.0.3", port=8006, reload=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: manage.py [OPTIONS]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        start()

    elif command == "migrate":
        return init_db.migrate()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()