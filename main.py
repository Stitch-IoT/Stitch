from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.toast.kivytoast.kivytoast import toast


Window.size = (360, 600)

kv = """

<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        hint_text: "here"
        line_color_normal: "black"
        pos_hint : {"center_x":.5, "center_y":.5}


MDFloatLayout:

	MDBottomNavigation:
    	MDBottomNavigationItem:

	        icon : 'home'
	        id : screen1
			name : "home"

			MDScrollView:
				bar_width:0

				MDList:
					OneLineAvatarIconListItem:
						text: "Name"
						on_size:
					    	self.ids._right_container.width = container.width
					    	self.ids._right_container.x = container.width

						

						YourContainer:
							adaptive_width : True
					    	id: container

					    	MDIconButton:
					        	icon: "pencil"
					

					    	MDIconButton:
					        	icon: "delete"
					        	on_press :
					        		app.delete_name()

			MDBoxLayout:
				adaptive_size:True
				pos_hint : {"center_x": .5, "center_y": .1}
				MDIconButton:
					icon_width: root.width*0.4
					id : plus
					icon : "plus"
					icon_size : 45
					adaptive_size:True
					on_press:
						app.add_sound()


	    MDBottomNavigationItem:
	        icon : 'information'
	        MDScreen:
				id : screen2
				name : "settings"

	



"""
class Content(MDFloatLayout):
    pass


class Main(MDApp):

	def build(self):
		return Builder.load_string(kv)

	def add_sound(self):
		add_name_button = MDIconButton(icon = "account", pos_hint= {'center_x': .5, 'center_y': .5})
		add_alarm_button = MDIconButton(icon = "alarm-light")
		self.dialog = MDDialog(buttons=[add_name_button, add_alarm_button])
		self.dialog.open()

	def add_name(self):
		close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
		save_button = MDFlatButton(text='Save', on_release=self.save_name)
		self.dialog = MDDialog(title='Write the name',type="custom",content_cls=Content(),
	                               buttons=[close_button, save_button])
		self.dialog.open()

	def close_dialog(self,obj):
		self.dialog.dismiss()

	def save_name(self,obj):
		self.dialog.dismiss()
		toast("Name saved", duration = 3)

		

	def delete_name(self):
		cancel_button = MDFlatButton(text='Cancel', on_release=self.deleting_cancel_button)
		admit_button = MDFlatButton(text='Admit', on_release=self.deleting_admit_button)
		self.dialog = MDDialog(title='Delete the name?',
	                               buttons=[cancel_button, admit_button])
		self.dialog.open()

	def deleting_cancel_button(self,obj):
		self.dialog.dismiss()

	def deleting_admit_button(self,obj):
		self.dialog.dismiss()
		toast("Name deleted", duration = 3)



class YourContainer(IRightBodyTouch, MDBoxLayout):
	pass
	#adaptive_width = True
	#edit_button = MDIconButton(icon='pencil', on_release=close_dialog)
	#delete_button = MDIconButton(icon='delete', on_release = app.delete_name)



if __name__ == "__main__":
    Main().run()
