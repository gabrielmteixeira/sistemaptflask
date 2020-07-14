from flask import render_template, Blueprint, request, redirect, url_for, flash

ej = Blueprint('ej', __name__, template_folder='templates')
