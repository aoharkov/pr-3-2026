import time
from urllib.parse import unquote

from wiki_fetcher import BASE_URL, fetch_page, get_random_wikipedia_page
from wiki_parser import extract_first_link

# Safety cutoff – empirical average chain is ~23 hops; 100 gives a 4× margin.
MAX_STEPS = 100

# Polite delay between requests (seconds).
REQUEST_DELAY = 0.1

# Testing start page (set to None to use a random page).
TEST_URL = None


def follow_chain(start_url: str | None = TEST_URL, max_steps: int = MAX_STEPS) -> None:
    """Start from a given (or random) page and follow first links until a cycle or dead end."""
    page = fetch_page(start_url) if start_url else get_random_wikipedia_page()

    visited_titles: list[str] = []  # ordered list for display
    visited_urls: list[str] = []
    visited_set: set[str] = set()   # for O(1) cycle detection

    reason = "cutoff"

    for step in range(1, max_steps + 1):
        title = page["title"]
        url = page["url"]

        # --- cycle detection ---
        if title in visited_set:
            reason = "cycle"
            print(f"\n↻  Cycle detected at step {step}: '{title}' was already visited.\n")
            break

        visited_titles.append(title)
        visited_urls.append(url)
        visited_set.add(title)

        print(f"  {step:>3}. {title}  —  {url}")

        # --- extract first link ---
        href = extract_first_link(page["html"])
        if href is None:
            reason = "dead_end"
            print(f"\n✖  Dead end at step {step}: no valid first link found.\n")
            break

        next_url = BASE_URL + href
        next_title = unquote(href.split("/wiki/")[-1]).replace("_", " ")

        # --- check if the *next* page was already visited (early cycle) ---
        if next_title in visited_set:
            reason = "cycle"
            print(f"\n↻  Cycle detected: step {step + 1} would be '{next_title}' (already visited).\n")
            break

        # --- check if the *next* page is Philosophy ---
        if next_url == "https://en.wikipedia.org/wiki/Philosophy":
            visited_titles.append(next_title)
            visited_urls.append(next_url)
            reason = "got_to_philosophy"
            print(f"\n🎉  Reached Philosophy at step {step + 1}!\n")
            break

        time.sleep(REQUEST_DELAY)
        page = fetch_page(next_url)
    else:
        print(f"\n⚠  Cutoff reached after {max_steps} steps.\n")

    # --- summary ---
    print("=" * 60)
    print(f"  Pages visited : {len(visited_titles)}")
    print(f"  Termination   : {reason}")
    print("=" * 60)
    print("\nFull chain:")
    for i, (t, u) in enumerate(zip(visited_titles, visited_urls), 1):
        print(f"  {i:>3}. {t}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    follow_chain()
