from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()


include(
    'components/basics.py',
    'components/database.py',
    'components/applications.py',
    'components/password_validation.py',
    'components/internalization.py',
)

LOCALE_PATHS = ['movies/locale']
