def paginate(page):
    per_page = 10
    start = (page - 1) * per_page
    end = page * per_page
    return [start, end, per_page]


def response(data=None, message=None, is_success=True, total=None, current_page=None,
             last_page=None, per_page=None):
    result = {
        'data': data,
        'message': message,
        'is_success': is_success,
        'current_page': current_page,
        # 'first_page_url': first_page_url,
        'last_page': last_page,
        # 'last_page_url': last_page_url,
        'total': total,
        'per_page': per_page
    }
    return result
