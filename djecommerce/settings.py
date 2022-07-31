import os

# Admin User- myadmin
# passsword-Uzair@76330
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = ['127.0.0.1', 'shopcygen.uzair.herokuapp.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'core.apps.CoreConfig',
    'crispy_forms',
    'django_countries',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

SITE_ID = 1
ROOT_URLCONF = 'djecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Auth
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',


]

LOGIN_REDIRECT_URL = "/"
# bootstrap template
CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# Email Message
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "ddark317@gmail.com"
# EMAIL_HOST_PASSWORD = 'Iojknm@8805'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ddark317@gmail.com'
EMAIL_HOST_PASSWORD = 'kssddzwljfblcppc'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#  Ack AllAuth about signup form
# ACCOUNT_SIGNUP_FORM_CLASS = 'userauth.forms.SignupForm'

# paypal


# STRIPE_SECRET_KEY = 'sk_test_51HRJw5JM7ki6t5T7EYwgNzFYjMhqsJkngCZbASJoXXFjt5aWNQEqOGALCrVkVFniYKW08OTMCT52WDp57AVKBDMG00ftWQYWs8'
# STRIPE_PUBLIC_KEY = 'pk_test_51HRJw5JM7ki6t5T7wIGiQCQ2YXWhBsLFHmhoARs32woYGLLGVXdeUwzSf0RMet183D8GMxVfnsiwuBJvwGstU9Ll00VXwJJyAc'
TIME_ZONE = 'Asia/Kolkata'
