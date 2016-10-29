# Template context processors
from CavTutor.views import _get_loggedin_user

# Adds user authentication context
def auth(request):
    
    context = {
            'user' : _get_loggedin_user(request)
            }

    return context
