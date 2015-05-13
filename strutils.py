import re

import six

# NOTE(flaper87): The following globals are used by `mask_password`
_SANITIZE_KEYS = ['adminPass', 'admin_pass', 'password', 'admin_password',
                  'auth_token', 'new_pass', 'auth_password', 'secret_uuid']

# NOTE(ldbragst): Let's build a list of regex objects using the list of
# _SANITIZE_KEYS we already have. This way, we only have to add the new key
# to the list of _SANITIZE_KEYS and we can generate regular expressions
# for XML and JSON automatically.
_SANITIZE_PATTERNS_2 = {}
_SANITIZE_PATTERNS_1 = {}

# NOTE(amrith): Some regular expressions have only one parameter, some
# have two parameters. Use different lists of patterns here.
_FORMAT_PATTERNS_1 = [r'(%(key)s\s*[=]\s*)[^\s^\'^\"]+']
_FORMAT_PATTERNS_2 = [r'(%(key)s\s*[=]\s*[\"\'])[^\"\']*([\"\'])',
                      r'(%(key)s\s+[\"\'])[^\"\']*([\"\'])',
                      r'([-]{2}%(key)s\s+)[^\'^\"^=^\s]+([\s]*)',
                      r'(<%(key)s>)[^<]*(</%(key)s>)',
                      r'([\"\']%(key)s[\"\']\s*:\s*[\"\'])[^\"\']*([\"\'])',
                      r'([\'"][^"\']*%(key)s[\'"]\s*:\s*u?[\'"])[^\"\']*'
                      '([\'"])',
                      r'([\'"][^\'"]*%(key)s[\'"]\s*,\s*\'--?[A-z]+\'\s*,\s*u?'
                      '[\'"])[^\"\']*([\'"])',
                      r'(%(key)s\s*--?[A-z]+\s*)\S+(\s*)']

# NOTE(dhellmann): Keep a separate list of patterns by key so we only
# need to apply the substitutions for keys we find using a quick "in"
# test.
for key in _SANITIZE_KEYS:
    _SANITIZE_PATTERNS_1[key] = []
    _SANITIZE_PATTERNS_2[key] = []

    for pattern in _FORMAT_PATTERNS_2:
        reg_ex = re.compile(pattern % {'key': key}, re.DOTALL)
        _SANITIZE_PATTERNS_2[key].append(reg_ex)

    for pattern in _FORMAT_PATTERNS_1:
        reg_ex = re.compile(pattern % {'key': key}, re.DOTALL)
        _SANITIZE_PATTERNS_1[key].append(reg_ex)

def mask_password(message, secret="***"):
    """Replace password with 'secret' in message.

    :param message: The string which includes security information.
    :param secret: value with which to replace passwords.
    :returns: The unicode value of message with the password fields masked.
    """

    try:
        message = six.text_type(message)
    except UnicodeDecodeError:
        # NOTE(jecarey): Temporary fix to handle cases where message is a
        # byte string. A better solution will be provided in Kilo.
        pass

    substitute1 = r'\g<1>' + secret
    substitute2 = r'\g<1>' + secret + r'\g<2>'

    # NOTE(ldbragst): Check to see if anything in message contains any key
    # specified in _SANITIZE_KEYS, if not then just return the message since
    # we don't have to mask any passwords.
    for key in _SANITIZE_KEYS:
        if key in message:
            for pattern in _SANITIZE_PATTERNS_2[key]:
                message = re.sub(pattern, substitute2, message)
            for pattern in _SANITIZE_PATTERNS_1[key]:
                message = re.sub(pattern, substitute1, message)

    return message
