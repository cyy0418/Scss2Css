# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
try:
  import scsscompiler
except ImportError:
  from . import scsscompiler

SETTING_SHOW_ALERT = "showErrorWithWindow"

#message window
class MessageWindow:
  def __init__(self, message=''):
    self.show(message)

  def show(self, message):
    if message == '':
      return
    settings = sublime.load_settings('scss2css.sublime-settings')
    project_settings = sublime.active_window().active_view().settings().get("scss2css")
    if project_settings is None:
      project_settings = {}
    show_alert = project_settings.get(SETTING_SHOW_ALERT, settings.get(SETTING_SHOW_ALERT,True))

    if not show_alert:
      return

    sublime.error_message(message)


############################
##### SUBLIME COMMANDS #####
############################

#single scss file
class ScssToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    s2c = scsscompiler.Compiler(self.view)
    resp = s2c.convertOne()
    MessageWindow(resp)


class AutoScssToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    s2c = scsscompiler.Compiler(self.view)
    resp = s2c.convertOne(is_auto_save=True)
    MessageWindow(resp)


#all scss files
class AllScssToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    s2c = scsscompiler.Compiler(self.view)
    sublime.status_message("Compiling .scss files...")
    resp = s2c.convertAll()

    if resp != "":
      MessageWindow(resp)
    else:
      sublime.message_dialog("All .scss files compiled successfully")


#listener to current scss file
class ScssToCssSave(sublime_plugin.EventListener):
  def on_post_save(self, view):
    view.run_command("auto_scss_to_css")


#change css base setting
class SetScssBaseCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Enter Your scss Base Directory: ", '', lambda s: self.set_scss_setting(s), None, None)

  def set_scss_setting(self, text):
    settings_base = 'scss2css.sublime-settings'

    settings = sublime.load_settings("scss2css.sublime-settings")

    if os.path.isdir(text):
      settings.set("scssBaseDir", text)
      sublime.save_settings(settings_base)  # have to assume this is successful...

      sublime.status_message("scss Base Directory updated")
    else:
      sublime.error_message("Entered directory does not exist")


# set the css output folder to auto
class ResetScssBaseAuto(sublime_plugin.WindowCommand):
  def run(self):
    settings_base = 'scss2css.sublime-settings'

    settings = sublime.load_settings("scss2css.sublime-settings")

    settings.set("outputDir", "auto")
    sublime.save_settings(settings_base)

    sublime.status_message("Output directory reset to auto")


class SetOutputDirCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Enter CSS Output Directory: ", "", lambda s: self.set_output_dir(s), None, None)

  def set_output_dir(self, text):
    settings_base = 'scss2css.sublime-settings'

    settings = sublime.load_settings("scss2css.sublime-settings")

    if os.path.isdir(text):
      settings.set("outputDir", text)
      sublime.save_settings(settings_base)

      sublime.status_message("Output directory updated")
    else:
      sublime.error_message("Entered directory does not exist")


#toggle minification
class toggleCssMinificationCommand(sublime_plugin.WindowCommand):
  def run(self):
    #show yes/no input
    self.window.show_quick_panel(["Minify css", "Don't minify css"], lambda s: self.set_minify_flag(s))

  def set_minify_flag(self, minify):
    minify_flag = False

    if minify == 0:
      minify_flag = True

    settings = sublime.load_settings("scss2css.sublime-settings")

    if minify == -1:
      #input was cancelled, don't change
      minify_flag = settings.get("minify", True)  # existing or default

    settings.set("minify", minify_flag)
    sublime.save_settings("scss2css.sublime-settings")

    sublime.status_message("Updated minify flag")
