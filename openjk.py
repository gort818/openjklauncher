#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import gi
import pygame
import fileinput
import re
import urllib2
import tarfile
import shutil
import glob
import requests
import ConfigParser

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GObject, GLib
from os import system
from sys import platform
from distutils.dir_util import copy_tree

# Check operating system
if sys.platform.startswith('linux'):
    homedir = os.path.expanduser('~')
    # gamedir = homedir + '/Games/OpenJk'
    gamedir = ""
    configdir = homedir + '/.local/share/openjk/base'
    configfile = configdir + '/autoexec.cfg'
    openjk_config = configdir + '/ojkl.cfg'
    tmpdir = '/tmp'
    path = configdir + '/ojkl.cfg'
    resourcedir = '/usr/share/openjk/resources'
    exe = gamedir + '/openjk.x86_64'
    print 'Running on Linux'
cancel = 0

##TODO add support for Windows and OSX


# Load the css file for glade
# cssProvider = Gtk.CssProvider()
# cssProvider.load_from_path('/usr/share/openjk/resources/style.css')
# screen = Gdk.Screen.get_default()
# styleContext = Gtk.StyleContext()
# styleContext.add_provider_for_screen(screen, cssProvider,
#        Gtk.STYLE_PROVIDER_PRIORITY_USER)


# setup audio
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# setup net
sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=2)
sess.mount('http://', adapter)


# Check where jedi academy base is installed




# check directory
def check_directory():
    if not os.path.isdir(configdir):
        os.makedirs(configdir)


# Create Config file
def create_file():
    if not os.path.isfile(configfile):
        file = open(configfile, 'w+')
        file.write('#mod "0"\n')
        file.write('seta r_mode "4"\n')
        file.write('seta r_fullscreen "0"\n')
        file.write('seta r_noborder "0"\n')
        file.close
    shutil.copy(configfile, configdir + '/autoexec_sp.cfg')


def create_openjk_config(path):
    config = ConfigParser.ConfigParser()
    config.add_section("Path")
    config.set("Path", "folder", "null")

    with open(path, "wb") as config_file:
        config.write(config_file)


def check_settings(self):
    # Check for fullscreen
    global gamedir
    config = ConfigParser.ConfigParser()
    config.read(path)
    gamedir = config.get("Path", "Folder")
    print ("Game dir is : " + gamedir)
    if os.path.isdir(gamedir + '/japlus'):
        self.modlist.insert_text(1, 'Ja ++')

    if os.path.isdir(gamedir + '/MBII'):
        self.modlist.insert_text(2, 'MBII')

    if os.path.isfile(configfile):
        if 'seta r_fullscreen "1"' in open(configfile).read():
            print "Fullscreen is on"
            self.checkbutton.set_active(True)
        else:
            print "Fullscreen is off"
            self.checkbutton.set_active(False)
            # Check for borderless window
        if 'seta r_noborder "1"' in open(configfile).read():
            print "Bordless window is on"
            self.checkbutton2.set_active(True)
        else:
            print "Bordless window is off"
            self.checkbutton2.set_active(False)
            # check for native resolution
        if 'seta r_mode "-2"' in open(configfile).read():
            print "Resolution is set to native"
            self.comboboxtext.set_active(0)
        else:
            print "Resolution is not set to native"
            self.comboboxtext.set_active(1)

            # check for mods

        if '#mod "1"' in open(configfile).read():
            print "Mod is set to Ja++"
            self.modlist.set_active(1)
            exe = gamedir + '/openjk.x86_64 +set fs_game japlus'
        if '#mod "0"' in open(configfile).read():
            print "Mod is not set"
            self.modlist.set_active(0)
            exe = gamedir + '/openjk.x86_64'


##################### Install script ###################





def install(self):
    cancel = 0
    sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
    sound_start.play()
    # global gamedir
    #self.window.hide()
    #self.folder.show()
    response = self.folder.run()
    if cancel == 1:
        return

##################### End of Install script ###################




def test(self):
    while Gtk.events_pending():
        Gtk.main_iteration()


def check_internet(self):
    try:
        response = urllib2.urlopen('https://google.com', timeout=2)
        print 'you are connected'
        return True
    except urllib2.URLError, err:
        print err
        print 'you are disconnected'
        self.errordialog.show()
        self.messagedialog.hide()


# print 'Your game directory is: ' + gamedir
print 'Your config directory is : ' + configdir


# Setting up the windows and widgets

class launcher:
    def __init__(self):

        self.builder = Gtk.Builder()

        self.builder.add_from_file(resourcedir+'/openjk.glade'
                                   )

        self.builder.connect_signals(self)

        self.single = self.builder.get_object('single')
        self.multi = self.builder.get_object('multi')
        self.overlay = self.builder.get_object('overlay')
        self.image = self.builder.get_object('image2')
        self.window2 = self.builder.get_object('window2')
        self.window3 = self.builder.get_object('window3')
        self.hd_res1 = self.builder.get_object('hd_res1')
        self.window = self.builder.get_object('window')
        self.comboboxtext = self.builder.get_object('comboboxtext')
        self.modlist = self.builder.get_object('modlist')
        self.install = self.builder.get_object('install')
        self.messagedialog = self.builder.get_object('messagedialog')
        self.errordialog = self.builder.get_object('errordialog')
        self.ok = self.builder.get_object('ok')
        self.ok3 = self.builder.get_object('ok3')
        self.install_label = self.builder.get_object('install_label')
        self.checkbutton = self.builder.get_object('checkbutton')
        self.checkbutton2 = self.builder.get_object('checkbutton2')
        self.window.connect('destroy', lambda w: Gtk.main_quit())
        self.window.show_all()
        self.messagedialog.hide()
        self.link = self.builder.get_object('link')
        self.link.set_label("Openjk @ Github.com")
        self.folder = self.builder.get_object("folder")
        self.ok_folder = self.builder.get_object("ok_folder")
        self.cancel_folder = self.builder.get_object("cancel_folder")
        check_directory()
        create_file()
        if not os.path.exists(path):
            create_openjk_config(path)
        check_settings(self)

    def on_ok_folder_clicked(self, widget):

        print("Open clicked")
        global gamedir
        gamedir = (self.folder.get_filename())
        config = ConfigParser.ConfigParser()
        config.read(path)
        config.set("Path", "folder", gamedir)
        with open(path, "wb") as config_file:
            config.write(config_file)
        print("Gamedir is now set to" + gamedir)
        self.folder.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()
        print(gamedir)


        def show_message():
            self.ok.set_visible(False)

        while Gtk.events_pending():
            Gtk.main_iteration()
        self.messagedialog.show()
        # self.ok.set_opacity(.25)
        self.ok.set_visible(False)
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.messagedialog.show()
        while Gtk.events_pending():
            Gtk.main_iteration()
        # self.install_label.set_text('Please Wait...')
        while Gtk.events_pending():
            Gtk.main_iteration()

        if check_internet(self) == True:
            show_message

        Gtk.main_iteration()
        site = 'https://builds.openjk.org/'
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }

        req = urllib2.Request(site, headers=hdr)
        Gtk.main_iteration()
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            self.errordialog.show()
            while Gtk.events_pending():
                Gtk.main_iteration()
            print e.fp.read()

        Gtk.main_iteration()
        content = page.read()
        Gtk.main_iteration()
        file = open('/tmp/tmp.html', 'w')
        file.write(content)
        file.close()
        print 'Checking openjk Builds for newest version'
        file = open('/tmp/tmp.html', 'r')
        lines = file.read()
        answer = re.findall(r'openjk[^<>]*?linux-64.tar.gz', lines)[-1]
        print answer
        base_url = 'https://builds.openjk.org/'
        file = base_url + answer
        print file
        Gtk.main_iteration()
        self.ok.set_visible(False)
        self.ok.set_sensitive(False)
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.messagedialog.show()
        self.ok.set_opacity(.25)
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.messagedialog.show()
        while Gtk.events_pending():
            Gtk.main_iteration()
        self.install_label.set_text('Please Wait...')
        while Gtk.events_pending():
            Gtk.main_iteration()
        print 'Downloading file now'
        for i in range(1):
            try:
                print ('Downloading %s' % answer)

                r = sess.get(file, stream=True, verify=False,
                             allow_redirects=True)
                total_length = r.headers.get('content-length')
                dl = 0
                total_length = int(total_length)
                with open('/tmp/' + answer, 'wb') as f:

                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            dl += len(chunk)
                            f.write(chunk)
                            print total_length
                            done = int(50 * dl / total_length)
                            sys.stdout.write('\r[%s%s]' % ('=' * done,
                                                           ' ' * (50 - done)))
                            sys.stdout.flush()
            except requests.exceptions.RequestException, e:
                print e
                sys.exit(1)

        # Gtk.main_iteration()
        print 'File finished downloading'
        print 'Extracting tarball'

        tar = tarfile.open('/tmp/' + answer)
        tar.extractall('/tmp/')
        tar.close()
        print 'Installing files'
        root_src_dir = tmpdir + '/install/JediAcademy/'
        root_dst_dir = gamedir

        copy_tree(root_src_dir, root_dst_dir)
        print 'Cleaning up....'
        print 'Done.\n'
        os.remove(tmpdir + '/' + answer)
        os.remove(tmpdir + '/tmp.html')
        shutil.rmtree(tmpdir + '/install')
        self.messagedialog.show()
        self.install_label.set_text('Done, Please press ok')
        self.ok.set_opacity(1)
        self.ok.set_visible(True)
        self.ok.set_sensitive(True)

        self.folder.hide()


    def on_cancel_folder_clicked(self, widget):
        self.folder.hide()

        cancel == 1
        return cancel

    def on_ok_clicked(self, widget):
        self.messagedialog.hide()

    def on_multi_enter_notify_event(self, widget, hover):
        sound_start = pygame.mixer.Sound(resourcedir + '/hover.WAV')
        sound_start.play()

    def on_single_enter_notify_event(self, widget, hover):
        sound_start = pygame.mixer.Sound(resourcedir + '/hover.WAV')
        sound_start.play()

    def on_exit_enter_notify_event(self, widget, hover):
        sound_start = pygame.mixer.Sound(resourcedir + '/hover.WAV')
        sound_start.play()

    def on_options_enter_notify_event(self, widget, hover):
        sound_start = pygame.mixer.Sound(resourcedir + '/hover.WAV')
        sound_start.play()

    def on_install_enter_notify_event(self, widget, hover):
        sound_start = pygame.mixer.Sound(resourcedir + '/hover.WAV')
        sound_start.play()

    def on_single_clicked(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        self.window.destroy()
        system(gamedir + "/openjk_sp.x86_64 +fs_game 'Openjk'")

    def on_multi_clicked(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        sound_open = pygame.mixer.Sound(resourcedir + '/start.WAV')
        sound_open.play()
        if '#mod "1"' in open(configfile).read():
            exe = gamedir + '/openjk.x86_64 +set fs_game japlus'
        elif '#mod "0"' in open(configfile).read():
            exe = gamedir + '/openjk.x86_64'
        else:
            exe = gamedir + '/openjk.x86_64'
        self.window.destroy()
        system(exe)

    def on_back_clicked(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/back.WAV')
        sound_start.play()
        self.window2.hide()
        self.window.show_all()

    def on_options_clicked(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        self.window.hide()
        self.window2.show_all()
        self.window2.connect('delete-event', lambda w, e: w.hide() \
                                                          or True)

    def on_exit_clicked(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        system('sleep .25')
        Gtk.main_quit()

    def on_comboboxtext_changed(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        model = widget.get_model()
        active = widget.get_active()
        if active == 0:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('seta r_mode "'):
                    line = 'seta r_mode "-2"\n'
                sys.stdout.write(line)
            shutil.copy(configfile, configdir + '/autoexec_sp.cfg')
            self.comboboxtext.set_active(0)

    def on_checkbutton_toggled(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        if self.checkbutton.get_active() == True:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('seta r_fullscreen "'):
                    line = 'seta r_fullscreen "1"\n'
                sys.stdout.write(line)
            shutil.copy(configfile, configdir + '/autoexec_sp.cfg')

        else:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('seta r_fullscreen "'):
                    line = 'seta r_fullscreen "0"\n'
                sys.stdout.write(line)
            shutil.copy(configfile, configdir + '/autoexec_sp.cfg')

    def on_checkbutton2_toggled(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        if self.checkbutton2.get_active() == True:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('seta r_noborder "'):
                    line = 'seta r_noborder "1"\n'
                sys.stdout.write(line)
            shutil.copy(configfile, configdir + '/autoexec_sp.cfg')

        else:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('seta r_noborder "'):
                    line = 'seta r_noborder "0"\n'
                sys.stdout.write(line)
            shutil.copy(configfile, configdir + '/autoexec_sp.cfg')

    def on_modlist_changed(self, widget):
        sound_start = pygame.mixer.Sound(resourcedir + '/click.WAV')
        sound_start.play()
        model = widget.get_model()
        active = widget.get_active()
        if active == 0:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('#mod "'):
                    line = '#mod "0"\n'
                sys.stdout.write(line)

        if active == 1:
            for line in fileinput.FileInput(configfile, inplace=True):
                if line.strip().startswith('#mod "'):
                    line = '#mod "1"\n'
                sys.stdout.write(line)
            self.modlist.set_active(1)

        if active == 2:
            system(gamedir + '/openjk.i386 +set fs_game MBII')

    def on_install_clicked(self, widget):
        install(self)

    def on_ok_clicked(self, widget):
        self.messagedialog.hide()

    def on_ok2_clicked(self, widget):
        self.errordialog.hide()


def main():
    def gtk_style():
        css = b"""
button:hover {
    background-image: none;
    background-color: transparent;
    transition: 400ms linear;
    border-right-color: #91a8d0;
    border-left-color: #91a8d0;
    border-top-color: #91a8d0;
    border-bottom-color: #91a8d0;
    border-radius: 10px;
    box-shadow: 0 0 10px #333 inset;
}   

window button{
   background-image: none;
   background-color: transparent;
   
   font-size: 11px;
   color: white;
}




label {
    
    font-size: 11px;
    color: white;
}

comboboxtext{
	background-image: none;
	background-color: transparent;
	border-color: transparent;
	color:black
   
}
combotextbox:active{
	background-image: none;
	background-color: transparent;
	border-color: transparent;

   
}

messagedialog {
	background-color: 	#696969;
	color:black
}
messagedialog button {
	background-image: none;
   	background-color: transparent;
   
   font-size: 11px;
   color: white;
}
dialog label{
color:black
}
dialog button{
background-color: 	#696969;
color:black

}
	"""
        # Load the css file for glade
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(resourcedir+"/style.css")
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

    app = launcher()
    gtk_style()
    sound_launch = pygame.mixer.Sound(resourcedir + '/open.WAV')
    sound_launch.play()
    Gtk.main()


if __name__ == '__main__':
    main()
