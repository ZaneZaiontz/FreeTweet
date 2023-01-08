""" 
    This code converts twitter links to add fx and remove extra unneeded info 
    
    Example conversion would be talking a link like
    'https://twitter.com/NASA/status/1606323406965817344?cxt=HHwWgIC-qZio58osAAAA'
    and converting it to
    'https://fxtwitter.com/NASA/status/1606323406965817344'
"""
import os
import sys

IS_SPOILER: bool = True
SPOILER_GAP: int = 5
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
    
    :param link_gap: Position in the string to add TWIT_PROXY to, should be placed right after 'https://'
    
    """
    link_gap: int = 8
    x = user_input.rfind('?')
    
    if x != -1:
        return user_input[0:link_gap] + TWIT_PROXY + user_input[link_gap:x]
    else:
        return user_input[0:link_gap] + TWIT_PROXY + user_input[link_gap:]
    
def add_spoiler(links) -> list:
    """
        Adds a discord spoiler tag to the given links
    """
    new_links = []
    for index, value in enumerate(links):
        if index % SPOILER_GAP == 0:
            new_links.append("|| " + value + " ||")
        else:
            new_links.append(value)
    return new_links


def print_links(links) -> None:
    print()
    for index, value in enumerate(links):
        if (index + 1) % 5 == 0:
            print(f"{value}\n")
        else:
            print(value)
    print()

        
def main():
    """
        Main entry to link _conversion.py
    """
    links = read_file()
    if IS_SPOILER:
        links = add_spoiler(links)
    print_links(links)


if __name__ == "__main__":
    main()
