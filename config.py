import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY') or 'AIzaSyC_pA_JzB5m_ZM-dKRx_CBTwfrq0SYq0jc'
