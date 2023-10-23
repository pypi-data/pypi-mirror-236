### move media

import toml
from pprint import pprint
import os
import shutil
import time


def load_config(
    config
):
    """Load config.

    Args:
        config: config file to load
    """
    config_dict = toml.load(config)
    return config_dict


def transmission_media(config_dict):
    """Handle transmission media.

    Args:
        config_dict: config dict
    """
    from transmission_rpc import Client
    tc = Client(
        host=config_dict['transmission']['host'],
        port=config_dict['transmission']['port'],
        username=config_dict['transmission']['username'],
        password=config_dict['transmission']['password']
    )
    for torrent in reversed(tc.get_torrents()):
        if torrent.progress != 100.0:
            continue
        if torrent.download_dir not in config_dict['transmission']['dirs']:
            continue
        move_dir = config_dict['transmission']['dirs'][torrent.download_dir]

        try:
            from_dir = config_dict['transmission']['os_dirs'][torrent.download_dir]
            source_dir = os.path.join(from_dir, torrent.name)
        except KeyError:
            source_dir = os.path.join(torrent.download_dir, torrent.name)

        try:
            minutes_done_wait = config_dict['transmission']['wait_done_time_minutes'][torrent.download_dir]
        except KeyError:
            minutes_done_wait = None

        if minutes_done_wait is not None:
            try:
                if torrent.date_done is not None:
                    from .date_funcs import dt_x_minutes_ago
                    check_dt = dt_x_minutes_ago(
                        minutes_done_wait,
                        tzinfo=torrent.date_done.tzinfo
                    )
                    if config_dict['startup']['debug'] is True:
                        print('check_date time seconds.')
                        pprint(check_dt)
                        print('current torrent date')
                        pprint(torrent.date_done)
                    # if date is not done, than not doing anythong
                    if torrent.date_done > check_dt:
                        if config_dict['startup']['debug'] is True:
                            print('skipping because done age is to young.')
                        continue
                    else:
                        if config_dict['startup']['debug'] is True:
                            print('ok moving because done age is older than..')
                else:
                    continue
            except AttributeError:
                continue

        print(f"{torrent.name}: -> {move_dir}")

        if config_dict['startup']['dry_run'] is True:
            print('dry_run.... skipping.')
            continue
        try:
            shutil.move(source_dir, move_dir)
        except Exception as e:  # noqa:B902
            print(f"failed moving file/dir. >>{source_dir}<< error: {e}")
            unknown_error = True
            # by no such file or directory we want to remove torrent...
            if "No such file or directory:" in str(e):
                unknown_error = False
            if unknown_error is True:
                continue
        tc.remove_torrent(torrent.id, delete_data=True)


def media_run(
    config_dict
):
    """Media run.

    Args:
        config_dict: config  dict
    """
    if 'transmission' in config_dict:
        transmission_media(config_dict)


def media_entry(
    config,
    debug=False,
    dry_run=False,
):
    """Media run.

    Args:
        config: config file to load
        debug: debug
        dry_run: do a dryrun
    """
    config_dict = load_config(config)
    config_dict['startup'] = {
        'debug': debug,
        'dry_run': dry_run
    }
    if debug is True:
        pprint(config_dict)
    move_media = config_dict.get('move-media', [])
    conf_repeat = move_media.get('repeat', False)
    conf_delay = move_media.get('delay', 60)
    if conf_repeat is False:
        media_run(config_dict)
    else:
        while True:
            media_run(config_dict)
            print(f"sleeping for {conf_delay} seconds, before next run.")
            time.sleep(conf_delay)
    pprint(config_dict)
