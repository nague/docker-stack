class Services(object):

    # MySQL
    # https://hub.docker.com/_/mysql/
    def mysql(self, args):
        # Default values
        data = {
            'restart': 'always',
            'volumes': ['./db:/docker-entrypoint-initdb.d'],
            'environment': {}
        }
        # Version is required
        if 'version' not in args:
            raise KeyError('version is missing... aborting')
        data['image'] = 'mysql:{}'.format(args['version'])
        # Ports
        if 'ports' in args:
            data['ports'] = args['ports']
        else:
            data['ports'] = [3306]
        # MYSQL environment keys
        for key in [
            'user',
            'password',
            'database',
            'root_password',
            'allow_empty_password',
            'random_root_password',
            'onetime_password'
        ]:
            if key in args:
                data['environment']['MYSQL_{}'.format(str(key).upper())] = args[key]

        return data

    # Docker-SMTP
    # https://hub.docker.com/r/namshi/smtp/
    def smtp(self, args):
        # Default values
        data = {
            'image': 'namshi/smtp',
            'environment': {}
        }
        # Ports
        if 'ports' in args:
            data['ports'] = args['ports']
        else:
            data['ports'] = [25]
        # SMTP environment keys
        for key in [
            'key_path',
            'certificate_path',
            'mailname',
            'relay_domains',
            'relay_networks',
            'ses_user',
            'ses_password',
            'ses_region',
            'gmail_user',
            'gmail_password',
            'smarthost_address',
            'smarthost_port',
            'smarthost_user',
            'smarthost_password',
            'smarthost_aliases'
        ]:
            if key in args:
                data['environment'][str(key).upper()] = args[key]

        return data
