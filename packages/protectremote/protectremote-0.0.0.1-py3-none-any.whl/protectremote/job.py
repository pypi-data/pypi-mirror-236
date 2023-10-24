from protectremote.main import RuleService
from python_settings import settings 


def update_request_data():
    try:
        service = RuleService()
        data = service.post_rules()
        settings.RULES_DATA = data
        print('Data updated...', settings.RULES_DATA)
    except Exception as e:
        print("data couldnt updated", e)
    