import os
from ctypes import cdll, c_char_p


def decrypt_passwd(passwd, so_path="./lib/passwd.so"):
    try:
        lib = cdll.LoadLibrary(so_path)
        lib.passedDecrypt.argtypes = [c_char_p]
        lib.passedDecrypt.restype = c_char_p
        password = lib.passedDecrypt(passwd.encode()).decode()
        return password
    except Exception:
        return passwd


class BasicConfig(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # SQLALCHEMY_ENGINE_OPTIONS
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,   # 每次從 Connection Pool 取得連線時，就試著執行一次相當於 SELECT 1 的 SQL ，如果有問題，就可以重新建立新的連線取代失效的連線。
        'pool_recycle': 60,      # 设置 DBAPI connection 存活多久断开
        'pool_timeout': 100,     # 从 pool 中获取新的连接等待时间，一般是指等待 pool 中连接可用的时间
        'pool_size': 10,         # The size of the pool to be maintained, defaults to 5.
        'max_overflow': 100,     # 允许超过 pool_size 多少
    }

