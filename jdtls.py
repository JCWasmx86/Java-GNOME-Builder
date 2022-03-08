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

class JavaService(Ide.LspService):
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
		self.set_program('jdtls')

	def do_configure_client(self, client):
		client.add_language("java")

	def do_configure_launcher(self, pipeline, launcher):
		launcher.push_argv(self.metadata_workdir)

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

class JavaCodeActionProvider(Ide.LspCodeActionProvider, Ide.CodeActionProvider):
	def do_load(self):
		JavaService.bind_client(self)

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
