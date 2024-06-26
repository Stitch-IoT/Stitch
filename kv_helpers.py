kv = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient kivy_gradient.Gradient
<LoadingScreen>:
    orientation: "vertical"
    spacing: "10dp"
    padding: "20dp"
    
    CustomLabel:
        text: "Loading..."
        halign: "center"
        font_style: "H6"
    
    AsyncImage:
        source: "lod.gif"  # Replace "loading.gif" with the path to your GIF file
        anim_delay: 1/30  # Adjust the animation delay as needed

    MDProgressBar:
        id: progress_bar
        size_hint_y: None
        height: "20dp"
        color: app.theme_cls.primary_color
        
<WordSectionContent>:
    md_bg_color: "#FFFFE8"
	id: word_section_content
	MDBoxLayout:
        orientation: 'vertical'
        MDIconButton:
            icon : "arrow-left"
            on_press : app.back_to_home_screen()

        MDScrollView:
            MDList:
                id: list_of_names


        MDIconButton:
            pos_hint: {"center_x": .5, "center_y": .1}
            spacing: 50
            id: plus
            icon: "plus"
            icon_size: 45
            adaptive_size: True
            on_press: app.add_name()

<SoundSectionContent>:
    md_bg_color: "F6E5FF"
	id: sound_section_content
	MDBoxLayout:
		orientation: 'vertical'
		MDIconButton:
			icon : "arrow-left"
			size_hint_y : .1
			on_press : app.back_to_home_screen()
		CustomLabel:
			halign: "center"
			text: "Виберіть звук"
			size_hint_y : .08
			font_size : "20sp"

		MDGridLayout:
			pos_hint: {"center_x": .5, "center_y": .5}
			cols: 2
			spacing: '3dp'
			CustomIconButton:
				icon : "bell"				
				text: 'Дзвінок'
				text_color: 0,0,0, 1  
				md_bg_color: 0,0,0,0
			    line_color: 0,0,0,1
				icon_color: 0,0,0, 1
				font_size: '16sp'  
				icon_size: '24dp'
				spacing: None
				size_hint_x: .5
				size_hint_y: .5


			CustomIconButton:
				icon : "alarm-light"
				text: 'Сигналізація'
				text_color: 0,0,0,1 
				md_bg_color: 0,0,0,0
			    line_color: 0,0,0,1
				icon_color: 0,0,0,1 
				font_size: '16sp'  
				icon_size: '24dp'  
				size_hint_x: .5
				size_hint_y: .5


			CustomIconButton:
				icon : "car"				
				text: 'Сигнал авто'
				text_color: 0,0,0, 1  
				md_bg_color: 0,0,0,0
			    line_color: 0,0,0,1
				icon_color: 0,0,0, 1
				font_size: '16sp'  
				icon_size: '24dp'
				size_hint_x: .5
				size_hint_y: .5


			CustomIconButton:
				icon : "lock"				
				text: 'Більше'
				text_color: 0,0,0, 1  
				md_bg_color: 0,0,0,0
			    line_color: 0,0,0,1
				icon_color: 0,0,0, 1
				font_size: '16sp'  
				icon_size: '24dp'
				size_hint_x: .5
				size_hint_y: .5


<SettingsSectionContent>:
    id: settings_section_content
    
	MDBoxLayout:
		orientation: 'vertical'
		
		MDIconButton:
			icon : "arrow-left"
			size_hint_y : .1
			on_press : app.back_to_home_screen()
			
        CustomLabel:
            halign: "center"
            text: "lol kek"
        AsyncImage:
            source: "asserts/roll.gif" 
            anim_delay: 1/30  
        

<ScreenOne>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
            texture: Gradient.vertical(get_color_from_hex("fafad7"), get_color_from_hex("FFFFE7"))
    MDFloatLayout:
        
        CustomLabel:
            text : "SoundTouch"
            font_size : "28dp"
            size_hint_y : 0.3
            halign : "center"
            pos_hint : {"center_y": .75}
            
    
            
        CustomIconButton:
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    texture: Gradient.horizontal(get_color_from_hex("985ce0"), get_color_from_hex("#7915a3"))
            halign : "center"
            padding : 30
            icon : "file-word-box"				
            text: 'Слова'
            text_color: 1,1,1,1  
            line_color: 0,0,0,1
            icon_color: 1,1,1,1 
            font_size: '18sp'  
            icon_size: '24dp'
            size_hint_x: 0.7
            pos_hint: {"center_x": 0.5, "center_y": 0.50}
            on_press: app.word_section()


        CustomIconButton:
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    texture: Gradient.horizontal(get_color_from_hex("985ce0"), get_color_from_hex("#7915a3"))
            padding : 30
            icon : "volume-high"
            text: 'Звуки'
            text_color: 1,1,1,1   
            md_bg_color: 0,0,0,0
            line_color: 0,0,0,1
            icon_color: 1,1,1,1 
            font_size: '18sp'  
            icon_size: '24dp'  
            size_hint_x: 0.7
            pos_hint: {"center_x": 0.5, "center_y": 0.35}
            on_press : app.sound_section()


        CustomIconButton:
            canvas.before:
                Color:
                    rgb: 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
                    texture: Gradient.horizontal(get_color_from_hex("bd92e8"), get_color_from_hex("b483e6"))
            padding : 15
            icon : "cog"
            text: 'Налаштування'
            text_color: 1,1,1,1 
            line_color: 0,0,0,1
            icon_color: 1,1,1,1
            font_size: '18sp' 
            icon_size: '24dp'  
            size_hint_x: 1
            pos_hint: {"center_x": 0.5}
            on_press : app.settings_section()

<Content>:
    
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
        panel_color: "faecbe"
		text_color_normal: 0, 0, 0, 1
		text_color_active: 142/255, 56/255, 255/255, 1
		spacing : 0
		id : bottom_nav
    	MDBottomNavigationItem:

			icon: 'home'
			id: home_screen
			name: "home"
			ScreenOne:

		MDBottomNavigationItem:
		    icon : 'play-circle'
			id : screen2
			name : "play"
			MDFloatLayout:
                canvas.before:
                    Color:
                        rgb: 1, 1, 1
                    Rectangle:
                        size: self.size
                        pos: self.pos
                        texture: Gradient.vertical(get_color_from_hex("#EDCDFF"), get_color_from_hex("#F6E5FF"))
				CustomLabel:
					id : detecting_label
					adaptive_size: True
					text : 'Почати розпізнавання'
					pos_hint : {"center_x":.5, "center_y":.6}
					font_size : "28dp"


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
		        md_bg_color: "#FFFFE8"
		    	orientation: 'vertical'
		    	MDFloatLayout:

			        CustomIconButton:
			            canvas.before:
                            Color:
                                rgb: 1, 1, 1
                            Rectangle:
                                size: self.size
                                pos: self.pos
                                texture: Gradient.horizontal(get_color_from_hex("985ce0"), get_color_from_hex("#7915a3"))
                                
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
			            line_color: 0, 0, 0, 1

			        CustomLabel:
		    			text: "Результат:"
		    			font_size : "16sp"
		    			pos_hint: {"center_x": .52, "center_y": .6}
		    			size_hint_x : None
		    			bold: True

		    		CustomLabel:
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
			            font_name: 'BenguiatGothicC_Bold'
			        	text: 'Очистити'
			            pos_hint: {"center_x": 0.5, "center_y": 0.55}
			            on_press : app.clear_text_field()


			        CustomIconButton:
			            canvas.before:
                            Color:
                                rgb: 1, 1, 1
                            Rectangle:
                                size: self.size
                                pos: self.pos
                                texture: Gradient.horizontal(get_color_from_hex("985ce0"), get_color_from_hex("#7915a3"))
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
			            line_color: 0, 0, 0, 1




"""
