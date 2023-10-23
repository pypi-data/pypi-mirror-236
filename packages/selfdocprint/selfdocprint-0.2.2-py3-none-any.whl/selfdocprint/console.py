import time

def clear(clear_buffer: bool = False, delay: float = 0.1):
    """Clears the screen of the console and positions the cursor at the top left.

    Args:
        clear_buffer (bool, optional): If set to true this will also clear the console's history. Defaults to False.
        delay (float, optional): Delay to allow the OS to clear the screen. Try increasing this value if the ouptut looks garbled. Defaults to 0.1.
    """
    print("\033[1J", end="")  # clear the screen
    if clear_buffer:
        print("\033[3J", end="")  # clear the buffer
    time.sleep(delay)
    print("\033[0;0H", end="")  # move cursor to 0,0

