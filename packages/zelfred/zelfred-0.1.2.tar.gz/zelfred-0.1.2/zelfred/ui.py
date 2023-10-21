# -*- coding: utf-8 -*-

"""
Alfred Workflow UI simulator.
"""

import typing as T
import time
import subprocess
import dataclasses

import readchar

from .vendor.os_platform import IS_WINDOWS
from . import exc
from . import events
from .item import T_ITEM, Item
from .line_editor import LineEditor
from .dropdown import Dropdown
from .render import UIRender
from .debug import debugger


key_to_name = {
    readchar.key.CTRL_C: "CTRL_C",
    readchar.key.TAB: "TAB",
    readchar.key.CTRL_X: "CTRL_X",
    readchar.key.UP: "UP",
    readchar.key.DOWN: "DOWN",
    readchar.key.CTRL_E: "CTRL_E",
    readchar.key.CTRL_D: "CTRL_D",
    readchar.key.CTRL_R: "CTRL_R",
    readchar.key.CTRL_F: "CTRL_F",
    readchar.key.LEFT: "LEFT",
    readchar.key.RIGHT: "RIGHT",
    readchar.key.HOME: "HOME",
    readchar.key.END: "END",
    readchar.key.CTRL_H: "CTRL_H",
    readchar.key.CTRL_L: "CTRL_L",
    readchar.key.CTRL_G: "CTRL_G",
    readchar.key.CTRL_K: "CTRL_K",
    readchar.key.BACKSPACE: "BACKSPACE",
    readchar.key.DELETE: "DELETE",
    readchar.key.ENTER: "ENTER",
    readchar.key.CR: "CR",
    readchar.key.LF: "LF",
    readchar.key.CTRL_A: "CTRL_A",
    readchar.key.CTRL_W: "CTRL_W",
    readchar.key.CTRL_P: "CTRL_P",
}

if IS_WINDOWS:
    OPEN_CMD = "start"
else:
    OPEN_CMD = "open"


@dataclasses.dataclass
class DebugItem(Item):
    def enter_handler(self, ui: "UI"):
        subprocess.run([OPEN_CMD, str(debugger.path_log_txt)])


T_HANDLER = T.Callable[[str, T.Optional["UI"]], T.List[T_ITEM]]


class UI:
    """
    Zelfred terminal UI implementation.

    :param handler: a callable function that takes a query string as input and
        returns a list of items.
    :param hello_message: sometimes the handler execution for the first time
        run takes long. This message will be shown to user to indicate that
        the handler is still running, and the UI will show the returned items
        once the handler is done.
    :param capture_error: whether you want to capture the error and show it
        in the UI, or you want to raise the error immediately.
    :param process_input_immediately: the handler will be called immediately
        after user input. This is the default behavior.
    :param process_input_after_query_delay: the handler will be called after
        a delay of `query_delay` seconds after the first user input. For example,
        let's say the query delay is 0.3 second. At begin, the user input is empty,
        then user entered "a". If then the user entered "bcd" within 0.3 second,
        the handler will not be called to give you the latest items. The handler
        will be called until the user entered a new key, let's say "e", from
        0.4 second after he entered "a".
    :param query_delay: read above.
    """

    def __init__(
        self,
        handler: T_HANDLER,
        hello_message: T.Optional[str] = "Welcome to interactive UI!",
        capture_error: bool = True,
        process_input_immediately: bool = False,
        process_input_after_query_delay: bool = False,
        query_delay: float = 0.3,
    ):
        # -------------------- input arguments
        self.handler: T_HANDLER = handler
        self._handler_queue: T.List[T_HANDLER] = list()
        self.hello_message: T.Optional[str] = hello_message
        self.capture_error: bool = capture_error
        self.query_delay: float = query_delay

        # -------------------- internal implementation related
        self.render: UIRender = UIRender()
        self.event_generator = events.KeyEventGenerator()
        self._process_input: T.Callable
        flag = sum(
            [
                process_input_immediately,
                process_input_after_query_delay,
            ]
        )
        if flag == 0:
            process_input_immediately = True
        elif flag > 1:
            raise ValueError
        else: # pragma: no cover
            pass

        if process_input_immediately:
            self._process_input = self._process_input_v1_immediately
        elif process_input_after_query_delay:
            self._process_input = self._process_input_v2_after_query_delay
        else:  # pragma: no cover
            raise NotImplementedError

        # -------------------- items related --------------------
        self.line_editor: LineEditor = LineEditor()
        self.dropdown: Dropdown = Dropdown([])
        self.n_items_on_screen: int = 0

        # -------------------- controller flags --------------------
        self.need_run_handler: bool = True
        self.need_move_to_end: bool = True
        self.need_clear_items: bool = True
        self.need_clear_query: bool = True
        self.need_print_query: bool = True
        self.need_print_items: bool = True
        self.need_process_input: bool = True

    def _debug_controller_flags(self):
        print(f"self.need_run_handler = {self.need_run_handler}")
        print(f"self.need_move_to_end = {self.need_move_to_end}")
        print(f"self.need_clear_items = {self.need_clear_items}")
        print(f"self.need_clear_query = {self.need_clear_query}")
        print(f"self.need_print_query = {self.need_print_query}")
        print(f"self.need_print_items = {self.need_print_items}")
        print(f"self.need_process_input = {self.need_process_input}")

    def replace_handler(self, handler: T_HANDLER):
        """
        Replace the current handler with a new handler, and push the current
        handler to the handler queue (a last in first out stack).
        """
        self._handler_queue.append(self.handler)
        self.handler = handler

    def _clear_query(self):
        """
        Clear the ``(Query): {user_query}`` line.
        """
        self.render.clear_line_editor()
        return True

    def clear_query(self):
        """
        A wrapper of the ``_clear_query()`` method, ensures that the
        ``need_clear_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- clear_query --------------------")
        try:
            if self.need_clear_query:
                debugger.log("before clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                self._clear_query()
                debugger.log("after clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_clear_query = True

    def _clear_items(self) -> bool:
        """
        Clear the item dropdown menu.
        """
        if self.render.line_number > 1:
            # time.sleep(1)
            self.render.clear_dropdown()
            # time.sleep(1)
            return True
        else:
            return False

    def clear_items(self):
        """
        A wrapper of the ``_clear_items()`` method, ensures that the
        ``need_clear_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- clear_items --------------------")
        try:
            if self.need_clear_items:
                debugger.log("before clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                flag = self._clear_items()
                debugger.log("after clear")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                if flag:
                    debugger.log(f"nothing happen")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_clear_items = True

    def _print_query(self):
        """
        Print the ``(Query): {user_query}`` line
        """
        content = self.render.print_line_editor(self.line_editor)
        debugger.log(f"printed: {content!r}")

    def print_query(self):
        """
        A wrapper of the core logic for printing query, ensures that the
        ``need_print_query`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- print_query --------------------")
        try:
            if self.need_print_query:
                debugger.log("before print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                self._print_query()
                debugger.log("after print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_print_query = True

    def _print_items(self):
        """
        Core logic for printing items in the dropdown menu.
        """
        debugger.log("render dropdown")
        n_items_on_screen = self.render.print_dropdown(
            self.dropdown, self.render.terminal.width
        )
        self.n_items_on_screen = n_items_on_screen

    def print_items(self):
        """
        A wrapper of the core logic for printint items, ensures that the
        ``need_print_items`` and ``need_run_handler`` flag is set to ``True``
        at the end regardless of whether an exception is raised.
        """
        debugger.log("-------------------- print_items --------------------")
        try:
            if self.need_print_items:
                debugger.log("before print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                self._print_items()
                # manually move the cursor to the edge to maximize the room for rendering
                self.render.move_down(1)
                self.render.move_up(1)
                debugger.log("after print")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            debugger.log(f"move_cursor_to_line_editor ...")
            debugger.log(f"render.line_number: {self.render.line_number}")
            debugger.log(f"render.n_lines: {self.render.n_lines}")
            # always move cursor back to line editor after printing items
            n_vertical, n_horizontal = self.render.move_cursor_to_line_editor(
                self.line_editor
            )
            debugger.log(f"n_vertical: {n_vertical}")
            debugger.log(f"n_horizontal: {n_horizontal}")
            self.need_print_items = True
            self.need_run_handler = True

    def process_key_pressed_input(self, pressed: str):
        """
        Process user keyboard input.

        - UP: move up
        - DOWN: move down
        - LEFT: move left
        - RIGHT: move right
        - HOME: move to start of the line
        - END: move to end of the line

        - CTRL + E: move up
        - CTRL + D: move down
        - CTRL + R: scroll up
        - CTRL + F: scroll down
        - CTRL + H: move left
        - CTRL + L: move right
        - CTRL + G: move word left
        - CTRL + K: move word right

        - CTRL + X: clear input

        Actions:

        - Enter:
        - CTRL + A:
        - CTRL + W:
        - CTRL + P:
        """
        pressed_key_name = key_to_name.get(pressed, pressed)
        debugger.log(f"pressed: {pressed_key_name!r}, key code: {pressed!r}")

        if pressed == readchar.key.CTRL_C:
            raise KeyboardInterrupt()

        if pressed == readchar.key.TAB:
            self.line_editor.clear_line()
            selected_item = self.dropdown.selected_item
            if selected_item.autocomplete:
                self.line_editor.enter_text(selected_item.autocomplete)
            return

        if pressed == readchar.key.CTRL_X:
            self.line_editor.clear_line()
            return

        if pressed in (
            readchar.key.UP,
            readchar.key.DOWN,
            readchar.key.CTRL_E,
            readchar.key.CTRL_D,
            readchar.key.CTRL_R,
            readchar.key.CTRL_F,
        ):
            self.need_run_handler: bool = False
            self.need_clear_query: bool = False
            self.need_print_query: bool = False

            if pressed in (readchar.key.UP, readchar.key.CTRL_E):
                self.dropdown.press_up()
            elif pressed in (readchar.key.DOWN, readchar.key.CTRL_D):
                self.dropdown.press_down()
            elif pressed == readchar.key.CTRL_R:
                self.dropdown.scroll_up()
            elif pressed == readchar.key.CTRL_F:
                self.dropdown.scroll_down()
            else:  # pragma: no cover
                raise NotImplementedError
            return

        # note: on windows terminal, the backspace and CTRL+H key code are the same
        # we have to sacrifice the CTRL+H key to keep BACKSPACE working,
        # so we put this code block before CTRL+H
        if pressed == readchar.key.BACKSPACE:
            self.line_editor.press_backspace()
            return

        if pressed == readchar.key.DELETE:
            self.line_editor.press_delete()
            return

        if pressed in (
            readchar.key.LEFT,
            readchar.key.RIGHT,
            readchar.key.HOME,
            readchar.key.END,
            readchar.key.CTRL_H,  # note, CTRL+H won't work on Windows
            readchar.key.CTRL_L,
            readchar.key.CTRL_G,
            readchar.key.CTRL_K,
        ):
            self.need_run_handler = False
            self.need_move_to_end = False
            self.need_clear_items = False
            self.need_clear_query = False
            self.need_print_query = False
            self.need_print_items = False
            if pressed in (readchar.key.LEFT, readchar.key.CTRL_H):
                self.line_editor.press_left()
            elif pressed in (readchar.key.RIGHT, readchar.key.CTRL_L):
                self.line_editor.press_right()
            elif pressed == readchar.key.HOME:
                self.line_editor.press_home()
            elif pressed == readchar.key.END:
                self.line_editor.press_end()
            elif pressed == readchar.key.CTRL_G:
                self.line_editor.move_word_backward()
            elif pressed == readchar.key.CTRL_K:
                self.line_editor.move_word_forward()
            else:  # pragma: no cover
                raise NotImplementedError
            return

        if pressed in (
            readchar.key.ENTER,
            readchar.key.CR,
            readchar.key.LF,
            readchar.key.CTRL_A,
            readchar.key.CTRL_W,
            readchar.key.CTRL_P,
        ):
            if self.dropdown.n_items == 0:
                raise exc.EndOfInputError(
                    selection="select nothing",
                )
            else:
                self.move_to_end()
                if self.dropdown.items:
                    selected_item = self.dropdown.selected_item
                    if pressed in (
                        readchar.key.ENTER,
                        readchar.key.CR,
                        readchar.key.LF,
                    ):
                        selected_item.enter_handler(ui=self)
                    elif pressed == readchar.key.CTRL_A:
                        selected_item.ctrl_a_handler(ui=self)
                    elif pressed == readchar.key.CTRL_W:
                        selected_item.ctrl_w_handler(ui=self)
                    elif pressed == readchar.key.CTRL_P:
                        selected_item.ctrl_p_handler(ui=self)
                    else:  # pragma: no cover
                        raise NotImplementedError
                raise exc.EndOfInputError(selection=selected_item)

        if pressed == readchar.key.F1:
            raise exc.JumpOutLoopError

        self.line_editor.press_key(pressed)

    def _process_input_v1_immediately(self):
        event = self.event_generator.next()
        if isinstance(event, events.KeyPressedEvent):
            self.process_key_pressed_input(pressed=event.value)

    def _process_input_v2_after_query_delay(self):
        start_time: T.Optional[float] = None
        while 1:
            event = self.event_generator.next()
            if isinstance(event, events.KeyPressedEvent):
                self.process_key_pressed_input(pressed=event.value)
            self.clear_query()
            self.print_query()
            self.render.move_cursor_to_line_editor(self.line_editor)
            if start_time is None:
                start_time = time.time()
            else:
                event_time = time.time()
                if event_time - start_time > self.query_delay:
                    break

    def process_input(self):
        """
        A wrapper of the core logic for processing input, ensures that the
        ``need_process_input`` flag is set to ``True`` at the end regardless of
        whether an exception is raised.
        """
        debugger.log("-------------------- process_input --------------------")
        try:
            if self.need_process_input:
                self._process_input()
        finally:
            self.need_process_input = True

    def run_handler(self, items: T.Optional[T.List[T_ITEM]] = None):
        if self.need_run_handler:
            debugger.log("need to run handler")
            if items is None:
                debugger.log("run handler")
                items = self.handler(self.line_editor.line, self)
            else:
                debugger.log("explicitly give items, skip handler")
            self.dropdown.update(items)

    def move_to_end(self):
        """
        Move the cursor to the next line of the end of the dropdown menu.
        """
        debugger.log("-------------------- move_to_end --------------------")
        try:
            if self.need_move_to_end:
                debugger.log("need to move to end")
                debugger.log("before move to end")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
                n_down = self.render.move_to_end()
                debugger.log(f"move down {n_down} lines")
                debugger.log("after move to end")
                debugger.log(f"render.line_number: {self.render.line_number}")
                debugger.log(f"render.n_lines: {self.render.n_lines}")
            else:
                debugger.log(f"nothing happen")
        finally:
            self.need_move_to_end = True

    def print_hello_items(self):
        items = [
            Item(
                uid="uid-hello-item",
                title="Welcome to the interactive UI",
            )
        ]
        self.dropdown.update(items)
        self.print_items()

    def print_debug_items(self, e: Exception):
        # if dropdown has items, then there must be one selected item
        # include the selected item information in the error message
        if self.dropdown.items:
            selected_item = self.dropdown.selected_item
            title = selected_item.title
            # handle the error in debug loop special case
            if title.startswith("Error on item: "):
                title = title[len("Error on item: ") :]
            processed_title = self.render.process_title(
                title,
                self.render.terminal.width - 15,
            )
            items = [
                DebugItem(
                    uid="uid",
                    title=f"Error on item: {processed_title}",
                    subtitle=f"{e!r}",
                )
            ]
        else:
            items = [
                DebugItem(
                    uid="uid",
                    title=f"Error on item: NA",
                    subtitle=f"{e!r}",
                )
            ]
        self.dropdown.update(items)
        self.print_items()

    def initialize_loop(self):
        debugger.log("=== initialize loop start ===")
        self.print_query() # show initial query, mostly it is empty
        self.print_hello_items() # show hello items
        self.run_handler() # run handler using initial query
        self.move_to_end() # move cursor to the end
        self.clear_items() # clear items
        self.clear_query() # clear query
        self.print_query() # print query
        self.print_items() # print items
        debugger.log("=== initialize loop end ===")

    def main_loop(self, _ith: int=0):
        while True:
            _ith += 1
            debugger.log(f"=== {_ith}th main loop start ===")
            self.process_input()
            # self._debug_controller_flags()
            self.run_handler()
            self.move_to_end()
            self.clear_items()
            self.clear_query()
            self.print_query()
            self.print_items()
            debugger.log(f"=== {_ith}th main loop end ===")

    def debug_loop(self, e: Exception):
        """
        Display error message in the UI and wait for new user input.
        New user input may fix the problem or trigger another error.
        """
        debugger.log("=== debug loop start ===")
        self.move_to_end()
        self.clear_items()
        self.clear_query()
        self.print_query()
        self.print_debug_items(e)
        debugger.log("=== debug loop end ===")

    def run(self, _do_init: bool = True):
        """
        Run the UI.

        Read :ref:`ui-event-loop`
        (or `this link <https://zelfred.readthedocs.io/en/latest/03-UI-Event-Loop/index.html>`_)
        for more information.
        """
        try:
            if _do_init:
                self.initialize_loop()
            self.main_loop()
        except exc.EndOfInputError as e:
            return e.selection
        except exc.JumpOutLoopError as e:
            if self._handler_queue:
                self.handler = self._handler_queue.pop()
            self.line_editor.clear_line()
            self.run_handler()
            self.move_to_end()
            self.clear_items()
            self.clear_query()
            self.print_query()
            self.print_items()
            return self.run(_do_init=False)
        except Exception as e:
            if self.capture_error:
                self.debug_loop(e)
                return self.run(_do_init=False)
            else:
                raise e
        finally:
            print("")
