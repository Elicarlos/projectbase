import threading

_current_organization = threading.local()


def get_current_organization():
    return getattr(_current_organization, "organization", None)


def set_current_organization(organization):
    _current_organization.organization = organization


def clear_current_organization():
    if hasattr(_current_organization, "organization"):
        del _current_organization.organization
