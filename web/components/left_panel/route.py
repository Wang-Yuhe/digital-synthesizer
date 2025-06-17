from flask import Blueprint, render_template

left_panel_bp = Blueprint('left_panel', __name__,
                          template_folder='.',
                          static_folder='.',
                          static_url_path='/static/left_panel')

@left_panel_bp.route('/')
def index():
    return render_template('index.html')
