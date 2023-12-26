import kivy.core.window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import MDList, OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.bottomnavigation import MDBottomNavigationItem



kivy.core.window.Window.size = (360, 600)

kv = """

<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
    	id : text_input
        line_color_normal: "black"
        pos_hint : {"center_x":.5, "center_y":.5}
        


MDFloatLayout:
	MDBottomNavigation:
		text_color_normal: 0, 0, 0, 1
		text_color_active: 57/255, 93/255, 203/255, 1
		spacing : 90
		id : bottom_nav
    	MDBottomNavigationItem:
	        icon : 'home'
	        id : home_screen
			name : "home"
			MDScrollView:
				MDList:
					id : list_of_names
					spacing : 0
					pos_hint : {"center_y": .9}
					padding : 0
	
						
							

			MDBoxLayout:
				pos_hint : {"center_x": .5, "center_y": .05}
				adaptive_size:True
				MDIconButton:
					id : plus
					icon : "plus"
					icon_size : 45
					adaptive_size:True
					on_press:
						app.add_name()

		MDBottomNavigationItem:
		    icon : 'play-circle'
			id : screen2
			name : "play"
			MDFloatLayout:
				MDLabel:
					id : detecting_label
					adaptive_size: True
					text : "Start detecting"
					pos_hint : {"center_x":.5, "center_y":.6}
					font_size : "28dp"
				MDIconButton:
					id: detecting_button
					icon : "play"
					icon_size: "60sp"
					adaptive_size: True
					pos_hint : {"center_x":.5, "center_y":.4}
					on_press: 
						detecting_button.icon = 'pause' if detecting_button.icon == 'play' else 'play'
						detecting_label.text = 'Stop detecting' if detecting_label.text == 'Start detecting' else 'Start detecting'


		MDBottomNavigationItem:
	        icon : 'account-voice'
			id : screen3
			name : "translation"
			
			MDRectangleFlatIconButton:
				text : 'plus'
				icon : 'play'
			MDFlatButton:
				text : 'minus'

			

"""


class Content(MDFloatLayout):
	pass


class Main(MDApp):
	current_icon = "play"

	def build(self):
		return Builder.load_string(kv)
 
      
	def add_name(self):
		close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
		save_button = MDFlatButton(text='Save', on_release=self.save_name)
		self.dialog = MDDialog(title='Write a name or a phrase', type="custom", content_cls=Content(),
                               buttons=[close_button, save_button])
		self.dialog.open()

	def close_dialog(self, obj):
		self.dialog.dismiss()

	def save_name(self, obj):
	    new_item_text = self.dialog.content_cls.ids.text_input.text
	    new_list_item = OneLineAvatarIconListItem(text=new_item_text)

	    # edit_button = MDIconButton(icon="pencil", on_release=self.edit_name)
	    delete_name_button = MDIconButton(icon="delete", on_release=self.delete_name)
	    new_list_item.add_widget(delete_name_button)

	    list_container = self.root.ids.list_of_names
	    list_container.add_widget(new_list_item)

	    toast("Name saved", duration=3)
	    self.dialog.dismiss()


	
	def delete_name(self, list_item):
	    cancel_deleting_button = MDFlatButton(text='Cancel', on_release=self.cancel_deleting)
	    admit_deleting_button = MDFlatButton(text='Admit', on_release=lambda x, item=list_item: self.admit_deleting(x, item))
	    self.dialog = MDDialog(title='Delete the name?',
	                           buttons=[cancel_deleting_button, admit_deleting_button])
	    self.dialog.open()		


	def cancel_deleting(self, obj):
		self.dialog.dismiss()

	def admit_deleting(self, obj, list_item):
	    list_container = self.root.ids.list_of_names
	    list_container.remove_widget(list_item)
	    self.dialog.dismiss()
	    toast("Name deleted", duration=3)



class YourContainer(IRightBodyTouch, MDBoxLayout):
    pass


# adaptive_width = True
# edit_button = MDIconButton(icon='pencil', on_release=close_dialog)
# delete_button = MDIconButton(icon='delete', on_release = app.delete_name)


if __name__ == "__main__":
    Main().run()