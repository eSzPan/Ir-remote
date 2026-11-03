#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pilot IR do Pydroid 3
Korzysta z wbudowanej diody IR (ConsumerIrManager) przez pyjnius.
Wymaga: Kivy (zainstaluj przez Pip w Pydroid jeśli nie ma)
Telefon musi mieć blaster IR.
"""

import traceback
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# ====================== DANE Z CSV ======================
DEVICES = {
    "Grundig listwa": [
        {"label": "on/off", "code": "20DFC23D", "color": "Green"},
        {"label": "--------", "code": "20DF2AD5", "color": "Default"},
        {"label": "++++++", "code": "20DF1AE5", "color": "Default"},
        {"label": "żółty", "code": "20DFC43B", "color": "Yellow"},
        {"label": "czerwony", "code": "20DFE41B", "color": "Red"},
        {"label": "biały ciepły", "code": "20DF10EF", "color": "Default"},
        {"label": "tęcza 2", "code": "20DFE817", "color": "Default"},
        {"label": "fiolet", "code": "20DF9867", "color": "Default"},
        {"label": "c.żółty", "code": "20DF24DB", "color": "Default"},
        {"label": "pomarańczowy", "code": "20DFA45B", "color": "Default"},
        {"label": "zielony", "code": "20DFCC33", "color": "Default"},
        {"label": "żółto-zielony", "code": "20DF14EB", "color": "Default"},
        {"label": "j.niebieski", "code": "20DF4CB3", "color": "Default"},
        {"label": "niebieski 2", "code": "20DF6C93", "color": "Default"},
        {"label": "żywy zielony", "code": "20DFAC53", "color": "Default"},
        {"label": "tęcza auto", "code": "20DF42BD", "color": "Default"},
        {"label": "tęcza schowana", "code": "20DF12ED", "color": "Default"},
        {"label": "demo kolorów", "code": "20DF926D", "color": "Default"},
        {"label": "demo 2", "code": "20DF52AD", "color": "Default"},
        {"label": "j.zielona", "code": "20DF20DF", "color": "Default"},
        {"label": "j.rozowa", "code": "20DFA05F", "color": "Default"},
        {"label": "tęcza rosnaca", "code": "20DFE01F", "color": "Default"},
        {"label": "j.niebieski 2", "code": "20DF906F", "color": "Default"},
    ],
    "LG TV": [
        {"label": "ON / SETTINGS", "code": "20DFC23D", "color": "Default"},
        {"label": "żółty", "code": "20DF10EF", "color": "Yellow"},
        {"label": "niebieski", "code": "20DF906F", "color": "Blue"},
        {"label": "VOL+", "code": "20DF40BF", "color": "Default"},
        {"label": "VOL-", "code": "20DFC03F", "color": "Default"},
        {"label": "CH+", "code": "20DF00FF", "color": "Default"},
        {"label": "CH-", "code": "20DF807F", "color": "Default"},
        {"label": "Q.MENU", "code": "20DFA25D", "color": "Default"},
        {"label": "AV/SOURCE", "code": "20DFD02F", "color": "Default"},
        {"label": "-/--", "code": "20DFD52A", "color": "Default"},
        {"label": "0", "code": "20DF08F7", "color": "Default"},
        {"label": "1", "code": "20DF8877", "color": "Default"},
        {"label": "2", "code": "20DF48B7", "color": "Default"},
        {"label": "3", "code": "20DFC837", "color": "Default"},
        {"label": "4", "code": "20DF28D7", "color": "Default"},
        {"label": "5", "code": "20DFA857", "color": "Default"},
        {"label": "6", "code": "20DF6897", "color": "Default"},
        {"label": "7", "code": "20DFE817", "color": "Default"},
        {"label": "8", "code": "20DF18E7", "color": "Default"},
        {"label": "9", "code": "20DF9867", "color": "Default"},
        {"label": "OK", "code": "20DF22DD", "color": "Default"},
        {"label": "UP", "code": "20DF02FD", "color": "Default"},
        {"label": "DOWN", "code": "20DF827D", "color": "Default"},
        {"label": "LEFT", "code": "20DFE01F", "color": "Default"},
        {"label": "RIGHT", "code": "20DF609F", "color": "Default"},
        {"label": "BACK / RETURN", "code": "20DF14EB", "color": "Default"},
        {"label": "EXIT", "code": "20DFDA25", "color": "Default"},
        {"label": "INFO", "code": "20DF55AA", "color": "Default"},
        {"label": "GUIDE", "code": "20DFD52A", "color": "Default"},
        {"label": "FAV", "code": "20DF7887", "color": "Default"},
        {"label": "INPUT", "code": "20DFD02F", "color": "Default"},
        {"label": "LIST", "code": "20DFCA35", "color": "Default"},
        {"label": "Q.VIEW", "code": "20DF58A7", "color": "Default"},
        {"label": "RATIO", "code": "20DF9E61", "color": "Default"},
        {"label": "PLAY", "code": "20DF0DF2", "color": "Default"},
        {"label": "PAUSE", "code": "20DF06F9", "color": "Default"},
        {"label": "STOP", "code": "20DF8D72", "color": "Default"},
        {"label": "REW", "code": "20DFF10E", "color": "Default"},
        {"label": "FWD", "code": "20DF718E", "color": "Default"},
        {"label": "REC", "code": "20DFBD42", "color": "Red"},
        {"label": "RED", "code": "20DF4EB1", "color": "Red"},
        {"label": "GREEN", "code": "20DF8E71", "color": "Green"},
        {"label": "YELLOW", "code": "20DFC639", "color": "Yellow"},
        {"label": "BLUE", "code": "20DF8679", "color": "Blue"},
        {"label": "SUBTITLE", "code": "20DF9C63", "color": "Default"},
        {"label": "TEXT", "code": "20DF04FB", "color": "Default"},
        {"label": "TV/RAD", "code": "20DF0FF0", "color": "Default"},
        {"label": "AUDIO", "code": "20DF4AB5", "color": "Default"},
        {"label": "ENERGY SAVING", "code": "20DFA956", "color": "Default"},
        {"label": "SLEEP", "code": "20DF7E81", "color": "Default"},
        {"label": "ZOOM", "code": "20DFA25D", "color": "Default"},
        {"label": "PICT", "code": "20DFB24D", "color": "Default"},
    ],
    "LG (sz)": [
        {"label": "lg sz", "code": "10EFD02F", "color": "Green"},
    ],
}

COLOR_MAP = {
    "Red":    "#E53935",
    "Green":  "#43A047",
    "Yellow": "#FDD835",
    "Blue":   "#1E88E5",
    "Default": "#37474F",
}


# ====================== NEC → pattern (mikrosekundy) ======================
def nec_to_pattern(hex_code: str) -> list:
    """
    Konwertuje 32-bitowy kod NEC (np. '20DFC23D') na listę
    [ON, OFF, ON, OFF, ...] w mikrosekundach.
    Standard NEC: header 9ms/4.5ms, bit 560/560 (0) lub 560/1690 (1), LSB first.
    """
    code = int(hex_code, 16)
    pattern = [9000, 4500]  # header mark + space

    for i in range(32):
        bit = (code >> i) & 1
        pattern.append(560)                 # mark
        pattern.append(1690 if bit else 560)  # space

    pattern.append(560)  # trailing mark
    return pattern


# ====================== Transmisja przez wbudowaną diodę IR ======================
class IRTransmitter:
    def __init__(self):
        self.ir = None
        self.has_ir = False
        self.error_msg = ""
        self.frequency = 38000
        self._init()

    def _init(self):
        try:
            from jnius import autoclass

            # Pobierz Context z aktywności Kivy/Pydroid
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            activity = PythonActivity.mActivity

            # Wbudowany serwis Consumer IR (dioda IR telefonu)
            self.ir = activity.getSystemService(Context.CONSUMER_IR_SERVICE)

            if self.ir is None:
                self.error_msg = "Brak serwisu CONSUMER_IR_SERVICE"
                return

            if not self.ir.hasIrEmitter():
                self.error_msg = "Telefon nie ma wbudowanej diody IR"
                return

            # Sprawdź obsługiwane częstotliwości i wybierz ~38 kHz
            try:
                ranges = self.ir.getCarrierFrequencies()
                if ranges and len(ranges) > 0:
                    for r in ranges:
                        mn = r.getMinFrequency()
                        mx = r.getMaxFrequency()
                        if mn <= 38000 <= mx:
                            self.frequency = 38000
                            break
                        self.frequency = (mn + mx) // 2
            except Exception:
                self.frequency = 38000

            self.has_ir = True
            self.error_msg = ""

        except Exception as e:
            self.error_msg = f"Init IR: {type(e).__name__}: {e}"
            self.has_ir = False
            self.ir = None

    def transmit(self, hex_code: str) -> bool:
        """Wysyła kod NEC przez wbudowaną diodę IR."""
        if not self.has_ir or self.ir is None:
            return False
        try:
            pattern = nec_to_pattern(hex_code)

            # Najpewniejszy sposób w pyjnius: jawna konwersja na Java int[]
            from jnius import autoclass
            JArray = autoclass('java.lang.reflect.Array')
            Integer = autoclass('java.lang.Integer')
            
            # Tworzymy natywną tablicę Javy typu int
            jarr = JArray.newInstance(Integer.TYPE, len(pattern))
            for i, val in enumerate(pattern):
                JArray.setInt(jarr, i, val)
                
            self.ir.transmit(self.frequency, jarr)
            return True

        except Exception as e:
            self.error_msg = f"Transmit: {type(e).__name__}: {e}"
            print(self.error_msg)
            return False


# ====================== GUI ======================
class RemoteButton(Button):
    def __init__(self, cmd, transmitter, status_label, **kwargs):
        super().__init__(**kwargs)
        self.cmd = cmd
        self.transmitter = transmitter
        self.status_label = status_label
        self.text = cmd["label"]
        self.font_size = "15sp"
        self.size_hint_y = None
        self.height = "48dp"
        self.background_normal = ""
        self.background_color = get_color_from_hex(
            COLOR_MAP.get(cmd["color"], "#37474F")
        )
        # Czarny tekst na żółtym, biały na reszcie
        self.color = (0.1, 0.1, 0.1, 1) if cmd["color"] == "Yellow" else (1, 1, 1, 1)
        self.bind(on_press=self._send)

    def _send(self, instance):
        code = self.cmd["code"]
        ok = self.transmitter.transmit(code)
        if ok:
            self.status_label.text = f"✓ Wysłano: {self.cmd['label']}  ({code})"
            self.status_label.color = (0.2, 0.9, 0.3, 1)
        else:
            msg = self.transmitter.error_msg or "brak IR / błąd"
            self.status_label.text = f"✗ {msg}"
            self.status_label.color = (1, 0.3, 0.3, 1)

        # Krótki flash przycisku
        orig = list(self.background_color)
        self.background_color = (1, 1, 1, 0.55)
        Clock.schedule_once(lambda dt: setattr(self, "background_color", orig), 0.12)


class DeviceTab(BoxLayout):
    def __init__(self, name, commands, transmitter, status_label, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 6
        self.spacing = 4

        scroll = ScrollView(do_scroll_x=False, bar_width="6dp")
        grid = GridLayout(cols=2, spacing=6, size_hint_y=None, padding=4)
        grid.bind(minimum_height=grid.setter("height"))

        for cmd in commands:
            grid.add_widget(RemoteButton(cmd, transmitter, status_label))

        scroll.add_widget(grid)
        self.add_widget(scroll)


class PilotApp(App):
    def build(self):
        Window.clearcolor = (0.12, 0.12, 0.14, 1)
        root = BoxLayout(orientation="vertical", padding=4, spacing=4)

        self.status = Label(
            text="Inicjalizacja diody IR…",
            size_hint_y=None,
            height="36dp",
            font_size="14sp",
            color=(0.7, 0.7, 0.7, 1),
        )
        root.add_widget(self.status)

        self.tx = IRTransmitter()

        if self.tx.has_ir:
            self.status.text = f"✓ Dioda IR gotowa  ({self.tx.frequency} Hz)"
            self.status.color = (0.3, 0.9, 0.4, 1)
        else:
            self.status.text = f"⚠ {self.tx.error_msg or 'Brak diody IR'}"
            self.status.color = (1, 0.6, 0.2, 1)

        tabs = TabbedPanel(do_default_tab=False, tab_pos="top_mid")
        tabs.background_color = (0.15, 0.15, 0.17, 1)

        for name, cmds in DEVICES.items():
            item = TabbedPanelItem(text=name)
            item.add_widget(DeviceTab(name, cmds, self.tx, self.status))
            tabs.add_widget(item)

        root.add_widget(tabs)

        info = Label(
            text="Pydroid 3 · wbudowana dioda IR · NEC 38 kHz",
            size_hint_y=None,
            height="28dp",
            font_size="12sp",
            color=(0.5, 0.5, 0.5, 1),
        )
        root.add_widget(info)
        return root


if __name__ == "__main__":
    # Blok try-except zapobiega cichemu zamykaniu programu przy błędach Kivy
    try:
        PilotApp().run()
    except Exception as e:
        print("\n--- KRYTYCZNY BŁĄD APLIKACJI ---")
        traceback.print_exc()
