import requests
import difflib
from rich.console import Console
from rich.table import Table

console = Console()

GENRES = [
    "architecture",
    "art_instruction",
    "art_history",
    "dance",
    "design",
    "fashion",
    "film",
    "graphic_design",
    "music",
    "music_theory",
    "painting",
    "photography",
    "animals",
    "bears",
    "cats",
    "kittens",
    "dogs",
    "puppies",
    "fiction",
    "fantasy",
    "historical_fiction",
    "horror",
    "humor",
    "literature",
    "magic",
    "mystery_and_detective_stories",
    "plays",
    "poetry",
    "romance",
    "science_fiction",
    "short_stories",
    "thriller",
    "young_adult",
    "science_and_mathematics",
    "biology",
    "chemistry",
    "mathematics",
    "physics",
    "programming",
    "business_and_finance",
    "management",
    "entrepreneurship",
    "business_economics",
    "business_success",
    "finance",
    "childrens",
    "kids_books",
    "stories_in_rhyme",
    "baby_books",
    "bedtime_books",
    "picture_books",
    "history",
    "ancient_civilization",
    "archaeology",
    "anthropology",
    "world_war_ii",
    "social_life_and_customs",
    "health_and_wellness",
    "cooking",
    "cookbooks",
    "mental_health",
    "exercise",
    "nutrition",
    "self_help",
    "biography",
    "autobiographies",
    "politics_and_government",
    "women",
    "kings_and_rulers",
    "composers",
    "artists",
    "social_sciences",
    "religion",
    "political_science",
    "psychology",
    "places",
    "brazil",
    "india",
    "indonesia",
    "united_states",
    "textbooks",
    "geography",
    "algebra",
    "education",
    "business_and_economics",
    "science",
    "english_language",
    "computer_science",
    "sports"
]


def get_user_genre():
    """returns the users genre"""

    while True:
        genre = input("What genre of Book would you like a suggestion for? ")
        genre = genre.replace(" ", "_").lower()

        if genre in GENRES:
            return genre

        suggestions = difflib.get_close_matches(genre, GENRES, n=3)

        if suggestions:
            print("Did you mean: ")
            for s in suggestions:
                print(f"{s}")

        else:
            print("Genre not recognized")

        print("Try again.\n")


def get_books_url(genre: str):
    """return the API which contains the books data"""
    response = requests.get(
        f"https://openlibrary.org/subjects/{genre}.json?limit=20")

    book_data = response.json()

    if response.status_code == 200:
        return book_data.get("works", [])
    else:
        raise ValueError("Request Denied!!")


def get_book_rating(work_key: str):
    """returns a books rating"""
    word_id = work_key.split("/")[-1]
    response = requests.get(
        f"https://openlibrary.org/works/{word_id}/ratings.json")
    rating_data = response.json()

    if response.status_code != 200:
        return "No rating"

    summary = rating_data.get("summary", {})
    average = summary.get("average")
    count = summary.get("count", 0)

    if average is None:
        return "No rating"

    return f"{average:.2f}/5 ⭐ ({count} ratings)"


def book_suggestions(book_data) -> list[str]:
    """returns a list of suggested books"""
    books = []

    for work in book_data[:15]:
        title = work.get("title", "unknown title")
        year = work.get("first_publish_year", "Unknown Year")
        authors = work.get("authors", [])
        author_name = authors[0].get("name", "Unknown Author")

        work_key = work.get("key")
        rating = get_book_rating(work_key)

        books.append(f"{title} - {author_name} - {year} - {rating}")

    return books


def display_books(books, genre):
    """displays the book suggestions"""

    formatted_genre = genre.replace("_", " ").title()

    console.print(
        f"\n[bold cyan]Here are 15 books in the {formatted_genre} genre[/bold cyan]\n"
    )

    table = Table(title="Book Recommendations")

    table.add_column("#", style="dim", width=4)
    table.add_column("Title", style="bold")
    table.add_column("Author")
    table.add_column("Year")
    table.add_column("Rating")

    count = 1

    for book in books:
        title, author, year, rating = book.split(" - ")
        table.add_row(str(count), title, author, year, rating)
        count += 1

    console.print(table)


def main():
    genre = get_user_genre()
    book_data = get_books_url(genre)
    books = book_suggestions(book_data)
    display_books(books, genre)


if __name__ == "__main__":
    main()
