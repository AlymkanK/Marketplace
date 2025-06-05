from django.core.cache import cache

def code_valid(email, code):
    key = f'sms_code_{email}'
    cached_code = cache.get(key)
    if cached_code and str(cached_code) == str(code):
        cache.delete(key)
        return True
    return False