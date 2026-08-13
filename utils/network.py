import ctypes
import threading
import socket

iphlpapi = ctypes.windll.iphlpapi

CALLBACK_FUNC = ctypes.WINFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)

wake_event = threading.Event()  # the "sleeping thread" signal


def on_network_change(context, row_ptr, notification_type):
    # Don't trust notification_type or row_ptr contents — just wake up.
    wake_event.set()


def is_online() -> bool:
    # Real ground truth check, done by us, not inferred from the event.
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


def main():
    callback = CALLBACK_FUNC(on_network_change)
    handle = wintypes.HANDLE() if False else ctypes.c_void_p()  # placeholder, fixed below
    handle = ctypes.c_void_p()

    result = iphlpapi.NotifyIpInterfaceChange(
        0,          # AF_UNSPEC
        callback,
        None,
        False,      # don't fire immediately
        ctypes.byref(handle)
    )
    if result != 0:
        print(f"Failed to register. Error code: {result}")
        return

    print("Sleeping. Waiting for OS to wake this thread on network change...")

    last_state = is_online()
    try:
        while True:
            wake_event.wait()      # thread sleeps here, zero CPU, until callback fires
            wake_event.clear()
            state = is_online()
            if state != last_state:
                print("Hello" if state else "Bye")
                last_state = state
    except KeyboardInterrupt:
        iphlpapi.CancelMibChangeNotify2(handle)
        print("\nStopped.")


if __name__ == "__main__":
    main()