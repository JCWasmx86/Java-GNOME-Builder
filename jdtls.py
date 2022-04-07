#!/usr/bin/env python3

import os
import json
import tempfile
import uuid
import gi

from gi.repository import GLib
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Ide

#123#class JavaCustomCommandMapper(Ide.Object,Ide.LspCustomCommandMapper):
#123#	def __init__(self, *args, **kwargs):
#123#		super().__init__(*args, **kwargs)
#123#		GObject.GObject.__init__(self)
#123#
#123#	def do_map_command(self, command):
#123#		arguments = command.lookup_value("arguments", None)
#123#		return arguments.get_child_value(0)
#123#
#123#class JavaService(Ide.LspService, Ide.LspCustomCommandMapper):
#124#class JavaService(Ide.LspService):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		context = self.get_context()
		self.set_inherit_stderr(True)
		self.set_search_path([os.path.expanduser("~/.local/bin"), "/app/bin", "/usr/bin", "/usr/local/bin"])
		if (context is None):
			self.metadata_workdir = tempfile.gettempdir() + "/.jdtls-metadata-"
		else:
			self.metadata_workdir = context.get_workdir().get_name() + "/.jdtls-metadata"
		try:
			os.makedirs(self.metadata_workdir)
		except:
			pass
		self.set_program(os.path.expanduser("~/.local/bin/jdtls"))
#123#		self.mapper = JavaCustomCommandMapper()

	def do_map_command(self, command):
		return JavaService.map_workspace_edit(command)

	def do_configure_client(self, client):
		client.add_language("java")
		client.connect("load-configuration", self.on_load_configuration)
#123#		client.register_custom_command("java.apply.workspaceEdit", self.mapper)

	def do_configure_launcher(self, pipeline, launcher):
		launcher.push_argv(self.metadata_workdir)

	def on_load_configuration(self, data):
		try:
			b = GLib.VariantBuilder(GLib.VariantType.new("a{sv}"))
			b.add_value(JavaService.create_dict_entry_int("java.format.tabSize", 8))
			b.add_value(JavaService.create_dict_entry_boolean("java.format.insertSpaces", False))
			return GLib.Variant.new_variant (b.end())
		except Error as e:
			Ide.debug ("On Load Configuration Error: {}".format(e.message))
			return GLib.Variant ("a{sv}", {})

	@staticmethod
	def create_dict_entry_boolean(key, val):
		vk = GLib.Variant.new_string (key)
		vv = GLib.Variant.new_variant(GLib.Variant.new_boolean(val))
		return GLib.Variant.new_dict_entry(vk, vv)

	@staticmethod
	def create_dict_entry_int(key, val):
		vk = GLib.Variant.new_string (key)
		vv = GLib.Variant.new_variant(GLib.Variant.new_int64(val))
		return GLib.Variant.new_dict_entry(vk, vv)

class JavaDiagnosticProvider(Ide.LspDiagnosticProvider, Ide.DiagnosticProvider):
	def do_load(self):
		JavaService.bind_client(self)

class JavaCompletionProvider(Ide.LspCompletionProvider, Ide.CompletionProvider):
	def do_load(self, context):
		JavaService.bind_client(self)

class JavaHoverProvider(Ide.LspHoverProvider):
	def do_prepare(self):
		self.props.priority = 100
		JavaService.bind_client(self)

#123#class JavaCodeActionProvider(Ide.LspCodeActionProvider, Ide.CodeActionProvider):
#123#	def do_load(self):
#123#		JavaService.bind_client(self)

class JavaRenameProvider(Ide.LspRenameProvider):
	def do_load(self):
		JavaService.bind_client(self)

class JavaSymbolResolver(Ide.LspSymbolResolver):
	def do_load(self):
		JavaService.bind_client(self)

class JavaHighlighter(Ide.LspHighlighter):
	def do_load(self):
		JavaService.bind_client(self)

class JavaFormatter(Ide.LspFormatter):
	def do_load(self):
		JavaService.bind_client(self)
