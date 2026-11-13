"""Guitar Shape Explorer: a Drafter website about electric guitar designs."""

from dataclasses import dataclass

from bakery import assert_equal
from drafter import *

set_website_title("Guitar Shape Explorer")

set_site_information(
    author="Your Name",
    description=(
        "An interactive website where visitors can explore "
        "different electric guitar body shapes, compare "
        "guitars, and save their favorites."
    ),
    sources=(
        "Drafter documentation and the guitar research "
        "sources used for this project."
    ),
    planning=["planning.md"],
    links=[
        "https://github.com/YOUR-USERNAME/YOUR-REPOSITORY"
    ]
)

hide_debug_information()
set_website_framed(False)

set_website_title("Guitar Shape Explorer")
set_site_information(
    author="Your Name",
    description=(
        "Explore electric guitar body shapes, learn about their designs, "
        "save favorites, compare models, and suggest guitars."
    ),
    sources="Add the sources you use to research guitar models and descriptions.",
    planning="",
    links=[]
)


@dataclass
class Guitar:
    """Store the information displayed for one guitar model."""
    name: str
    maker: str
    body_style: str
    description: str
    genres: list[str]


@dataclass
class State:
    """Store the guitar catalog and the visitor's selections."""
    guitars: list[Guitar]
    favorites: list[str]
    compare_names: list[str]
    search_term: str
    message: str


def make_initial_state() -> State:
    """Create the starting catalog and empty visitor selections."""
    guitars = [
        Guitar(
            "Explorer",
            "Gibson",
            "Angular, offset body",
            "The Explorer has a bold, angular outline and a distinctive "
            "body that stands out from more traditional guitar designs.",
            ["Rock", "Hard Rock", "Metal"]
        ),
        Guitar(
            "Flying V",
            "Gibson",
            "V-shaped body",
            "The Flying V is recognized by its two long wings that form a "
            "V shape. Its design is especially recognizable on stage.",
            ["Rock", "Hard Rock", "Metal"]
        ),
        Guitar(
            "Les Paul",
            "Gibson",
            "Single-cutaway, rounded body",
            "The Les Paul has a thick, rounded body with one cutaway near "
            "the neck. It is known for its classic look and full sound.",
            ["Rock", "Blues", "Jazz"]
        ),
        Guitar(
            "Stratocaster",
            "Fender",
            "Double-cutaway contoured body",
            "The Stratocaster has two cutaways and smooth body contours. "
            "The shape makes the upper frets easy to reach.",
            ["Rock", "Blues", "Pop", "Country"]
        ),
        Guitar(
            "Telecaster",
            "Fender",
            "Single-cutaway slab body",
            "The Telecaster has a simple, familiar outline with a flat "
            "body and one cutaway.",
            ["Country", "Rock", "Blues", "Pop"]
        ),
        Guitar(
            "SG",
            "Gibson",
            "Double-cutaway, thin body",
            "The SG has a thin body, two pointed horns, and deep cutaways "
            "that provide access to the higher frets.",
            ["Rock", "Hard Rock", "Metal", "Blues"]
        ),
        Guitar(
            "Jazzmaster",
            "Fender",
            "Offset-waist body",
            "The Jazzmaster has an offset waist that gives its body an "
            "asymmetrical outline.",
            ["Jazz", "Surf Rock", "Alternative"]
        ),
        Guitar(
            "Firebird",
            "Gibson",
            "Reverse, angular body",
            "The Firebird uses a long, swept-back outline that looks "
            "different from many traditional guitar shapes.",
            ["Rock", "Blues"]
        )
    ]
    return State(guitars, [], [], "", "")


def get_guitar_names(guitars: list[Guitar]) -> list[str]:
    """Return the names of every guitar in the catalog."""
    names = []
    for guitar in guitars:
        names.append(guitar.name)
    return names


def guitar_exists(guitars: list[Guitar], guitar_name: str) -> bool:
    """Return True when a guitar with the given name is in the catalog."""
    for guitar in guitars:
        if guitar.name.lower() == guitar_name.lower():
            return True
    return False


def navigation(state: State) -> list:
    """Create the common title and navigation links for every page."""
    content = [
        Header("Guitar Shape Explorer"),
        Link("Home", "index"),
        " | ",
        Link("Catalog", "catalog"),
        " | ",
        Link("Search", "search"),
        " | ",
        Link("Favorites", "favorites"),
        " | ",
        Link("Compare", "compare"),
        " | ",
        Link("Suggest a Guitar", "submit_guitar"),
        "\n",
        HorizontalRule()
    ]
    if state.message != "":
        content.append(state.message + "\n")
    return content


def add_guitar_description(content: list, guitar: Guitar) -> None:
    """Add one guitar's information to a page content list."""
    content.append("\n" + guitar.name + "\n")
    content.append("Maker: " + guitar.maker + "\n")
    content.append("Body shape: " + guitar.body_style + "\n")
    content.append(guitar.description + "\n")
    content.append("Genres: " + ", ".join(guitar.genres) + "\n")


@route
def index(state: State) -> Page:
    """Show the website introduction and its main destinations."""
    return Page(state, navigation(state) + [
        Header("Discover Guitar Shapes"),
        "Welcome to Guitar Shape Explorer!\n",
        "Electric guitars come in many different body shapes. Some are "
        "rounded and traditional, while others have sharp angles or "
        "unusual outlines.\n",
        "Use this website to explore guitar designs, search the catalog, "
        "save your favorites, and compare two models. You can also suggest "
        "a guitar to add to the catalog.\n",
        Button("Explore the catalog", "catalog"),
        Button("Compare guitars", "compare"),
        Button("Suggest a guitar", "submit_guitar")
    ])


@route
def catalog(state: State) -> Page:
    """List the guitar models and let visitors open a detail page."""
    content = navigation(state) + [
        Header("Guitar Catalog"),
        "Browse the guitar shapes in the catalog. Select a model to learn "
        "more about its body design.\n"
    ]
    for guitar in state.guitars:
        content.append(guitar.name + " â€” " + guitar.body_style + "\n")

    guitar_names = get_guitar_names(state.guitars)
    if len(guitar_names) > 0:
        content.extend([
            "\nChoose a guitar:",
            SelectBox("guitar_name", guitar_names, guitar_names[0]),
            Button("View guitar details", "guitar_detail")
        ])
    else:
        content.append("There are no guitars in the catalog yet.\n")
    return Page(state, content)


@route
def guitar_detail(state: State, guitar_name: str) -> Page:
    """Show details for one guitar and let visitors save it as a favorite."""
    content = navigation(state) + [Header("Guitar Details")]
    selected_guitar = None

    for guitar in state.guitars:
        if guitar.name == guitar_name:
            selected_guitar = guitar

    if selected_guitar is None:
        content.append("That guitar could not be found. Return to the catalog.\n")
    else:
        add_guitar_description(content, selected_guitar)

    guitar_names = get_guitar_names(state.guitars)
    if len(guitar_names) > 0:
        favorite_value = guitar_name in state.favorites
        content.extend([
            "\nChoose which guitar to save:",
            SelectBox("guitar_name", guitar_names, guitar_name),
            "\nMark this guitar as a favorite: ",
            CheckBox("favorite", favorite_value),
            "\n",
            Button("Save favorite setting", "save_favorite"),
            Link("Back to catalog", "catalog")
        ])
    return Page(state, content)


@route
def save_favorite(state: State, guitar_name: str, favorite: bool) -> Page:
    """Add or remove a guitar from the visitor's favorites."""
    if not guitar_exists(state.guitars, guitar_name):
        state.message = "Choose a guitar that is in the catalog."
    elif favorite and guitar_name not in state.favorites:
        state.favorites.append(guitar_name)
        state.message = guitar_name + " was added to your favorites."
    elif not favorite and guitar_name in state.favorites:
        state.favorites.remove(guitar_name)
        state.message = guitar_name + " was removed from your favorites."
    else:
        state.message = "Your favorites are up to date."
    return guitar_detail(state, guitar_name)


@route
def search(state: State, query: str = "") -> Page:
    """Search guitar names, body shapes, descriptions, and genres."""
    state.search_term = query.strip()
    query_lower = state.search_term.lower()
    content = navigation(state) + [
        Header("Search the Catalog"),
        "Search by guitar name, body shape, description, or genre.\n",
        TextBox("query", state.search_term),
        Button("Search", "search"),
        "\n"
    ]

    if query_lower == "":
        content.append("Enter a search term to see matching guitars.\n")
    else:
        matches = []
        for guitar in state.guitars:
            found_match = (
                query_lower in guitar.name.lower()
                or query_lower in guitar.body_style.lower()
                or query_lower in guitar.description.lower()
            )
            for genre in guitar.genres:
                if query_lower in genre.lower():
                    found_match = True
            if found_match:
                matches.append(guitar)

        if len(matches) == 0:
            content.append("No guitars matched that search. Try another term.\n")
        else:
            content.append("Matching guitars:\n")
            for guitar in matches:
                content.append(
                    guitar.name + " â€” " + guitar.body_style + "\n"
                )
    return Page(state, content)


@route
def favorites(state: State) -> Page:
    """Display saved guitars and provide a way to remove a favorite."""
    content = navigation(state) + [Header("My Favorite Guitars")]
    if len(state.favorites) == 0:
        content.append(
            "You have not saved any favorites yet. Visit the catalog and "
            "open a guitar's detail page to save one.\n"
        )
    else:
        content.append("Your saved guitar shapes:\n")
        for guitar in state.guitars:
            if guitar.name in state.favorites:
                content.append(
                    guitar.name + " â€” " + guitar.body_style + "\n"
                )
        content.extend([
            "\nChoose a favorite to remove:",
            SelectBox("favorite_name", state.favorites, state.favorites[0]),
            Button("Remove favorite", "remove_favorite")
        ])
    return Page(state, content)


@route
def remove_favorite(state: State, favorite_name: str) -> Page:
    """Remove the selected guitar from the favorites list."""
    if favorite_name in state.favorites:
        state.favorites.remove(favorite_name)
        state.message = favorite_name + " was removed from your favorites."
    else:
        state.message = "That guitar was not in your favorites."
    return favorites(state)


@route
def compare(
    state: State,
    first_guitar: str = "",
    second_guitar: str = ""
) -> Page:
    """Let visitors select two guitars and compare their designs."""
    guitar_names = get_guitar_names(state.guitars)

    if first_guitar != "" and second_guitar != "":
        if first_guitar == second_guitar:
            state.message = "Choose two different guitars to compare."
        elif (
            guitar_exists(state.guitars, first_guitar)
            and guitar_exists(state.guitars, second_guitar)
        ):
            state.compare_names = [first_guitar, second_guitar]
            state.message = "Your guitar comparison has been updated."

    content = navigation(state) + [
        Header("Compare Guitar Shapes"),
        "Choose two different guitars to compare their body shapes, "
        "descriptions, and associated genres.\n"
    ]

    if len(guitar_names) < 2:
        content.append("You need at least two guitars to compare.\n")
    else:
        first_choice = guitar_names[0]
        second_choice = guitar_names[1]
        if len(state.compare_names) == 2:
            if state.compare_names[0] in guitar_names:
                first_choice = state.compare_names[0]
            if state.compare_names[1] in guitar_names:
                second_choice = state.compare_names[1]

        content.extend([
            "First guitar:",
            SelectBox("first_guitar", guitar_names, first_choice),
            "\nSecond guitar:",
            SelectBox("second_guitar", guitar_names, second_choice),
            Button("Compare selected guitars", "compare"),
            "\n"
        ])

        if len(state.compare_names) == 2:
            content.append("Comparison results:\n")
            for guitar in state.guitars:
                if guitar.name in state.compare_names:
                    add_guitar_description(content, guitar)
    return Page(state, content)


@route
def submit_guitar(
    state: State,
    submitted_name: str = "",
    submitted_shape: str = "Other",
    submitted_description: str = "",
    submitted_genre: str = "Rock",
    add_to_favorites: bool = False
) -> Page:
    """Accept a visitor's guitar suggestion and optionally save it."""
    clean_name = submitted_name.strip()
    clean_description = submitted_description.strip()

    # Only validate when the visitor has started filling in the form.
    if clean_name != "" or clean_description != "":
        if clean_name == "" or clean_description == "":
            state.message = "Please enter both a guitar name and a description."
        elif guitar_exists(state.guitars, clean_name):
            state.message = "That guitar is already in the catalog."
        else:
            new_guitar = Guitar(
                clean_name,
                "Community suggestion",
                submitted_shape,
                clean_description,
                [submitted_genre]
            )
            state.guitars.append(new_guitar)
            if add_to_favorites:
                state.favorites.append(clean_name)
            state.message = clean_name + " was added to the catalog."

    shape_options = [
        "Explorer", "Flying V", "Les Paul", "Stratocaster", "Telecaster",
        "SG", "Jazzmaster", "Firebird", "Other"
    ]
    genre_options = [
        "Rock", "Metal", "Blues", "Jazz", "Pop", "Country", "Other"
    ]
    content = navigation(state) + [
        Header("Suggest a Guitar"),
        "Know a guitar shape that is missing? Submit it below.\n",
        "Guitar model name:",
        TextBox("submitted_name", ""),
        "\nBody shape or model category:",
        SelectBox("submitted_shape", shape_options, "Other"),
        "\nAssociated genre:",
        SelectBox("submitted_genre", genre_options, "Rock"),
        "\nDescribe the guitar:",
        TextArea("submitted_description", "", rows=4),
        "\nAdd this guitar to my favorites: ",
        CheckBox("add_to_favorites", False),
        "\n",
        Button("Submit guitar", "submit_guitar")
    ]
    return Page(state, content)


# Unit tests for helper functions and routes.
# Each route is called directly so its state changes can be checked.
assert_equal(get_guitar_names(make_initial_state().guitars)[0], "Explorer")
assert_equal(guitar_exists(make_initial_state().guitars, "Les Paul"), True)
assert_equal(guitar_exists(make_initial_state().guitars, "Unknown"), False)

assert_equal(len(index(make_initial_state()).content) > 0, True)
assert_equal(len(catalog(make_initial_state()).content) > 0, True)
assert_equal(len(guitar_detail(make_initial_state(), "Explorer").content) > 0, True)
assert_equal(search(make_initial_state(), "LES").state.search_term, "LES")
assert_equal(favorites(make_initial_state()).state.favorites, [])
assert_equal(
    compare(make_initial_state(), "Explorer", "Flying V").state.compare_names,
    ["Explorer", "Flying V"]
)
assert_equal(
    submit_guitar(
        make_initial_state(),
        "Test Guitar",
        "Other",
        "A guitar added by a unit test.",
        "Rock",
        True
    ).state.guitars[-1].name,
    "Test Guitar"
)
assert_equal(
    save_favorite(make_initial_state(), "Explorer", True).state.favorites,
    ["Explorer"]
)
assert_equal(
    remove_favorite(
        State(make_initial_state().guitars, ["Explorer"], [], "", ""),
        "Explorer"
    ).state.favorites,
    []
)


start_server(make_initial_state())
