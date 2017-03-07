import sublime, sublime_plugin, os
# checks sidebar  has multiple same project folder name 
def hasMultipleSameProjectName(view):
	result = False
	projectFolderNameList = []
	# Go through project folders
	for folder in view.window().folders():
		# Split project folder and path
		currentProjectFolder = os.path.split(folder)[1]
		# Check if the project name is in the list
		if(currentProjectFolder not in projectFolderNameList):
			# Path is not in the projectFolderNameList so adding it
			projectFolderNameList.append(currentProjectFolder)
		else:
			# Path is exist setting result to true 
			# and breaking the for since we got what we need
			result = True
			break
	return result
##
 # Writes the file status into Status Bar for given view
 #
def writeStatus(view):
	path = view.file_name()
	# Checking are there any modification on view
	isDirty = view.is_dirty()
	filename = ("❗" if isDirty else "") + view.name()
	# checking is the path exist if not its a new file
	if path is not None:
		# Spliting for path and name of the file
		file_path = os.path.split(path)[0]
		# Go through project folders
		for projectFolder in view.window().folders():
			# print(projectFolder)
			if (projectFolder not in file_path):
				continue
			# print("This is", projectFolder)
			projectPath = os.path.split(projectFolder)[0]
			# if there is multiple project name that has same name better get 
			# one above folder as well
			if hasMultipleSameProjectName(view):
				projectPath = os.path.split(projectPath)[0]
			# replace the folder
			path = path.replace(projectPath + '/', '', 1)
			# we don't need to continue the whole folder paths
			break
		filename = ("❗" if isDirty else "🍺 ") + path
	# else:
	# 	path = 'untitled'
	# view.set_status('file_name', ("◉ " if isDirty else "◎ ") + 'untitled')
	view.set_status('file_name', filename)
##
 # Plugin Definition
 # 
class CurrentViewStatus(sublime_plugin.EventListener):
	def on_activated(self, view):
		writeStatus(view)
	def on_modified(self, view):
		writeStatus(view)