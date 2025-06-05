from django.core.cache import cache

def is_code_limited(email):
    return cache.get(f'code_limited_{email}') is not None


def set_code_limited(email, timeout=300):
    return cache.set(f'code_limited_{email}', True, timeout=timeout)



