import flask
from commons import get_env_or_fail
import mc_backup_delete
import mc_backup_create

if __name__ == '__main__':
    app = flask.Flask(__name__)

    @app.route('/delete', methods=['POST'])
    def delete_old_backups():
        max_age = int(flask.request.args['max_age'])
        deleted_backups = mc_backup_delete.delete_old_backups(max_age)
        return str(list(deleted_backups))

    @app.route('/create', methods=['POST'])
    def create_backup():
        return mc_backup_create.create_default_backup()

    app.run(host='0.0.0.0', port=get_env_or_fail('BACKUP_SERVER_PORT'))
