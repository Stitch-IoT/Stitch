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
import speech_recognition as sr
import plyer
import threading
from kivy.clock import Clock
from watchdog.observers import Observer
from kv_helpers import kv    
kivy.core.window.Window.size = (360, 600)


class ScreenOne(MDFloatLayout):
    pass


class YourContainer(MDBoxLayout):
    pass


class Content(MDFloatLayout):
    pass


class WordSectionContent(MDBoxLayout):
    pass


class SoundSectionContent(MDBoxLayout):
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
            list_container = WordSectionContent().ids.list_of_names
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
        list_container = self.root.ids.list_of_names
        list_container.remove_widget(list_item)
        self.dialog.dismiss()
        self.names_list.remove(list_item.text)
        toast("Об'єкт видалено", duration=2)

    def cancel_deleting(self, obj):
        self.dialog.dismiss()

    def start_listening_thread(self):
        self.is_listening = True
        threading.Thread(target=self.listen_for_command).start()

    def listen_for_command(self):

        recognizer = sr.Recognizer()

        if not self.listen_for_command:
            return

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Recognize the speech using Google Speech Recognition with Ukrainian language
            command = recognizer.recognize_google(audio, language="uk-UA")
            Clock.schedule_once(
                lambda dt: toast(f"Отримано команду: {command}", duration=3), 0
            )

            # Check if any trigger word is present in the command
            if any(self.names_list in command):
                Clock.schedule_once(
                    lambda dt: plyer.notification.notify(
                        title="Розпізнано слово", message=command
                    ),
                    0,
                )

            else:
                print("Команда не визначена.")

        except sr.UnknownValueError:
            pass
        # Clock.schedule_once(lambda dt: toast("Розпізнавання мови не вдалося.", duration=3), 0)
        except sr.RequestError as e:
            pass
        # Clock.schedule_once(lambda dt: toast(f"Не вдалося отримати результати від служби Google Speech Recognition; {e}", duration=3), 0)

        while True:
            if self.root.ids.detecting_button.icon == "play":
                break

    def general_detection(self):
        detecting_label = self.root.ids.detecting_label
        detecting_button = self.root.ids.detecting_button

        if detecting_button.icon == "play":
            detecting_label.text = "Розпізнавання..."
            self.listen_for_command = True
            detecting_label.pos_hint = {"center_x": 0.6, "center_y": 0.6}
            detecting_button.icon = "square"
        else:
            detecting_label.text = "Почати розпізнавання"
            self.listen_for_command = False
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

        else:
            audio_to_text_button.icon = "play"
            audio_to_text_button.text = "Почати"
            audio_to_text_button.icon_color = 1, 1, 1, 1
            audio_to_text_button.text_color = 1, 1, 1, 1
            audio_to_text_button.md_bg_color = 0, 0, 0, 1

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

    def word_section(self):
        self.remove_home_screen_content()
        word_section_content = WordSectionContent()
        self.root.ids.home_screen.add_widget(word_section_content)

    def sound_section(self):
        self.remove_home_screen_content()
        sound_section_content = SoundSectionContent()
        self.root.ids.home_screen.add_widget(sound_section_content)

    def remove_home_screen_content(self):
        home_screen = self.root.ids.home_screen
        home_screen.clear_widgets()

    def back_to_home_screen(self):
        self.remove_word_section()
        self.remove_sound_section()
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


if __name__ == "__main__":
    Main().run()