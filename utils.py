import logging
import os

def get_html_from_page_name(pageName : str,directory : str = "./html") -> str:
    working_dir = os.path.dirname(__file__)
    pageName = pageName.lstrip("/")
    pageName = pageName.rstrip("/")
    directory = directory.rstrip("/")
    relative_directory = os.path.join(working_dir,str(directory))
    mpath = os.path.join(relative_directory,pageName)
    logging.warning("Looking for mpath: %s",str(mpath))

    if(os.path.exists(mpath)):
        return open(mpath).read()
    logging.warning("Couldn't find .html for %s",pageName)
    return ""
