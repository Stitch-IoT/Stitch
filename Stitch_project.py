import threading
import time
import kivy.core.window
import plyer
import speech_recognition as sr
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineRightIconListItem
from speech_recognition import WaitTimeoutError
from kv_helpers import kv
from text_to_speach import text_to_speech

kivy.core.window.Window.size = (360, 600)

from kivy.uix.image import Image


class LoadingScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.image = Image(source='lod.gif')  # Замість 'your_loading_gif.gif' використайте шлях до вашого GIF файлу
        self.add_widget(self.image)


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


class LoadingScreen(MDBoxLayout):
    pass


def update_ui(detection_label, audio_to_text_button, result_text):
    detection_label.text = result_text

    audio_to_text_button.icon = "play"
    audio_to_text_button.icon_color = (1, 1, 1, 1)
    audio_to_text_button.text = "Почати"
    audio_to_text_button.text_color = (1, 1, 1, 1)
    audio_to_text_button.md_bg_color = (0, 0, 0, 1)
    # Re-enable the button after recognition is done
    # audio_to_text_button.disabled = False


class Main(MDApp):
    DEBUG = False
    RAISE_ERROR = True
    AUTO_RELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word_section_content = None
        self.names_list = []
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.thread = None

    def build(self):
        self.title = "SoundTouch"
        Clock.schedule_interval(self.update_progress_bar, 0.1)
        return Builder.load_string(kv)

    def show_loading_screen(self):
        self.loading_screen = LoadingScreen()
        self.root.add_widget(self.loading_screen)
        self.start_time = time.time()  # Record the start time

    def hide_loading_screen(self):
        self.root.remove_widget(self.loading_screen)
        self.stop_time = time.time()  # Record the stop time

    def update_progress_bar(self, dt):
        if hasattr(self, 'start_time') and hasattr(self, 'stop_time'):
            elapsed_time = self.stop_time - self.start_time
            if elapsed_time < 5:  # Adjust the duration as needed
                progress = elapsed_time / 5  # Adjust the total duration as needed
                self.loading_screen.ids.progress_bar.value = progress * 100
            else:
                # Loading is complete, hide the loading screen
                self.hide_loading_screen()

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

    def stop_listening(self):
        self.is_listening = False
        if (
                hasattr(self, "thread")
                and self.thread is not None
                and self.thread.is_alive()
        ):
            self.thread.join()

    def listen_for_command(self):
        while self.is_listening:
            print("Listening started")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = self.recognizer.listen(source, timeout=4)
                except WaitTimeoutError:
                    continue

            try:
                command = self.recognizer.recognize_google(audio, language="uk-UA")
                Clock.schedule_once(
                    lambda dt: toast(f"Отримано команду: {command}", duration=3), 0
                )

                if any(name in command for name in self.names_list):
                    print("if any(name in command for name in self.names_list):")
                    Clock.schedule_once(
                        lambda dt: plyer.notification.notify(
                            title="Розпізнано слово", message=command
                        ),
                        0,
                    )
                else:
                    continue

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass

            time.sleep(0.3)
            print("Listening stopped.")

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
            # audio_to_text_button.disabled = True
            audio_to_text_button.icon = "square"
            audio_to_text_button.icon_color = (0, 0, 0, 1)
            audio_to_text_button.text = "Слухаю..."
            audio_to_text_button.text_color = (0, 0, 0, 1)
            audio_to_text_button.md_bg_color = (1, 1, 1, 1)

            threading.Thread(target=self.recognize_speech, args=(detection_label, audio_to_text_button)).start()
        else:
            audio_to_text_button.icon = "play"
            audio_to_text_button.icon_color = (1, 1, 1, 1)
            audio_to_text_button.text = "Почати"
            audio_to_text_button.text_color = (1, 1, 1, 1)
            audio_to_text_button.md_bg_color = (0, 0, 0, 1)
            # audio_to_text_button.disabled = False

    def recognize_speech(self, detection_label, audio_to_text_button):
        import speech_recognition as sr
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="uk-UA", show_all=False)
            print("You said:", text)
            # Limiting to 260 characters
            if len(text) > 260:
                text = text[:260] + "..."
            result_text = text if text else "ніхуя не ясно"
        except sr.UnknownValueError:
            result_text = "ніхуя не ясно"
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            result_text = "Could not request results"

        # Update UI elements on the main thread
        Clock.schedule_once(lambda dt: update_ui(detection_label, audio_to_text_button, result_text), 0)

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

            file = text_to_speech(translation_text)
            toast("saying...", duration=4)
            self.play_audio(file)

            if text_to_audio_button.icon == "play":
                text_to_audio_button.icon = "square"
                text_to_audio_button.icon_color = (0, 0, 0, 1)
                text_to_audio_button.text = "Відтворюється..."
                text_to_audio_button.text_color = (0, 0, 0, 1)
                text_to_audio_button.md_bg_color = (1, 1, 1, 1)
                text_to_audio_button.disabled = True  # Блокуємо кнопку

            else:
                self.reset_button()

    def reset_button(self):
        text_to_audio_button = self.root.ids.text_to_audio_button
        text_to_audio_button.icon = "play"
        text_to_audio_button.text = "Відтворити"
        text_to_audio_button.icon_color = (1, 1, 1, 1)
        text_to_audio_button.text_color = (1, 1, 1, 1)
        text_to_audio_button.md_bg_color = (0, 0, 0, 1)
        text_to_audio_button.disabled = False  # Розблоковуємо кнопку

    def play_audio(self, filename):
        sound = SoundLoader.load(filename)
        if sound:
            sound.bind(on_stop=self.on_audio_complete)
            sound.play()

    def on_audio_complete(self, sound):
        self.reset_button()
        # toast("тут можна якись текст бахнути", duration=2)

    def clear_text_field(self):
        translation_input = self.root.ids.translation_input
        text_to_audio_button = self.root.ids.text_to_audio_button

        if len(translation_input.text) < 1:
            toast("Поле порожнє", duration=2)

        else:
            text_to_audio_button.disabled = True

            translation_input.text = ""
            self.reset_button()
            text_to_audio_button.disabled = False

            text_to_audio_button.icon = "play"
            text_to_audio_button.text = "Відтворити"
            text_to_audio_button.icon_color = 1, 1, 1, 1
            text_to_audio_button.text_color = 1, 1, 1, 1
            text_to_audio_button.md_bg_color = 0, 0, 0, 1

    def added_name(self, item):
        pass

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
