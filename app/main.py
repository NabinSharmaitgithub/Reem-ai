from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import orchestrator
import voice

class ReemMobileApp(App):
    def build(self):
        self.title = "Reem AI - Mobile Operator"

        # Root layout
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Safety Warning
        warning_box = BoxLayout(size_hint_y=None, height=50, padding=5)
        warning_label = Label(
            text="[color=ff0000]⚠ SAFETY: Controls device gestures. Use on trusted systems.[/color]",
            markup=True,
            halign='center',
            valign='middle'
        )
        warning_box.add_widget(warning_label)
        root.add_widget(warning_box)

        # Title
        root.add_widget(Label(text="Reem AI", font_size='32sp', size_hint_y=None, height=60))

        # Command Input
        self.command_input = TextInput(
            hint_text="What can I do for you?",
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        self.command_input.bind(on_text_validate=self.on_send)
        root.add_widget(self.command_input)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)

        send_btn = Button(text="Send", background_color=(0.3, 0.7, 0.3, 1))
        send_btn.bind(on_press=self.on_send)
        btn_layout.add_widget(send_btn)

        voice_btn = Button(text="🎤 Voice")
        voice_btn.bind(on_press=self.on_voice)
        btn_layout.add_widget(voice_btn)

        root.add_widget(btn_layout)

        # Status
        self.status_label = Label(
            text="Status: Ready",
            size_hint_y=None,
            height=40,
            halign='left',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        root.add_widget(self.status_label)

        return root

    def set_status(self, text):
        self.status_label.text = f"Status: {text}"

    def on_send(self, instance=None):
        cmd = self.command_input.text.strip()
        if cmd:
            self.command_input.text = ""
            self.set_status("Processing...")
            threading.Thread(target=self.run_command, args=(cmd,), daemon=True).start()

    def run_command(self, cmd):
        try:
            orchestrator.process(cmd)
            Clock.schedule_once(lambda dt: self.set_status("Ready"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.set_status(f"Error: {str(e)}"))

    def on_voice(self, instance):
        self.set_status("Listening...")
        threading.Thread(target=self.run_voice, daemon=True).start()

    def run_voice(self):
        text = voice.listen()
        if text and not text.startswith("Error"):
            Clock.schedule_once(lambda dt: setattr(self.command_input, 'text', text))
            Clock.schedule_once(lambda dt: self.set_status("Voice recognized"))
        else:
            Clock.schedule_once(lambda dt: self.set_status(text if text else "Could not hear anything"))

if __name__ == "__main__":
    ReemMobileApp().run()
