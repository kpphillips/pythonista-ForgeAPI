'''
UI components to show data to user
'''
import ui
import model
from PIL import Image
import forgeapi
import datetime
import viewModelPlot
			
def __setupUi(view,model):
	vdel=MyTableViewDelegate(model)
	print('delegate')
	print(model)
	datasource=MyTableViewDataSource(model)
	view['tableview1'].data_source=datasource
	view['tableview1'].delegate=vdel
	
	imgView=view['imageview1']
	
	label=view['label1']
	
	#userName=model['user'].name
	label.text='Aquiring user...'
	
	#webview
	#segment
	sc1=view['segmentedcontrol1']
	sc1.enabled=False
	cv=view['view1']
	cv.background_color='#ff916a'
	
	#project button
	b4=view['button4']
	b4.enabled=False
	
	#activity indicator
	ai=ui.ActivityIndicator()
	ai.style=ui.ACTIVITY_INDICATOR_STYLE_WHITE
	rect=(12.5,5,20,20)
	ai.frame=rect
	cv.add_subview(ai)
	ai.start()
	
	view.present('sheet')
	return view

def showViewWithData(model):
	v=__setupUi(ui.load_view(),model)
	return v
	
def updateView(model, view):	
	#s=model['state']
	svs=view.subviews
	ms = model['state']
	print(f'forgeui.py updateView with State: {ms}')	
	for v in svs:		
		vn = v.name
		if ms != 'User' and vn == 'view1':
			v.background_color='#6aff9e'
			ai=v.subviews[0]
			ai.stop()
			
		if ms == 'User' and vn == 'imageview1':
			imgView=view['imageview1']
			imgView.load_from_url(model['user'].imgUrl)
			label=view['label1']
			userName=model['user'].name
			label.text=userName		
		
		if ms != 'User' and vn == 'tableview1':				
			v.data_source.model=model
			v.reload_data()		
		
		#print(f'before segment update {vn}')
		
		if ms == 'MetaGuidObjects' and vn == 'segmentedcontrol1':
			print(f'updating segment: {v.name}')
			v.enabled=True
			propObjTogglePressed(v)
			
		if ms == 'MetaProperties' and vn == 'segmentedcontrol1':
			print(f'updating segment: {v.name}')
			v.selected_index=1
			#v.enabled=True
			#propObjTogglePressed(v)
		if ms == 'Projects' and vn == 'button4':
			print(f'updating segment: {v.name}')
	pass
	
def plotPressed(sender):	
	data=model.dataFromState(forgeapi._model)
	state=forgeapi._model['state']
	print()
	print(f'Plot Type: {type(data)}, Count: {len(data)}, First Element: {data[0]}, State: {state}')
	viewModelPlot.presentPlotData(data,state)

def graphPressed(sender):
	m=forgeapi._model
	data=model.dataFromState(m)
	state=m['state']
	os=m['objectstate']
	if os == 'Model Objects':
		print()
		print(f'Plot Type: {type(data)}, Model Objects: {len(data)}, First Element: {data[0]}, State: {state}')
		mps=m['metaproperties']
		viewModelPlot.presentGraphData(data,os,mps,m)
	
def propObjTogglePressed(sender):
	i=sender.selected_index
	#print('Segment Index:{i}')
	model=forgeapi._model
	if i == 0:
		model['state'] = 'MetaGuidObjects'
	else:
		model['state'] = 'MetaProperties'
	#print('---model state on toggle')
	#print(model['state'])
	model['objectstate']='Model Objects'	
	svs=sender.superview.subviews
	for v in svs:
		if v.name == 'tableview1':
			v.data_source.model=model
			print('reloading tableview')
			v.reload_data()				
	
def viewJaysonPressed(sender):
	model.viewJayson()
	
def parseProjectsPressed(sender):
	print(sender)
	pass

#TableView Delegate
class MyTableViewDelegate (object):
	 
	def __init__(self, model):
		self.model = model
		
	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.	
		svs=tableview.superview.subviews
		for v in svs:
			if v.name == 'view1':
				v.background_color='#ff916a'
				ai=v.subviews[0]
				ai.start()
		start = datetime.datetime.now()	
		model.selected(self.model,row)
		pass
		
	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Monitor'

#tableview datasource
class MyTableViewDataSource (object):
	
	def __init__(self, _model):
		self.model = _model
		self.cells = []
		
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		state=self.model['state']
		#print(f'UI datafromststate {state}')
		data=model.dataFromState(self.model)
		#print(f'Data: {data}')
		#print('number of rows')
		self.cells=[]
		return len(data)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		data=model.dataFromState(self.model)		
		
		if data[row].name:
			cell.text_label.text = data[row].name
		elif data[row].objectId:
			idstr = str(data[row].objectId)
			cell.text_label.text = idstr
		else:
			cell.text_label.text = 'Bro, no name or id'		
		self.cells.append(cell)
		#print(cell.text_label.text)
		return cell

	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		return self.model['state']
	
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		state = self.model['state']
		#print('tableview_can_delete')
		#print(state)
		if state == 'Folder':
			data=model.dataFromState(self.model)	
			if data[row].type == 'items':		
				#print('true')
				return True
			else:
				return False
		else:
			#print('false')
			return False
	
	def select_row(self, sel_row):
		items=self.model['items']
		for cell,item in zip(self.cells,items):
			cell.accessory_type = ""			
			self.cells[sel_row].accessory_type = 'checkmark'
			#self.sel_item = sel_row
			#print(f'checkbox? {cell.accessory_type}')
			#print(cell.text_label.text)
	
	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		print('update model with monitoring')
		#data=model.dataFromState(self.model)
		self.select_row(row)		
		pass
	
