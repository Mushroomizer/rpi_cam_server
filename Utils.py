import logging
import os

def get_html_from_page_name(pageName : str,directory : str = "./html") -> str:
    pageName = pageName.lstrip("/")
    pageName = pageName.rstrip("/")
    directory = directory.rstrip("/")

    logging.info("Looking for mpath: %s/%s",str(directory),str(pageName))
    mpath = os.path.join(directory,pageName)
    if(os.path.exists(mpath)):
        return open(mpath).read()
    logging.warning("Couldn't find .html for %s",pageName)
    return ""