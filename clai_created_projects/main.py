import sys
from shortener import shorten_url, resolve_url

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url> or python main.py --resolve <key>")
        return

    if sys.argv[1] == "--resolve":
        if len(sys.argv) < 3:
            print("Error: Key required for resolution")
            return
        key = sys.argv[2]
        url = resolve_url(key)
        if url:
            print(f"Original URL: {url}")
        else:
            print("Error: Key not found")
    else:
        url = sys.argv[1]
        try:
            key = shorten_url(url)
            print(f"Shortened URL key: {key}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
