from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views  import RecycleDataViewBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior, ButtonBehavior
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
path = '/storage/emulated/0/'
Builder.load_string('''
<DesignLabel>:
	size_hint_y:None
	height:dp(40)
	orientation:'horizontal'
	
	MDIconButton:
		icon:root.icon_name
	MDLabel:
		text:root.file_name
	CheckBox:
		active:root.check_status
		
<SelectableLabel>:
	canvas.before:
		Color:
			rgba:(0, 0.3,0,0.5) 
		Rectangle:
			size:self.size
			pos:self.pos
<RV>:
	viewclass:'SelectableLabel'
	SelectedRecycleBoxLayout:
		orientation:'vertical'
		default_size:None, dp(56)
		default_size_hint:1, None
		size_hint_y:None
		height:self.minimum_height
		spacing: dp(12)
<CustomLabel>:
	size_hint_y:None
	height:dp(56)
<CustomTitleBar>:
	id:title
	size_hint_y:None
	height:dp(60)
	
''')
class CustomTitleBar(MDBoxLayout):
	path = StringProperty()
	backbutton = ObjectProperty()
	customlabel = ObjectProperty()
	option_button = ObjectProperty()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.backbutton = MDIconButton(icon='arrow-left')
		self.option_button = MDIconButton(icon='dots-vertical')
		self.customlabel = CustomLabel(text=self.path, color=(0,0.5,0,1))
		self.add_widget(self.backbutton)
		self.add_widget(self.customlabel)
		self.add_widget(self.option_button)
	def back(self, *args):
		print(App.get_running_app().root.path)
		dirs = self.path.split('/')
		for i in range(len(dirs)):
			if '' in dirs:
				dirs.pop(dirs.index(''))
		name = dirs[-1:][0]
		dirs.pop(dirs.index(name))
		new = ''
		for i in dirs:
			new += ('{}/'.format(i))
			
		self.path = new
		#App.get_running_app().root.path = new	
		
class SelectedRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	pass
class CustomLabel(Label):
	pass
	
class DesignLabel(MDBoxLayout):
	icon_name = StringProperty()
	file_name = StringProperty()
	check_status = BooleanProperty()
		
class SelectableLabel(RecycleDataViewBehavior,  DesignLabel):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)
	import os
	#global path 
	def refresh_view_attrs(self, rv, index ,data):
		self.index = index 
		return super().refresh_view_attrs(rv, index, data)
	def on_touch_down(self, touch):
		if super().on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)
	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected 
		if is_selected:
			#toast('selected {0}, type {1}'.format(rv.data[index],type(rv.data[index])))
			#name = rv.data[index]['file_name']
			#print(name)
			self.name = rv.data[index]['file_name']
			print(self.name)
			path  = os.path.join(rv.path, self.name)
			rv.path = path
		else:
			#toast('removed {0}'.format(rv.data[index]))
			pass
			
			
class RV(RecycleView):
	path = StringProperty()
	changepath = StringProperty()
	state = BooleanProperty(True)
	def __init__(self, **kwargs):
		import os
		self.history = []
		super().__init__(**kwargs)
		directory_content = []
		content = os.listdir(path)
		for file in content:
			path_dict= {}
			file_path = os.path.join(path, file)
			if os.path.isfile(file_path):
				path_dict['icon_name'] = 'file'
				path_dict['file_name'] = file
				path_dict['check_status'] = False
			else:
				path_dict['icon_name'] = 'folder'
				path_dict['file_name'] = file
				path_dict['check_status'] = False
				
			directory_content.append(path_dict)
		self.data = directory_content
				
		#self.data = [{'file_name':x, 'icon_name':'folder', 'check_status':False} for x in os.listdir(self.path)]
		self.bind(path=self.changeDir)
	def changeDir(self, instance, path):
		directory_content = []
		if os.path.isdir(path):
			self.history.append(path)
			content = os.listdir(path)
			for file in content:
				path_dict= {}
				file_path = os.path.join(path, file)
				if os.path.isfile(file_path):
					path_dict['icon_name'] = 'file'
					path_dict['file_name'] = file
					path_dict['check_status'] = False
				else:
					path_dict['icon_name'] = 'folder'
					path_dict['file_name'] = file
					path_dict['check_status'] = True
				directory_content.append(path_dict)
			self.data = directory_content
				
			#self.data = [{'file_name':x} for x in os.listdir(path)]
			
class Dir(MDBoxLayout):
	path = StringProperty()
	label = ObjectProperty()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.history = []
		self.orientation='vertical'
		self.recycle = RV(path=self.path)
		self.label = CustomTitleBar(path=self.recycle.path)
		self.label.backbutton.bind(on_press=self.back)
		self.add_widget(self.label)
		self.add_widget(self.recycle)
		self.history.append(self.path)
		self.new = self.path
		self.label.path = self.recycle.path
		print(self.label.path)
	def back(self, *args):
		
		if True:
			dirs = self.recycle.path.split('/')
			for i in range(len(dirs)):
				if '' in dirs:
					dirs.pop(dirs.index(''))
			name = dirs[-1:][0]
			dirs.pop(dirs.index(name))
			new = '/'
			for i in dirs:
				new += ('{}/'.format(i))
				
			self.path = new
			self.recycle.path = new
			self.label.path = self.recycle.path 
			toast(new)
		'''
		if len(self.recycle.history)> 1:
			self.recycle.history.pop()
			new = self.recycle.history[-1:][0]
			self.recycle.path = new
		print(self.recycle.history)
		'''
				
class Main(MDApp):
	def build(self):
		#self.droot.label.backbutton.bind(on_press=self.back)
		return Dir(path = '/storage/emulated/0/python')
		
if __name__ =='__main__':
	Main().run()