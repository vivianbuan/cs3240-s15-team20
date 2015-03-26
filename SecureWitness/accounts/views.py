from django.shortcuts import render


from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Create your views here.

@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, authentication_form=AuthenticationForm):

    if request.method == "POST":
    	# Add User Model instance here
    	form = authentication_form(request, data=request.POST)

    form = authentication_form(request)

    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("registration/register.html", context)