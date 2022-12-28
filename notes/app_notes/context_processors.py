from .forms import FilterForm


def filter_form_processor(request):
    filter_form = {
        'filter_form': FilterForm()
    }
    return filter_form