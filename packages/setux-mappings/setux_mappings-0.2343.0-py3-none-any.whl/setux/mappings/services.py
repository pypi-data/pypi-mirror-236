from setux.core.mapping import Services


class Debian(Services):
    mapping = dict(
        cups = 'cupsd',
    )


class FreeBSD(Services):
    mapping = dict(
        ssh  = 'sshd',
        cups = 'cupsd',
    )
