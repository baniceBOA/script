from kivymd.app import MDApp
from kivy.uix.dropdown import DropDown
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button


class Hinting(MDTextField):
	memory = ['jane','diana','Bravin','Brian']
	hints = ListProperty()
	entry = BooleanProperty('False')
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.hint_text = 'search'
		self.drop = DropDown(dismiss_on_select=True)
		self.bind(entry=self.drops)
		self.drop.bind(on_dismiss=self.diss)
		self.drop.bind(on_select=lambda select_instance, x: setattr(self, 'text', x))
	def on_text(self, instance, value):
		if not self.text:
			#don't do anything if no text is found'
			pass
		else:
			for name in self.memory:
				if value in name and name not in self.hints:
					self.hints.append(name)
					self.label = Button(text=str(name),
													size_hint=(None,None), 
													width=self.width,
													background_normal='',
													background_color=(0.8,0.8,0.8,1),
													color=(0,0,0,1))
					self.label.bind(on_release=lambda lb_instance: self.drop.select(lb_instance.text))
					self.drop.add_widget(self.label)
				if self.hints:
					# trigger the drop down 
					self.entry = True
			
	def drops(self, instance, value):
		''' opens the dropdown '''
		self.drop.open(self)
	def diss(self, instance):
		# restore to so as to trigger on the next entry
		self.entry = False
		
			
class Root(MDFloatLayout):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.hints = Hinting(hint_text='search')
		self.hints.pos_hint = {'center_x':0.5, 'center_y':0.9}
		self.add_widget(self.hints)
		
			
class Main(MDApp):
	def build(self):
		return Root()
		
if __name__ == '__main__':
	Main().run()