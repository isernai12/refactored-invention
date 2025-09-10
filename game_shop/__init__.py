import os
from flask import Flask
import datetime
import pytz
from datetime import timedelta

# সময়কে বাংলাদেশ সময়ে রূপান্তর করার জন্য ফাংশন
def format_datetime_bst(utc_dt):
    if not utc_dt:
        return ""

    utc_timezone = pytz.timezone('UTC')
    # naive datetime কে aware করার জন্য localize ব্যবহার করা হয়
    if utc_dt.tzinfo is None:
        utc_dt = utc_timezone.localize(utc_dt)

    bst_timezone = pytz.timezone('Asia/Dhaka')
    bst_dt = utc_dt.astimezone(bst_timezone)

    return bst_dt.strftime('%d-%m-%Y, %I:%M:%S %p')

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='SHIWISHF828398R83U2JBWNDO919',
        # নিচের এই লাইনে আপনার PostgreSQL লিঙ্কটি বসানো হয়েছে
        DATABASE='postgresql://atopip_user:QW7SpBuDChO4yeMGMedeodl5lYEk9zYg@dpg-d2van9nfte5s73btn8hg-a/atopip',
        PERMANENT_SESSION_LIFETIME=timedelta(days=30)
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # bst_time ফিল্টারটি রেজিস্টার করা হচ্ছে
    app.jinja_env.filters['bst_time'] = format_datetime_bst

    # app.jinja_env.add_extension('jinja2.ext.date') <-- এই লাইনটি এখন আর প্রয়োজন নেই

    # ব্লুপ্রিন্ট রেজিস্টার করা
    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import views
    app.register_blueprint(views.bp)

    from . import user_auth
    app.register_blueprint(user_auth.bp)

    app.add_url_rule('/', endpoint='index')

    return app
