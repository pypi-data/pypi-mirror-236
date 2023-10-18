""" simple dns server """

from flask import Flask, request
from psycopg2 import Error as PGError  # type: ignore
from teamhack_db.sql import drop_row_hostname_recordtype, drop_row_hostname # type: ignore
from teamhack_db.sql import drop_row_ip, insert  # type: ignore
from teamhack_db.sql import select_hostname_recordtype, select_hostname, select_ip  # type: ignore
from teamhack_db.util import get_name, get_record_type  # type:ignore


def create_app(conn):
    """ create the app """
    app = Flask(__name__)
    # api = Api(app)

    def dispatch(data, hostname_recordtype_cb, hostname_cb, ip_cb):
        """ helper for retrieve/delete """
        if 'host' in data and 'type' in data:
            host = data['host']
            host = get_name(host)
            rt = data['type']
            rt = get_record_type(rt)
            assert rt is not None
            assert rt != ''
            assert rt
            print(
                f"hostname_recordtype_cb(host={host}, type={data['type']} ({rt}))")
            ret = hostname_recordtype_cb(conn, host, rt)
            return ret
        if 'host' in data and 'type' not in data:
            host = data['host']
            host = get_name(host)
            print(f'hostname_cb(host={host})')
            ret = hostname_cb(conn, host)
            return ret
        if 'inet' in data:
            addr = data['inet']
            print(f'ip_cb(addr={addr})')
            ret = ip_cb(conn, addr)
            return ret
        return '', 404



    @app.route('/create', methods=['POST'])
    def add():
        """ create a dns entry """
        data = request.get_json(force=True)
        if 'host' not in data:
            return '', 404
        host = data['host']
        host = get_name(host)
        print(f"add(host={host})")
        if 'type' not in data:
            return '', 404
        rt = data['type']
        print(f"add(type={rt})")
        rt = get_record_type(rt)
        assert rt
        if 'inet' not in data:
            return '', 404
        addr = data['inet']
        print(f"insert(host={host}, type={data['type']}, addr={addr})")
        try:
            insert(conn, host, rt, addr)
            conn.commit()
            # return ret
            return ''
        except PGError as e:
            print(f"Error: {e}")
            conn.rollback()
            return 'DB Error', 204

    @app.route('/retrieve', methods=['POST'])
    def retrieve():
        """ retrieve a dns entry """
        data = request.get_json(force=True)
        return dispatch(data, select_hostname_recordtype, select_hostname, select_ip)

    @app.route('/update', methods=['POST'])
    def update():
        """ update a dns entry """
        return 'Not Implemented', 404

    @app.route('/delete', methods=['POST'])
    def delete():
        """ delete a dns entry """
        data = request.get_json(force=True)
        try:
            dispatch(data, drop_row_hostname_recordtype,
                           drop_row_hostname, drop_row_ip)
            conn.commit()
            return ''
        except PGError as e:
            print(f"Error: {e}")
            conn.rollback()
            return 'DB Error', 204

    return app


def start_server(conn, *args, host="0.0.0.0", port=5001, **kwargs):
    """ start the server """
    app = create_app(conn)
    app.run(debug=True, host=host, port=port, *args, **kwargs)
