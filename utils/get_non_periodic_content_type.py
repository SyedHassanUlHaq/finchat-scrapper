from utils.check_cagny import check_cagny
from utils.check_bank import check_bank


def get_non_periodic_content_type(text, path, type):
    content_type = 'other'
    if check_bank(text):
        content_type = f'sellside_conference_{type}'
    elif check_cagny(text, path):
        content_type = f'industry_conference_{type}'
    else:
        content_type = f'company_conference_{type}'
    return content_type