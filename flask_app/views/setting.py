from flask import Blueprint, render_template, redirect, url_for, request

setting_bp = Blueprint('setting', __name__)

# TODO : 設定画面の実装
@setting_bp.route('/setting')
def setting():
	return render_template('setting_index.html')

@setting_bp.route('/setting/edit', methods=['GET', 'POST'])
def setting_edit():
    if request.method == 'POST':
        return redirect(url_for('setting.setting'))
    else:
        return render_template('setting_edit.html')