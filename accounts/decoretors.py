from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_only(func_view) :
    def wrapper(request, *args, **kwagrs) :
        if request.user.is_authenticated :
            return redirect(reverse('blog:index'))

        else :
            return func_view(request, *args, **kwagrs)

    return wrapper