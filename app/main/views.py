from flask import render_template, flash, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from ..models import User, Menu
from .. import db,photos
from . import main
