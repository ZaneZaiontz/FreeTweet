""" 
    This code converts twitter links to add fx and remove extra unneeded info 
    
    Example conversion would be talking a link like
    'https://twitter.com/NASA/status/1606323406965817344?cxt=HHwWgIC-qZio58osAAAA'
    and converting it to
    'https://fxtwitter.com/NASA/status/1606323406965817344' - good all around
    'https://vxtwitter.com/NASA/status/1606323406965817344' - works better with gifs
    'https://twxtter.com/NASA/status/1606323406965817344' - also decent choice
    'https://twitter.com/NASA/status/1606323406965817344' - works better for multiple images
"""

IS_SPOILER: bool = True
# SPOILER_GAP: int = 5
TWIT_PROXY: str = "fx"

def read_file() -> list:
    """
        Reads in links from file
    """
    f = open("links.txt", "r")
    fixed_links = [fix_links(x).strip('\n') for x in f]
    return fixed_links

def fix_links(user_input) -> str:
    """
    This function takes links and strips out the garbage 

    :param link_gap: Position in the string to add TWIT_PROXY to, 
    should be placed right after 'https://'

    """
    link_gap: int = 8
    x = user_input.rfind('?')

    if x != -1:
        return user_input[0:link_gap] + TWIT_PROXY + user_input[link_gap:x]
    else:
        return user_input[0:link_gap] + TWIT_PROXY + user_input[link_gap:]

def add_spoiler(links: list[str]) -> list:
    """
        Adds a discord spoiler tag to the given links
    """
    for index, value in enumerate(links):
        links[index] = f"|| {value} ||"
    return links

def main():
    """
        Main entry to link _conversion.py
    """
    links = read_file()
    if IS_SPOILER:
        links = add_spoiler(links)

if __name__ == "__main__":
    main()
