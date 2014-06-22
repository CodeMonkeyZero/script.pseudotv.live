# Autoupdate Module By: Blazetamer 2013#
########################################

import urllib,urllib2
import xbmcplugin,xbmcgui,xbmc,xbmcaddon,xbmcvfs
import re,os,sys,time,shutil
import downloader, extract
from addon.common.addon import Addon
from addon.common.net import Net
from resources.lib.Globals import *
from resources.lib.FileAccess import *

net = Net()
__settings__   = xbmcaddon.Addon(id='script.pseudotv.live')
__cwd__        = __settings__.getAddonInfo('path')


def UPDATEFILES():
    ADDON = os.path.split(__cwd__)[1]
    xbmc.log('script.pseudotv.live-autoupdate: UPDATEFILES')
    xbmc.log('script.pseudotv.live-autoupdate: Version = ' + ADDON)
    
    url = ''
    name = ''
    changelog = 'https://raw.githubusercontent.com/Lunatixz/script.pseudotv.live/master/changelog.txt'         
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    addonpath = xbmc.translatePath(os.path.join('special://','home/addons'))
    lib = os.path.join(path,name)
    
    if ADDON == 'script.pseudotv.live-Hub-Edition':
        url='https://github.com/Lunatixz/script.pseudotv.live/archive/Hub-Edition.zip'
        name = 'script.pseudotv.live-Hub-Edition.zip' 
    else:
        url='https://github.com/Lunatixz/script.pseudotv.live/archive/master.zip'
        name = 'script.pseudotv.live-master.zip'    
    
    xbmc.log('script.pseudotv.live-autoupdate: URL = ' + url)
    
    response = urllib2.urlopen(changelog)
    changeTXT = response.read()
    xbmc.log('script.pseudotv.live-autoupdate: ChangeTXT Init')
    
    try: 
        os.remove(lib)
        xbmc.log('script.pseudotv.live-autoupdate: deleted old package')
    except: 
        pass
         
    downloader.download(url, lib, '')
    xbmc.log('script.pseudotv.live-autoupdate: downloaded new package')
    extract.all(lib,addonpath,'')
    xbmc.log('script.pseudotv.live-autoupdate: extracted new package')
        
    xbmc.executebuiltin("RunScript("+__cwd__+"/videowindow.py,-autopatch)")
    xbmc.executebuiltin("RunScript("+__cwd__+"/donordownload.py,-autopatch)")
    xbmc.executebuiltin("UpdateLocalAddons")
    MSG = 'Update Complete'
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("PseudoTV Live", MSG, 2000, THUMB) ) 
    dialog = xbmcgui.Dialog()   
    dialog.ok("PseudoTV Live - Change Log", changeTXT)    
    return
        