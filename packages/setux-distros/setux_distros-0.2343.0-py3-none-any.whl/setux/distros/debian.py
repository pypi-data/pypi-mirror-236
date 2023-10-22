from setux.core.distro import Distro


class Debian(Distro):
    Package = 'apt'
    Service = 'SystemD'
    pip_cmd = 'pip3'

    @classmethod
    def release_name(cls, infos):
        did = infos['ID'].strip().capitalize()
        ver = infos['VERSION_ID'].strip('\r"')
        return f'{did}_{ver}'


class Debian_9(Debian):
    ''' Stretch '''


class Debian_10(Debian):
    ''' Buster '''


class Debian_11(Debian):
    ''' Bullseye '''

