from django.utils.translation import gettext_lazy as _

TITLES = {
    'new_application':   _('New application'),
    'app_accepted':      _('Application accepted'),
    'mission_completed': _('Mission completed'),
    'new_delivery':      _('New delivery'),
    'delivery_accepted': _('Delivery accepted'),
    'revision_requested':_('Revision requested'),
    'new_message':       _('New message'),
    'mission_approved':  _('Mission approved — funds released'),
}

# Each value is a lazy string with named placeholders.
# All placeholders are filled with raw data (names, titles) — not translated.
MESSAGES = {
    'new_application':   _('%(name)s applied to your mission "%(mission)s"'),
    'app_accepted':      _('Your application for "%(mission)s" has been accepted!'),
    'mission_completed': _('The mission "%(mission)s" has been marked as completed.'),
    'new_delivery':      _('%(name)s submitted a delivery for "%(mission)s"'),
    'delivery_accepted': _('Your delivery for "%(mission)s" has been accepted!'),
    'revision_requested':_('The client requested a revision for "%(mission)s".'),
    'new_message':       _('%(name)s sent you a message.'),
    'mission_approved':  _('Admin approved the mission "%(mission)s". Funds have been credited to you.'),
}


def resolve(key_map, key, params):
    """Return the translated string for *key*, filling in *params*.
    Falls back to the raw key string if the key is unknown."""
    template = key_map.get(key)
    if template is None:
        return key
    try:
        return str(template) % params if params else str(template)
    except (KeyError, TypeError):
        return str(template)
