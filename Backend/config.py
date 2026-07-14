class Config:
    SQLALCHEMY_DATABASE_URI= 'sqlite:///models.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECRET_KEY = 'my_secret_database'
    SECURITY_PASSWORD_SALT = 'MY_SECRET_SALT'

    # Mail Configuration
    # MAIL_SERVER='smtp.gmail.com' #for gmail test
    # MAIL_PORT=587 # stand TLS email port
    # MAIL_USE_TLS=True
    # MAIL_USERNAME='[EMAIL_ADDRESS]'
    # MAIL_PASSWORD='[PASSWORD]'
    # MAIL_DEFAULT_SENDER='[EMAIL_ADDRESS_college]'