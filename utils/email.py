from django.template.loader import render_to_string


def render_messages(rpath, filename, context={}):
    """
    A wrapper around django's render_to_string to 
    render txt and html messages for emails.

    rpath: the relative path to the dir containing the template
    filename: the name of the template (excluding file extension)
    context: an optional context dictionary to provide to the template

    Example usage: 

    message, html_message = render_messages('accounts/user', 'account_recover', context={'user': user})
    """

    return (
        # txt message
        render_to_string(f"{rpath}/{filename}.txt", context),
        # html message
        render_to_string(f"{rpath}/{fielname}.html", context),
    )
