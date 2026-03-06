from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

# CSS classes to skip when looking for the first <p> in body content.
SKIP_CLASSES = {
    "infobox", "sidebar", "navbox", "metadata", "mw-editsection",
    "toc", "thumb", "noprint", "hatnote", "shortdescription",
    "mw-empty-elt",
}


def _has_skip_class(tag: Tag) -> bool:
    """Return True if *tag* (or any ancestor) carries a class we should skip."""
    for cls in tag.get("class", []):
        if cls in SKIP_CLASSES:
            return True
    return False


def _is_valid_wiki_link(tag: Tag) -> bool:
    """Return True if *tag* is an internal article link worth following."""
    href = tag.get("href", "")
    if not href.startswith("/wiki/"):
        return False
    # Namespace links contain a colon after /wiki/  (e.g. File:, Help:, …)
    after_wiki = href[len("/wiki/"):]
    if ":" in after_wiki:
        return False
    # Skip self-links and red (non-existent) links
    classes = set(tag.get("class", []))
    if classes & {"mw-selflink", "new"}:
        return False
    return True


def extract_first_link(html: str) -> str | None:
    """Return the /wiki/… path of the first valid link in the article body.

    Rules (following the classic "Getting to Philosophy" experiment):
    * Only consider <p> tags inside the main parser output.
    * Skip links inside parentheses in the rendered text.
    * Skip links inside <i> / <em> (typically foreign-language terms).
    * Skip non-article links (namespaced, red, self).
    """
    soup = BeautifulSoup(html, "lxml")

    # The page may contain several mw-parser-output divs (e.g. coordinates).
    # The main article body is always a direct child of #mw-content-text.
    wrapper = soup.find("div", id="mw-content-text")
    if wrapper is not None:
        content = wrapper.find("div", class_="mw-parser-output", recursive=False)
    else:
        content = soup.find("div", class_="mw-parser-output")

    if content is None:
        return None

    # Iterate over top-level children that are <p> tags.
    for element in content.children:
        if not isinstance(element, Tag):
            continue
        if element.name != "p":
            continue
        if _has_skip_class(element):
            continue

        # Walk the <p> tree keeping track of parenthesis depth.
        link = _first_link_in_element(element)
        if link is not None:
            return link

    return None


def _first_link_in_element(element: Tag) -> str | None:
    """Walk *element* depth-first, tracking paren depth, return first valid link."""
    paren_depth = 0

    for node in element.descendants:
        if isinstance(node, NavigableString):
            # Update parenthesis depth from plain text.
            for ch in str(node):
                if ch == "(":
                    paren_depth += 1
                elif ch == ")":
                    paren_depth = max(0, paren_depth - 1)
            continue

        if not isinstance(node, Tag):
            continue

        if node.name == "a" and paren_depth == 0:
            # Skip links inside <i> or <em>.
            if any(p.name in ("i", "em") for p in node.parents if isinstance(p, Tag)):
                continue
            if _is_valid_wiki_link(node):
                return node["href"]

    return None
