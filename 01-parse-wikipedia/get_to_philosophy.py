import time
from urllib.parse import unquote

from chain_utils import ChainResult, VisitTracker, print_chain_result, print_step
from wiki_fetcher import BASE_URL, fetch_page, get_random_wikipedia_page
from wiki_parser import extract_first_link

# Safety cutoff – empirical average chain is ~23 hops; 100 gives a 4× margin.
MAX_STEPS = 100

# Polite delay between requests (seconds).
REQUEST_DELAY = 0.1

# Testing start page (set to None to use a random page).
TEST_URL = None


def follow_chain(start_url: str | None = TEST_URL, max_steps: int = MAX_STEPS) -> ChainResult:
    """Follow first-links from *start_url* until Philosophy, a cycle, or a dead end."""
    page = fetch_page(start_url) if start_url else get_random_wikipedia_page()
    tracker = VisitTracker()

    for step in range(1, max_steps + 1):
        title = page["title"]
        url = page["url"]

        if tracker.has_visited(title):
            print(f"\n↻  Cycle detected at step {step}: '{title}' was already visited.\n")
            return tracker.to_result("cycle")

        tracker.add(title, url)
        print_step(step, title, url)

        href = extract_first_link(page["html"])
        if href is None:
            print(f"\n✖  Dead end at step {step}: no valid first link found.\n")
            return tracker.to_result("dead_end")

        next_url = BASE_URL + href
        next_title = unquote(href.split("/wiki/")[-1]).replace("_", " ")

        if tracker.has_visited(next_title):
            print(f"\n↻  Cycle detected: step {step + 1} would be '{next_title}' (already visited).\n")
            return tracker.to_result("cycle")

        if next_url == "https://en.wikipedia.org/wiki/Philosophy":
            tracker.add(next_title, next_url)
            print(f"\n🎉  Reached Philosophy at step {step + 1}!\n")
            return tracker.to_result("got_to_philosophy")

        time.sleep(REQUEST_DELAY)
        page = fetch_page(next_url)

    print(f"\n⚠  Cutoff reached after {max_steps} steps.\n")
    return tracker.to_result("cutoff")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    result = follow_chain()
    print_chain_result(result)
