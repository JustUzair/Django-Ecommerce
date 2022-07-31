import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings')

application = get_wsgi_application()
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(get_wsgi_application())

path = '/home/cryptoassistant/tfg/'
if path not in sys.path:
    sys.path.append(path)