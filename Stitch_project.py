import kivy.core.window
from kaki.app import App
import time
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import MDList, OneLineListItem, OneLineRightIconListItem
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.core.audio import SoundLoader
import speech_recognition as sr
import plyer
import threading
from kivy.clock import Clock
from kv_helpers import kv
from text_to_speach import text_to_speach
import time
from speech_recognition import WaitTimeoutError
from watchdog.observers import Observer


kivy.core.window.Window.size = (360, 600)


class ScreenOne(MDBoxLayout):
    pass


class Content(MDFloatLayout):
    pass


class WordSectionContent(MDBoxLayout):
    pass


class SoundSectionContent(MDBoxLayout):
    pass


class SettingsSectionContent(MDBoxLayout):
    pass


class Main(MDApp):
    DEBUG = False
    RAISE_ERROR = True
    AUTO_RELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.names_list = []
        self.is_listening = False
        self.recognizer = sr.Recognizer()

    def build(self):
        self.title = "SoundTouch"
        return Builder.load_string(kv)

    def add_name(self):
        close_button = MDFlatButton(text="Закрити", on_release=self.close_dialog)
        save_button = MDFlatButton(text="Зберегети", on_release=self.save_name)
        self.dialog = MDDialog(
            title="Запишіть ім'я чи фразу",
            type="custom",
            content_cls=Content(),
            buttons=[close_button, save_button],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def save_name(self, obj):
        new_item_text = self.dialog.content_cls.ids.text_input.text
        if len(new_item_text) < 1:
            toast("Поле порожнє", duration=2)
        else:
            new_list_item = OneLineRightIconListItem(text=new_item_text)

            delete_name_button = MDIconButton(
                icon="delete",
                on_release=lambda x, item=new_list_item: self.delete_name(item),
            )
            delete_name_button.pos_hint = {"center_x": 0.9, "center_y": 0.5}
            new_list_item.add_widget(delete_name_button)
            self.names_list.append(new_item_text)
            list_container = self.word_section_content.ids.list_of_names
            list_container.add_widget(new_list_item)
            toast("Фраза збережена", duration=2)

            self.dialog.dismiss()

    def delete_name(self, list_item):
        cancel_deleting_button = MDFlatButton(
            text="Скасувати", on_release=self.cancel_deleting
        )
        admit_deleting_button = MDFlatButton(
            text="Підтвердити",
            on_release=lambda x, item=list_item: self.admit_deleting(item),
        )
        self.dialog = MDDialog(
            title="Видалити?", buttons=[cancel_deleting_button, admit_deleting_button]
        )
        self.dialog.open()

    def admit_deleting(self, list_item):
        list_container = self.word_section_content.ids.list_of_names
        list_container.remove_widget(list_item)
        self.dialog.dismiss()
        self.names_list.remove(list_item.text)
        toast("Об'єкт видалено", duration=2)

    def cancel_deleting(self, obj):
        self.dialog.dismiss()

    def start_listening_thread(self):
        self.is_listening = True
        if self.is_listening:
            self.thread = threading.Thread(target=self.listen_for_command)
            self.thread.start()
            print("Start")

    def stop_listening(self):
        self.is_listening = False
        print("Stop")

    def listen_for_command(self):
        def callback(recognizer, audio):
            try:
                if not self.is_listening:
                    return  # Exit the callback if not listening anymore
                    
                command = recognizer.recognize_google(audio, language="uk-UA")
                Clock.schedule_once(
                    lambda dt: toast(f"Отримано команду: {command}", duration=3), 0
                )

                if any(name in command for name in self.names_list):
                    Clock.schedule_once(
                        lambda dt: plyer.notification.notify(
                            title="Розпізнано слово", message=command
                        ),
                        0,
                    )
                else:
                    return

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass

        # Create and enter the audio source into a context manager only once
        source = sr.Microphone()
        with source as mic:
            self.recognizer.adjust_for_ambient_noise(mic)

        # Start listening in the background with the adjusted audio source
        recognizer_thread = self.recognizer.listen_in_background(source, callback)

    def general_detection(self):
        detecting_label = self.root.ids.detecting_label
        detecting_button = self.root.ids.detecting_button

        if detecting_button.icon == "play":
            detecting_label.text = "Розпізнавання..."
            self.start_listening_thread()
            detecting_label.pos_hint = {"center_x": 0.6, "center_y": 0.6}
            detecting_button.icon = "square"
        else:
            detecting_label.text = "Почати розпізнавання"
            self.stop_listening()
            detecting_label.pos_hint = {"center_x": 0.5, "center_y": 0.6}
            detecting_button.icon = "play"

    def start_audio_to_text(self):
        detection_label = self.root.ids.result_from_audio
        audio_to_text_button = self.root.ids.audio_to_text_button

        if audio_to_text_button.icon == "play":
            audio_to_text_button.icon = "square"
            audio_to_text_button.icon_color = 0, 0, 0, 1
            audio_to_text_button.text = "Слухаю..."
            audio_to_text_button.text_color = 0, 0, 0, 1
            audio_to_text_button.md_bg_color = 1, 1, 1, 1
            recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(
                    audio, language="uk-UA", show_all=False
                )
                print("You said:", text)
                # Limiting to 120 characters
                if len(text) > 260:
                    text = text[:260] + "..."
                detection_label.text = text if text else "ніхуя не ясно"
            except sr.UnknownValueError:
                detection_label.text = "ніхуя не ясно"
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
                detection_label.text = "Could not request results"
            finally:
                audio_to_text_button.icon = "play"
                audio_to_text_button.text = "Почати"
                audio_to_text_button.icon_color = 1, 1, 1, 1
                audio_to_text_button.text_color = 1, 1, 1, 1
                audio_to_text_button.md_bg_color = 0, 0, 0, 1

        else:
            audio_to_text_button.icon = "square"
            audio_to_text_button.icon_color = 0, 0, 0, 1
            audio_to_text_button.text = "Слухаю..."
            audio_to_text_button.text_color = 0, 0, 0, 1
            audio_to_text_button.md_bg_color = 1, 1, 1, 1

    def change_detection_label(self, dt):
        detection_label = self.root.ids.result_from_audio
        audio_to_text_button = self.root.ids.audio_to_text_button

        detection_label = self.root.ids.result_from_audio
        detection_label.text = "Це приклад роботи нашої програми"
        audio_to_text_button.icon = "play"
        audio_to_text_button.text = "Почати"
        audio_to_text_button.icon_color = 1, 1, 1, 1
        audio_to_text_button.text_color = 1, 1, 1, 1
        audio_to_text_button.md_bg_color = 0, 0, 0, 1

    def start_text_to_audio(self):
        translation_text = self.root.ids.translation_input.text
        text_to_audio_button = self.root.ids.text_to_audio_button

        if len(translation_text) < 1:
            toast("Поле порожнє", duration=2)
        else:
            new_list_item = OneLineRightIconListItem(text=translation_text)
            tranlate_button = MDIconButton(
                on_release=lambda x, item=new_list_item: self.added_name(item)
            )
            tranlate_button.pos_hint = {"center_x": 0.9, "center_y": 0.5}
            new_list_item.add_widget(tranlate_button)

            file = text_to_speach(translation_text)  # Capture the returned filename
            toast("saying...", duration=4)
            self.play_audio(file)

            if text_to_audio_button.icon == "play":
                text_to_audio_button.icon = "square"
                text_to_audio_button.icon_color = 0, 0, 0, 1
                text_to_audio_button.text = "Відтворюється..."

                text_to_audio_button.text_color = 0, 0, 0, 1
                text_to_audio_button.md_bg_color = 1, 1, 1, 1

            else:
                text_to_audio_button.icon = "play"
                text_to_audio_button.text = "Відтворити"
                text_to_audio_button.icon_color = 1, 1, 1, 1
                text_to_audio_button.text_color = 1, 1, 1, 1
                text_to_audio_button.md_bg_color = 0, 0, 0, 1

    def clear_text_field(self):
        translation_input = self.root.ids.translation_input
        text_to_audio_button = self.root.ids.text_to_audio_button

        if len(translation_input.text) < 1:
            toast("Поле порожнє", duration=2)

        else:
            translation_input.text = ""

            text_to_audio_button.icon = "play"
            text_to_audio_button.text = "Відтворити"
            text_to_audio_button.icon_color = 1, 1, 1, 1
            text_to_audio_button.text_color = 1, 1, 1, 1
            text_to_audio_button.md_bg_color = 0, 0, 0, 1

    def added_name(self, item):
        pass

    def play_audio(self, filename):
        sound = SoundLoader.load(filename)
        if sound:
            sound.play()

    def word_section(self):
        self.remove_home_screen_content()
        self.word_section_content = WordSectionContent()
        self.root.ids.home_screen.add_widget(self.word_section_content)


    def sound_section(self):
        self.remove_home_screen_content()
        sound_section_content = SoundSectionContent()
        self.root.ids.home_screen.add_widget(sound_section_content)

    def settings_section(self):
        self.remove_home_screen_content()
        settings_section_content = SettingsSectionContent()
        self.root.ids.home_screen.add_widget(settings_section_content)

    def remove_home_screen_content(self):
        home_screen = self.root.ids.home_screen
        home_screen.clear_widgets()

    def back_to_home_screen(self):
        self.remove_word_section()
        self.remove_sound_section()
        self.remove_settings_section()
        home_screen = self.root.ids.home_screen
        home_screen.add_widget(ScreenOne())

    def remove_word_section(self):
        home_screen = self.root.ids.home_screen
        for child in home_screen.children[:]:
            if isinstance(child, WordSectionContent):
                home_screen.remove_widget(child)
                break

    def remove_sound_section(self):
        home_screen = self.root.ids.home_screen
        for child in home_screen.children[:]:
            if isinstance(child, SoundSectionContent):
                home_screen.remove_widget(child)
                break

    def remove_settings_section(self):
        home_screen = self.root.ids.home_screen
        for child in home_screen.children[:]:
            if isinstance(child, SettingsSectionContent):
                home_screen.remove_widget(child)
                break


if __name__ == "__main__":
    Main().run()
