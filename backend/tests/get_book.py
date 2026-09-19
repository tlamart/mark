import sys
import requests

def main():
    id = input("id: ")
    r = requests.get(f"http://127.0.0.1:8000/books/{id}")
    print(r.text)

if __name__ == "__main__":
    main()