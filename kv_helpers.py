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
        text_color_focus: 0, 0, 0, 1
        text_color_normal: 0, 0, 0, 1
        hint_text_color_focus: "gray"
        line_color_focus: "gray"


MDFloatLayout:
	MDBottomNavigation:
		text_color_normal: 0, 0, 0, 1
		text_color_active: 57/255, 93/255, 203/255, 1
		spacing : 0
		id : bottom_nav
    	MDBottomNavigationItem:
	        icon : 'home'
	        id : home_screen
			name : "home"
			MDScrollView:
				size: self.size
				MDList:
					id : list_of_names



			MDIconButton:
				pos_hint: {"center_x": .5, "center_y": .1}
				spacing : 50
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
					text : 'Почати розпізнавання'
					pos_hint : {"center_x":.5, "center_y":.6}
					font_size : "24dp"


				MDIconButton:
					id: detecting_button
					icon : "play"
					icon_size: "60sp"
					adaptive_size: True
					pos_hint : {"center_x":.5, "center_y":.4}
					on_press: app.general_detection()



		MDBottomNavigationItem:
		    icon: 'account-voice'
		    id: screen3
		    name: "translation"

		    MDBoxLayout:
		    	orientation: 'vertical'
		    	MDFloatLayout:

			        MDRectangleFlatIconButton:
			        	id : audio_to_text_button
			            text: 'Почати'
			            font_size : "16sp"
			            icon: 'play'
			            icon_color: 1, 1, 1, 1
			            size_hint_y: 0.15
			            size_hint_x: 0.4
			            pos_hint: {"center_x": 0.5, "center_y": 0.8}
			            on_press: app.start_audio_to_text()
			            theme_text_color: "Custom"
			            text_color: 1, 1, 1, 1  
			            md_bg_color: 0, 0, 0, 1 
			            line_color: 0, 0, 0, 1

			        MDLabel:
		    			text: "Результат:"
		    			font_size : "16sp"
		    			pos_hint: {"center_x": .52, "center_y": .6}
		    			size_hint_x : None
		    			bold: True

		    		MDLabel:
		    			id : result_from_audio
		    			text : ""
		    			pos_hint: {"center_x": .5, "center_y": .3}
		    			size_hint: 0.9, None
		    			font_size : "16sp"


		        Widget:
			        size_hint_y: None
			        height: 3
			        canvas:
			            Color:
			                rgba: 0, 0, 0, 1 
			            Line:
			                points: self.x, self.y, self.width, self.y

		    	MDFloatLayout:

			    	MDTextField:
			            id: translation_input
			            hint_text: "Введіть текст"
			            helper_text_mode: "on_focus"
			            pos_hint: {"center_x": 0.5, "center_y": 0.7}
			            size_hint_x: 0.85
			            text_color_focus: 0, 0, 0, 1
			            text_color_normal: 0, 0, 0, 1
			            hint_text_color_focus: "gray"
			            line_color_focus: "gray"

			        MDFlatButton:
			        	text: 'Очистити'
			            pos_hint: {"center_x": 0.5, "center_y": 0.55}
			            on_press : app.clear_text_field()


			        MDRectangleFlatIconButton:
			        	id : text_to_audio_button
			            text: 'Відтворити'
			            font_size : "16sp"
			            icon: 'play'
			            icon_color: 1, 1, 1, 1
			            on_press : app.start_text_to_audio()
			            size_hint_y: 0.15
			            size_hint_x: 0.4
			            pos_hint: {"center_x": 0.5, "center_y": 0.25}
			            theme_text_color: "Custom"
			            text_color: 1, 1, 1, 1  
			            md_bg_color: 0, 0, 0, 1 
			            line_color: 0, 0, 0, 1




"""
