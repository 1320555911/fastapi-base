"""
    Settings
"""
import os
from logging import INFO

# 默认非调试模式
DEBUG = bool(os.getenv('DEBUG'))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TIME_ZONE = 'Asia/Shanghai'

# for jwt token
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION = eval(
    os.getenv('JWT_EXPIRATION', '0')) or 60 * 60 * 24  # seconds

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'upload')

DIR_KN_GRAPH = os.path.join(MEDIA_ROOT, 'kn_graph')
DIR_LOG = os.path.join(BASE_DIR, 'log')

# create needed directory
for d in [MEDIA_ROOT, DIR_KN_GRAPH, DIR_LOG]:
    if not os.path.exists(d):
        os.makedirs(d)

# ****************************** For OBS ***************************
OBS_ACCESS_KEY_ID = os.getenv('OBS_ACCESS_KEY_ID')
OBS_SECRET_ACCESS_KEY = os.getenv('OBS_SECRET_ACCESS_KEY')
OBS_ENDPOINT = os.getenv('OBS_ENDPOINT')
OBS_SERVER = f'https://{OBS_ENDPOINT}'

OBS_BUCKET = os.getenv('OBS_BUCKET', 'tjcloud-knowledge-graph')
OBS_DIR_ROOT = os.getenv('OBS_DIR_ROOT', 'knowledge_work_test')
OBS_GES_IMPORT = os.getenv('OBS_GES_IMPORT', 'ges_imports')
OBS_IMPORT_MODEL = os.getenv('OBS_IMPORT_MODEL', 'import_model')
OBS_SUBJECT_ICON = os.getenv('OBS_DIR_SUBJECT_ICON', 'subject_icon')
OBS_SUBJECT_IMG = os.getenv('OBS_DIR_SUBJECT_IMG', 'subject_img')
OBS_UPLOAD_KN_GRAPH = os.getenv('OBS_DIR_UPLOAD_KN_GRAPH', 'upload_kn_graph')
OBS_VERSION_ICON = os.getenv('OBS_DIR_VERSION_ICON', 'version_icon')
OBS_DIR_AVATAR = f'{OBS_DIR_ROOT}/avatar'
OBS_DIR_LOG = f'{OBS_DIR_ROOT}/logs'

OBS_BASE_URL = f'https://{OBS_BUCKET}.{OBS_ENDPOINT}'
OBS_AVATAR_DEFAULT = f'{OBS_BASE_URL}/{OBS_DIR_AVATAR}/avatar.jpg'
MODEL_PUBLIC_URL = f'{OBS_BASE_URL}/{OBS_DIR_ROOT}/{OBS_IMPORT_MODEL}'
SUBJECT_IMG_URL = f'{OBS_BASE_URL}/{OBS_DIR_ROOT}/{OBS_SUBJECT_IMG}'
SUBJECT_ICON_URL = f'{OBS_BASE_URL}/{OBS_DIR_ROOT}/{OBS_SUBJECT_ICON}'

# ************************* For HuaweiCloud SDK ********************
# reference https://support.huaweicloud.com/api-ges/ges_03_0132.html
IAM_USERNAME = os.getenv('IAM_USERNAME')  # IAM用户名
IAM_PASSWORD = os.getenv('IAM_PASSWORD')  # IAM用户密码
HW_DOMAIN_NAME = os.getenv('HW_DOMAIN_NAME')  # 账号名
HW_DOMAIN_ID = os.getenv('HW_DOMAIN_ID')  # 账号ID
HW_PROJECT_NAME = os.getenv('HW_PROJECT_NAME')  # 所属区域名称:cn-east-3
HW_PROJECT_ID = os.getenv('HW_PROJECT_ID')  # 所属区域ID
GES_SERVER_URL = os.getenv('GES_SERVER_URL')  # GES公网IP
GES_GRAPH_NAME = os.getenv('GES_GRAPH_NAME')  # 图实例名称
GES_GRAPH_ID = os.getenv('GES_GRAPH_ID')  # 图实例ID
GES_ENDPOINT = os.getenv('GES_ENDPOINT')  # 终端节点
GES_TOKEN_CHECK_INTERVAL = int(
    os.getenv('GES_CHECK_TOKEN_INTERVAL', '30'))  # 校验token间隔 分钟
GES_UPDATE_TOKEN_INTERVAL = eval(
    os.getenv('GES_UPDATE_TOKEN_INTERVAL', '60*60'))  # 应用从 Redis 获取最新token间隔 秒
GES_BATCH_VERTEX_MAX = int(os.getenv('GES_BATCH_VERTEX_MAX', 10000))
GES_BATCH_EDGE_MAX = int(os.getenv('GES_BATCH_VERTEX_MAX', 10000))

CACHE_EXPIRATION = 60 * 60 * 24

CAPTCHA_EXPIRATION = 300

CAPTCHA_RESEND_INTERVAL = 60

# for redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT') or '6379')
REDIS_MAX_CONNECTION = int(os.getenv('REDIS_MAX_CONNECTION') or '10')
REDIS_DB_DEFAULT = int(os.getenv('REDIS_DB_DEFAULT') or '1')
REDIS_DB_LABEL = int(os.getenv('REDIS_DB_LABEL') or '2')
REDIS_DB_SESSION = int(os.getenv('REDIS_DB_SESSION') or '3')
REDIS_DB_EXTERNAL = int(os.getenv('REDIS_DB_EXTERNAL') or '4')
REDIS_DB_CELERY = int(os.getenv('REDIS_DB_CELERY') or '5')
REDIS = {
    'default': REDIS_DB_DEFAULT,
    'session': REDIS_DB_SESSION,
    'label': REDIS_DB_LABEL,
    'external': REDIS_DB_EXTERNAL
}

# for uvicorn
RELOAD_DIRS = [
    os.path.join(BASE_DIR, 'api'),
    os.path.join(BASE_DIR, 'control'),
    os.path.join(BASE_DIR, 'api_external'),
    os.path.join(BASE_DIR, 'model'),
    os.path.join(BASE_DIR, 'fastapi'),
    os.path.join(BASE_DIR, 'utils'),
]

# cors origins
# 默认不使用跨域
CORS_ORIGINS_APP = eval(os.getenv('CORS_ORIGINS_APP', '[]'))
CORS_ORIGINS_EXTERNAL = eval(os.getenv('CORS_ORIGINS_EXTERNAL', '[]'))
CORS_ORIGINS_ALGORITHM = eval(os.getenv('CORS_ORIGINS_ALGORITHM', '[]'))


# for log
LOG_LEVEL = eval(os.getenv('LOG_LEVEL', f'{INFO}'))
LOG_ROTATION = os.getenv('LOG_ROTATION', '1 week')
LOG_RETENTION = os.getenv('LOG_RETENTION', '1 month')
LOG_DIAGNOSE = bool(os.getenv('LOG_DIAGNOSE'))

