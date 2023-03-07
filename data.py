import requests
from bs4 import BeautifulSoup, element

PUPS = ['Chase', 'Marshall', 'Skye', 'Rubble', 'Everest', 'Rocky', 'Zuma']
HTML_ELEMENTS = ['h2', 'h3', 'ul', 'p', 'div']
PAGE_SECTIONS = ['Summary', 'Characters', 'Synopsis', 'Pups in Action', 'First Responders', 'Backup Responders', 'Other Tasks', 'DVD Inclusions']

def get_episode_from_url(url: str) -> str:
    return url.split('/')[-1]

def get_page_elements(url: str) -> element.ResultSet:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    td = soup.find('td')
    return td.findAll(HTML_ELEMENTS)

def get_elements(
    elements: element.ResultSet,
    header: str, 
    element_type: str) -> list[str]:
    
    header_loc = PAGE_SECTIONS.index(header)
    next_header = PAGE_SECTIONS[header_loc + 1]
    first_next_elements = None
    second_prev_elements = None
    
    for element in elements:
        if element.text == header:
            first_next_elements = element.find_all_next(element_type)
        if element.text == next_header:
            second_prev_elements = element.find_all_previous(element_type)
    if first_next_elements is None:
        raise ValueError(f'Section value of {header} not found in the provided elements')
        
    if second_prev_elements is None:
        for i in range(header_loc+1, len(PAGE_SECTIONS)):
            next_header = PAGE_SECTIONS[i]
            for element in elements:
                if element.text == next_header:
                    second_prev_elements = element.find_all_previous(element_type)
                    break
    if second_prev_elements is None:
        raise ValueError('Could not locate next section for `header`') 
                
    between_elements = []
    for element in first_next_elements:
        if element in second_prev_elements:
            between_elements.append(element.text.strip())
    return between_elements

def split_list_items(items: list[str], sep: str) -> list:
    split_list = []
    for item in items:
        if len(item.split('+')) == 1:
            split_list.append(item)
        else:
            for split_item in item.split('+'):
                split_list.append(split_item)
    return split_list

def get_episode_name(elements):
    return elements[1].text

def get_season_number(elements: element.ResultSet) -> int:
    try:
        season_str = get_elements(elements,'Season', 'div')[0]
    except:
        return None
    return int(season_str)

def get_episode_number(elements: element.ResultSet) -> int:
    try:
        ep_str = get_elements(elements,'Number', 'div')[0]
    except:
        return None
    return ep_str

def get_overall_episode_number(elements: element.ResultSet) -> int:
    try:
        overall_ep_str = get_elements(elements,'Overall Episode #', 'div')[0]
    except:
        return None
    return int(overall_ep_str)

def get_summary(elements: element.ResultSet) -> str:
    try:
        summary = get_elements(elements, 'Summary', 'p')
    except:
        return None
    return ''.join(summary)

def get_characters(elements: element.ResultSet) -> list:
    try:
        characters = get_elements(elements, 'Characters', 'li')
    except:
        return None
    return characters

def get_synopsis(elements: element.ResultSet) -> str:
    try:
        synopsis = get_elements(elements, 'Synopsis', 'p')
    except:
        return None
    return ''.join(synopsis)

def get_first_responders(elements: element.ResultSet) -> list:
    try:
        first_responders = get_elements(elements, 'First Responders', 'p')
    except:
        return None
    return split_list_items(first_responders, '+')
def get_backup_responders(elements: element.ResultSet) -> list:
    try:
        backups = get_elements(elements, 'Backup Responders', 'p')
    except:
        return None
    return split_list_items(backups, '+')

def get_other_tasks(elements: element.ResultSet) -> list:
    try:
        others = get_elements(elements, 'Other Tasks', 'p')
    except Exception:
        return None
    return split_list_items(others, '+')

def get_episode_data(url: str) -> dict:
    elements = get_page_elements(url)
    return {
        'episode_id' : get_episode_from_url(url),
        'episode_name' : get_episode_name(elements),
        'episode_number' : get_episode_number(elements),
        'overall_episode_number': get_overall_episode_number(elements),
        'summary' : get_summary(elements),
        'characters' : get_characters(elements),
        'synopsis' : get_synopsis(elements),
        'first_responders' : get_first_responders(elements),
        'backup_responders' : get_backup_responders(elements),
        'other_tasks' : get_other_tasks(elements)
    }
