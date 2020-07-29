import os
from flask import render_template, Blueprint, request, redirect, url_for, flash
from projeto_base.ej.models import Ej
from projeto_base import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user

ej = Blueprint('ej', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "principal.index"
