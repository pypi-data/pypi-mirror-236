"""
thread_utils.py - Thread Utilities Module

This module provides utility functions for working with threads in Python.

Usage:
    import abstract_utilities.thread_utils as thread_utils

Example:
    # Creating a thread
    my_thread = thread_utils.get_thread(target=my_function, args=(arg1, arg2), daemon=True)

    # Starting the thread
    thread_utils.start_thread(my_thread)

    # Verifying if a given object is a valid thread
    is_valid = thread_utils.verify_thread(my_thread)

    # Checking if a thread is alive
    if thread_utils.thread_alive(my_thread):
        print("Thread is alive")
    else:
        print("Thread is not alive")

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""

import threading
from .type_utils import T_or_F_obj_eq
import queue
class ThreadedEvent:
    def __init__(self, target_function):
        self._event = threading.Event()
        self._queue = queue.Queue()  # Add a queue for return values
        self._thread = threading.Thread(target=self._run, args=(target_function,))


    def _run(self, target_function):
        while not self._event.is_set():
            result = target_function()
            self._queue.put(result)  # Store the return value in the queue
            self._event.wait(60)  # This will wait for 60 seconds or until interrupted by calling `stop`.
    def get_result(self):
        """Retrieve the result from the queue. Returns None if no result available."""
        if not self._queue.empty():
            return self._queue.get()
        return None
    def start(self):
        """Starts the thread."""
        self._thread.start()

    def stop(self):
        """Stops the thread."""
        self._event.set()
        #self._thread.join()  # Optionally, you can wait for the thread to finish.

    def is_alive(self):
        """Returns whether the thread is still running."""
        return self._thread.is_alive()
class ThreadManager:
    def __init__(self):
        self.threads = {}

    def add_thread(self, name, target_function):
        """Add a thread with a name and target function."""
        self.threads[name] = ThreadedEvent(target_function)

    def start(self, name):
        """Start a specific thread by name."""
        if not self.is_alive(name):
            self.threads[name].start()

    def stop(self, name):
        """Stop a specific thread by name."""
        self.threads[name].stop()

    def start_all(self):
        """Start all threads."""
        for thread in self.threads.values():
            thread.start()

    def stop_all(self):
        """Stop all threads."""
        for thread in self.threads.values():
            thread.stop()

    def is_alive(self, name):
        """Check if a specific thread is alive by name."""
        return self.threads[name].is_alive()

    def all_alive(self):
        """Return a dictionary indicating if each thread is alive."""
        return {name: thread.is_alive() for name, thread in self.threads.items()}

def get_thread(target=None, args=(), daemon=True) -> threading.Thread:
    """
    Returns a threading.Thread object with the provided target function, arguments, and daemon status.

    Args:
        target: The target function for the thread to execute.
        args: The arguments to pass to the target function.
        daemon (bool): The daemon status of the thread.

    Returns:
        threading.Thread: A threading.Thread object.
    """
    return threading.Thread(target=target, args=args, daemon=daemon)

def start_thread(thread=None):
    """
    Starts the specified thread if it is valid.

    Args:
        thread (threading.Thread): The thread to start.
    """
    if verify_thread(thread):
        thread.start()

def verify_thread(thread=None) -> bool:
    """
    Checks if the given object is a valid threading.Thread object.

    Args:
        thread: The object to check.

    Returns:
        bool: True if the object is a threading.Thread object, False otherwise.
    """
    return T_or_F_obj_eq(type(thread), type(threading.Thread()))

def thread_alive(thread) -> bool:
    """
    Checks if the specified thread is currently alive.

    Args:
        thread (threading.Thread): The thread to check.

    Returns:
        bool: True if the thread is alive, False otherwise.
    """
    if verify_thread(thread):
        return thread.is_alive()
    return False
