from collections.abc import Callable
from functools import partial, wraps
from typing import Any

from dearpygui import dearpygui as dpg
from keyboard import add_hotkey

from trainerbase.codeinjection import AbstractCodeInjection
from trainerbase.common import Teleport
from trainerbase.gameobject import (
    GameBool,
    GameByte,
    GameDouble,
    GameFloat,
    GameInt,
    GameLongLong,
    GameObject,
    GameShort,
    GameUnsignedInt,
    GameUnsignedLongLong,
    GameUnsignedShort,
)
from trainerbase.scriptengine import Script
from trainerbase.tts import say


TAG_TELEPORT_LABELS = "__teleport_labels"


def simple_trainerbase_menu(window_title: str, width: int, height: int):
    def menu_decorator(initializer: Callable):
        @wraps(initializer)
        def run_menu_wrapper(on_initialized: Callable):
            dpg.create_context()
            dpg.create_viewport(
                title=window_title,
                min_width=width,
                min_height=height,
                width=width,
                height=height,
            )
            dpg.setup_dearpygui()

            with dpg.window(
                label=window_title,
                tag="menu",
                min_size=[width, height],
                no_close=True,
                no_move=True,
                no_title_bar=True,
                horizontal_scrollbar=True,
            ):
                initializer()

            dpg.show_viewport()

            on_initialized()

            dpg.start_dearpygui()
            dpg.destroy_context()

        return run_menu_wrapper

    return menu_decorator


def add_script_to_gui(
    script: Script,
    label: str,
    hotkey: str | None = None,
    tts_on_hotkey: bool = True,
):
    def on_script_state_change():
        script.enabled = dpg.get_value(script.dpg_tag)

    if hotkey is not None:
        pure_label = label

        def on_hotkey_press():
            dpg.set_value(script.dpg_tag, not dpg.get_value(script.dpg_tag))
            on_script_state_change()
            if tts_on_hotkey:
                status = "enabled" if script.enabled else "disabled"
                say(f"Script {pure_label} {status}")

        add_hotkey(hotkey, on_hotkey_press)

        label = f"[{hotkey}] {label}"

    dpg.add_checkbox(label=label, tag=script.dpg_tag, callback=on_script_state_change, default_value=script.enabled)


def add_gameobject_to_gui(
    gameobject: GameObject,
    label: str,
    hotkey: str | None = None,
    default_setter_input_value: Any = 0,
    before_set: Callable = int,
    tts_on_hotkey: bool = True,
):
    def on_frozen_state_change():
        gameobject.frozen = gameobject.value if dpg.get_value(gameobject.dpg_tag_frozen) else None

    def on_value_set():
        new_value = before_set(dpg.get_value(gameobject.dpg_tag_setter))

        if gameobject.frozen is None:
            gameobject.value = new_value
        else:
            gameobject.frozen = new_value

    if hotkey is not None:
        pure_label = label

        def on_hotkey_press():
            dpg.set_value(gameobject.dpg_tag_frozen, not dpg.get_value(gameobject.dpg_tag_frozen))
            on_frozen_state_change()
            if tts_on_hotkey:
                status = "released" if gameobject.frozen is None else "frozen"
                say(f"GameObject {pure_label} {status}")

        add_hotkey(hotkey, on_hotkey_press)

        label = f"[{hotkey}] {label}"

    match gameobject:
        case GameFloat():
            add_setter_input = dpg.add_input_float
        case GameDouble():
            add_setter_input = dpg.add_input_double
        case GameByte() | GameShort() | GameInt() | GameLongLong() | GameBool():
            add_setter_input = dpg.add_input_int
        case GameUnsignedShort() | GameUnsignedInt() | GameUnsignedLongLong():
            add_setter_input = partial(dpg.add_input_int, min_clamped=True, min_value=0)
        case _:
            add_setter_input = dpg.add_input_text

    with dpg.group(horizontal=True):
        dpg.add_checkbox(tag=gameobject.dpg_tag_frozen, callback=on_frozen_state_change)
        dpg.add_text(label)
        dpg.add_input_text(width=220, tag=gameobject.dpg_tag_getter, readonly=True)
        add_setter_input(width=220, tag=gameobject.dpg_tag_setter, default_value=default_setter_input_value)
        dpg.add_button(label="Set", callback=on_value_set)


def add_codeinjection_to_gui(
    injection: AbstractCodeInjection,
    label: str,
    hotkey: str | None = None,
    tts_on_hotkey: bool = True,
):
    def on_codeinjection_state_change():
        if dpg.get_value(injection.dpg_tag):
            injection.inject()
        else:
            injection.eject()

    if hotkey is not None:
        pure_label = label

        def on_hotkey_press():
            dpg.set_value(injection.dpg_tag, not dpg.get_value(injection.dpg_tag))
            on_codeinjection_state_change()
            if tts_on_hotkey:
                status = "applied" if dpg.get_value(injection.dpg_tag) else "removed"
                say(f"CodeInjection {pure_label} {status}")

        add_hotkey(hotkey, on_hotkey_press)

        label = f"[{hotkey}] {label}"

    dpg.add_checkbox(label=label, tag=injection.dpg_tag, callback=on_codeinjection_state_change)


def add_teleport_to_gui(
    tp: Teleport,
    hotkey_save_position: str | None = None,
    hotkey_set_saved_position: str | None = None,
    hotkey_dash: str | None = None,
    tts_on_hotkey: bool = True,
):
    _tp_add_save_set_position_hotkeys_if_needed(tp, hotkey_save_position, hotkey_set_saved_position, tts_on_hotkey)
    _tp_add_dash_hotkeys_if_needed(tp, hotkey_dash, tts_on_hotkey)

    add_gameobject_to_gui(tp.player_x, "X")
    add_gameobject_to_gui(tp.player_y, "Y")
    add_gameobject_to_gui(tp.player_z, "Z")

    _tp_add_labels_if_needed(tp)

    def on_clip_coords():
        dpg.set_clipboard_text(repr(tp.get_coords()))

    dpg.add_button(label="Clip Coords", callback=on_clip_coords)


def _tp_add_save_set_position_hotkeys_if_needed(
    tp: Teleport,
    hotkey_save_position: str | None,
    hotkey_set_saved_position: str | None,
    tts_on_hotkey: bool,
):
    if hotkey_save_position is None or hotkey_set_saved_position is None:
        return

    def on_hotkey_save_position_press():
        tp.save_position()
        if tts_on_hotkey:
            say("Position saved")

    def on_hotkey_set_saved_position_press():
        is_position_restored = tp.restore_saved_position()

        if tts_on_hotkey:
            say("Position restored" if is_position_restored else "Save position at first")

    add_hotkey(hotkey_save_position, on_hotkey_save_position_press)
    add_hotkey(hotkey_set_saved_position, on_hotkey_set_saved_position_press)

    dpg.add_text(f"[{hotkey_save_position}] Save Position")
    dpg.add_text(f"[{hotkey_set_saved_position}] Set Saved Position")


def _tp_add_dash_hotkeys_if_needed(tp, hotkey_dash: str | None, tts_on_hotkey: bool):
    if tp.movement_vector_updater_script is None or hotkey_dash is None:
        return

    def on_hotkey_dash_press():
        tp.dash()
        if tts_on_hotkey:
            say("Dash!")

    add_hotkey(hotkey_dash, on_hotkey_dash_press)

    dpg.add_text(f"[{hotkey_dash}] Dash")


def _tp_add_labels_if_needed(tp: Teleport):
    if not tp.labels:
        return

    def on_goto_label():
        tp.goto(dpg.get_value(TAG_TELEPORT_LABELS))

    labels = sorted(tp.labels.keys())

    with dpg.group(horizontal=True):
        dpg.add_button(label="Go To", callback=on_goto_label)
        dpg.add_combo(label="Labels", tag=TAG_TELEPORT_LABELS, items=labels, default_value=labels[0])
