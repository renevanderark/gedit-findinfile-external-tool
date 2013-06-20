#!/usr/bin/python
import os
import subprocess
from gi.repository import Gtk

class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Find in files")

		self.box = Gtk.Box()
		self.entry = Gtk.Entry()
		self.button = Gtk.Button(label="Search")
		self.ext_entry = Gtk.Entry()
		self.dir_entry = Gtk.Entry()
		self.dir_entry.set_text(os.environ['GEDIT_CWD'])
		self.ext_entry.set_text("php,js,css,phtml")
		self.button.connect("clicked", self.on_button_clicked)
		self.entry.connect("activate", self.on_button_clicked)
		self.dir_entry.connect("activate", self.on_button_clicked)
		self.ext_entry.connect("activate", self.on_button_clicked)
		self.box.add(self.dir_entry)
		self.box.add(self.ext_entry)
		self.box.add(self.entry)
		self.box.add(self.button)
		self.add(self.box)

	def on_button_clicked(self, widget):
		if(len(self.entry.get_text()) > 0):
			ex = ["grep", "-r", "-n", self.entry.get_text(), "--exclude-dir=.svn", self.dir_entry.get_text()]
			for include in self.ext_entry.get_text().split(","):
				ex.append("--include=*." + include)
			results = subprocess.Popen(ex, stdout=subprocess.PIPE).communicate()[0].split("\n")
			for line in results:
				parts = line.replace(self.dir_entry.get_text() + "/", "").split(":")
				if(len(parts) > 1):
					print parts[0] + ":" + parts[1] + ": " + parts[2]

			print "found '" + self.entry.get_text() + "' " + str(len(results)-1) + " times"
			Gtk.main_quit()
		

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

