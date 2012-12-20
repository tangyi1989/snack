power_state = { 1 : _("On") }
catalog = {"power_state" : power_state}

def translate(what, type):
    page = catalog.get(type, None)
    if page == None:
        return what
    
    return page.get(what, what)
    
    
        