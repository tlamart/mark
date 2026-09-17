import sys
import requests

def main():
    id = input("id: ")
    current_page = input("current_page: ")
    current_page = None if current_page == "" else int(current_page)
    reading_time = input("reading_time: ")
    reading_time = None if reading_time == "" else int(reading_time)
    data = {
        "current_page": current_page,
        "reading_time": reading_time
    }
    r = requests.patch(f"http://localhost:8000/books/{id}", json=data)
    print(r.text)

if __name__ == "__main__":
    main()