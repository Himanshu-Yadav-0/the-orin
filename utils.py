import psutil


def is_wifi_connected() -> bool:
    return psutil.net_if_stats()['Wi-Fi'].isup