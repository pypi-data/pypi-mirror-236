from collections.abc import Callable
from threading import Thread
from time import sleep
from uuid import uuid4

from dearpygui import dearpygui as dpg
from pymem.exception import MemoryReadError, MemoryWriteError

from trainerbase.gameobject import GameObject


class Script:
    DPG_TAG_PREFIX = "script__"

    def __init__(self, callback: Callable, enabled: bool = False):
        self.callback = callback
        self.enabled = enabled
        self.dpg_tag = f"{Script.DPG_TAG_PREFIX}{uuid4()}"

    def __repr__(self):
        return (
            f"<Script {getattr(self.callback, '__name__', 'Anon')}:"
            f" enabled={self.enabled},"
            f" dpg_tag={repr(self.dpg_tag)}"
            f">"
        )

    def __call__(self):
        return self.callback()


class ScriptEngine:
    def __init__(self, delay: float = 0.05):
        self.delay = delay
        self.should_run = False
        self.thread = Thread(target=self.script_loop)
        self.scripts: list[Script] = []

    def __repr__(self):
        return f"<ScriptEngine delay={self.delay} should_run={self.should_run} scripts={len(self.scripts)}>"

    def start(self):
        self.should_run = True
        self.thread.start()

    def stop(self):
        self.should_run = False
        self.thread.join()

    def script_loop(self):
        while self.should_run:
            try:
                for script in self.scripts:
                    if script.enabled:
                        script()
            except (MemoryReadError, MemoryWriteError):
                continue
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(e)
                self.stop()

            sleep(self.delay)

    def register_script(self, script: Script) -> Script:
        self.scripts.append(script)
        return script

    def simple_script(self, executor: Callable) -> Script:
        script = Script(executor)
        self.register_script(script)
        return script


system_script_engine = ScriptEngine()


@system_script_engine.simple_script
def update_frozen_objects():
    for game_object in GameObject.updated_objects:
        if game_object.frozen is not None:
            try:
                game_object.value = game_object.frozen
            except MemoryWriteError:
                continue


@system_script_engine.simple_script
def update_displayed_objects():
    for game_object in GameObject.updated_objects:
        if dpg.does_alias_exist(game_object.dpg_tag_getter):
            try:
                dpg.set_value(game_object.dpg_tag_getter, game_object.value)
            except MemoryReadError:
                continue


update_frozen_objects.enabled = True
update_displayed_objects.enabled = True
