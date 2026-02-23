import sys
from collections import deque

TRACE = False

def trace(msg):
    if TRACE:
        print(f"[TRACE] {msg}")

favorites = []
feed = deque()

def add_post():
    """
    Add a new URL to the rear of the feed queue.
    """
    new_post = input('Enter the URL: ')
    trace(f"User entered URL: {new_post!r}")
    feed.append(new_post)
    trace(f"Feed now has {len(feed)} items")
    print(f"{new_post}, added to feed.")

def skip_post():
    """
    Remove a URL from the front of the queue.
    """ 
    trace("skip_post() called")
    if feed:
        lastRemoved = feed.popleft()
        print(f"{lastRemoved} removed from feed.")
        return
    print("Feed empty, try adding a URL")

def view_data(label, datastruct):
    """
    Display the data structure, if the data structure exists then it loops through printing each value and counting each iteration starting at 1.
    Args:
        label: Name of the data structure to show in messages.
        datastruct: Iterable structure with items to print.
    """
    trace(f"view_data() called with label={label!r}, size={len(datastruct)}")
    print(f"\n=== {label} ===")
    if datastruct:
        count = 1
        for item in datastruct:
            print(f"{count}. {item}")
            count += 1
        return
    print(f"{label} empty, try adding a URL")

def add_favorite():
    """
    Add a URL from the feed queue to the top of the favorites stack. 
    """
    trace("add_favorite() called")
    if feed:
        view_data("Feed", feed)
        pickFavorite = input(f"Select which option to add as favorite (ex: 2): ")
        try:
            slot = int(pickFavorite) # user must pick from numbered list (1-10)
            favorites.append(feed[slot - 1]) # subtract 1 for python index
            print(f"{favorites[-1]} added successfully.")
        except (ValueError, IndexError):
            print("Invalid selection.")
        return
    print("Feed empty, try adding a URL")

def remove_last_favorite():
    """
    Remove a URL from the top of the favorites stack
    """
    trace("remove_last_favorite() called")
    if favorites:
        lastFavorite = favorites.pop()
        print(f"{lastFavorite} removed from favorites.")
        return
    print("Favorites empty, try adding a URL")

def shutdown():
    """
    Exit the program gracefully.
    """
    trace("shutdown() called")
    print("Shutting Down...")
    return False


def print_menu():
    """
    Displays each Key: label, function within the menu tuple.
    """
    trace("print_menu() called")
    print("=== Menu ===")
    for key, label, func in menu:
        print(f"[{key}] {label}")
    print("=== Select an action ===")
        
def toggle_trace():
    """Toggle debug trace messages on or off."""
    global TRACE # use the global value for leftside of '='
    TRACE = not TRACE # if false become true, if true become false
    state = "ON" if TRACE else "OFF" # label for trace status
    print(f"Trace mode is now {state}.")


menu = [ 
# key, label, func
("0", "Shut down", shutdown),
("1", "Add post", add_post),
("2", "Skip post", skip_post),
("3", "Add favorites", add_favorite),
("4", "Remove last favorited", remove_last_favorite),
("5", "View feed", lambda: view_data("Feed", feed)), # hide params from menu using the temp wrapper on view_data()
("6", "View Favorites", lambda: view_data("Favorites", favorites)),
("7", "Show menu", print_menu),
("8", "Toggle trace", toggle_trace)
]

def main():
    running = True
    print_menu()
    dispatch = {key: func for key, _, func in menu} # this will store the key value pair for menu entries
    trace(f"Dispatch table keys: {list(dispatch.keys())}")
    while running: # exits if set False
        choice = input().strip()
        trace(f"User choice: {choice!r}")
        action = dispatch.get(choice) # dispatch safely gets the function value from menu
        if action is None:
            print("Invalid choice.")
            continue
        trace(f"Dispatching to: {action.__name__}")
        result = action()
        if result is False:  # only shutdown returns False
            trace("Shutdown signal received; exiting main loop")
            running = False
    trace("Program exiting main()")
    return
    
if __name__ == "__main__":
    main()