#!/usr/bin/python

import steamodd as steam
import thread
import threading
import time
import string
import ConfigParser
import os, sys

class DropThread(threading.Thread):
    def __init__(self, steamId):
        threading.Thread.__init__(self)
        self.steamId = steamId
        self.lastId = None
        self.schema = None
        self.threadKeepAlive = True
        self.pollMinutes = options.pollMinutes
        
    def run(self):
        while self.threadKeepAlive:
            try:
                newestItems = self.get_newest_items()
                if newestItems is None:
                    continue
                
                for i in newestItems:
                    item = Item()
                    item.account = self.steamId
                    itemname = i.get_name()
                    item.name = itemname
                    item.id = str(i.get_id())
                    #item.time = time.strftime('%d/%m/%y %H:%M', time.localtime(time.time()))
                    item.time = time.strftime('%d/%m/%y %H:%M', time.localtime(time.time()+28800))
                    material = i.get_craft_material_type()
                    
                    if material != None:
                        if material == 'supply_crate':
                            # Stick crate series on end of crate item name
                            if itemname == 'Mann Co. Supply Crate':
                                crateseries = str(int(i.get_attributes()[0].get_value()))
                                item.name = itemname + ' #' + crateseries
                            material = 'crate'
                        elif material == 'hat':
                            if i.get_slot() == 'misc':
                                material = 'misc'
                    else:
                        slot = i.get_slot()
                        class_ = i.get_class()
                        if slot == 'head':
                            material = 'hat'
                        elif slot == 'misc':
                            material = 'misc'
                        elif slot == 'primary' or slot == 'secondary' or slot == 'melee' or slot == 'pda2':
                                material = 'weapon'
                        elif class_ == 'supply_crate':
                                # Stick crate series on end of crate item name
                                if itemname == 'Mann Co. Supply Crate':
                                        crateseries = str(int(i.get_attributes()[0].get_value()))
                                        item.name = itemname + ' #' + crateseries
                                material = 'crate'
                        elif class_ == 'tool' or slot == 'action' or class_ == 'craft_item':
                                material = 'tool'
                        else:
                                # Catch all
                                material = 'tool'
                    item.material = material
                    
                    self.dropEvent(item)
                    
                timer = 0
                while self.threadKeepAlive and timer < self.pollMinutes: 
                    time.sleep(60)
                    timer += 1
            except Exception as e:
                print 'DropThread Error:', e


    def get_newest_items(self):
        try:
            backpack = steam.tf2.backpack(self.steamId)
        except Exception as e:
            #print 'Error getting newest items: ', e
            return None
        if self.lastId is None:
            self.lastId = 0
            for item in backpack:
                if item.get_id() > self.lastId:
                    self.lastId = item.get_id()
            return []
        else:
            newestItems = []
            for item in backpack:
                if item.get_id() > self.lastId and item.get_id() == item.get_original_id():
                #if item.get_id() > self.lastId:
                    newestItems.append(item)
            if len(newestItems) != 0:
                self.lastId = max([item.get_id() for item in newestItems])
            return newestItems
            
    def dropEvent(self, item):
        log.log(item)

class Item:
    def __init__(self):
        self.name = ''
        self.itemId = ''
        self.account = ''
        self.material = ''
        self.time = None
        
class Options:
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.accounts = []
        self.apiKey = ''
        self.pollMinutes = 1
        self.logging = 0
        self.htmldir = ''
        self.get_config_options()

    def get_config_options(self):
        try:
            self.conf.read(os.path.join(os.path.dirname(sys.argv[0]), 'TF2DropMonitor.ini'))
            self.accounts = self.conf.get('General', 'accounts').split(',')
            self.apiKey = self.conf.get('General', 'api_key')
            self.pollMinutes = int(self.conf.get('General', 'poll_minutes'))
            self.logging = int(self.conf.get('General', 'logging'))
            self.htmldir = self.conf.get('General', 'html_dir')
        except Exception as e:
            print 'Options Error:', e
            return

class Log:
    def __init__(self):
        self.logfile = os.path.join(os.path.dirname(sys.argv[0]), 'TF2DropMonitor.log')
        self.enabled = 0


    def log(self, item):
        if self.enabled:
            msg = '%s  | %s | %s | %s' %(item.time,
                                string.ljust(item.account, 12),
                                string.ljust(item.material, 6),
                                item.name)
            print msg
            self.log_html(item)
            with open(self.logfile, 'a') as f:
                f.write(msg + '\r\n')

    def log_html(self, item):
        row = self.construct_row(item)
        row = '%s\n<!--APPENDROWHERE-->' % row
        htmlfilepath = os.path.join(options.htmldir, 'index.html')
        try:
            with open(htmlfilepath, 'r') as f:
                content = f.read()
                newContent = content.replace('<!--APPENDROWHERE-->', row)
            with open(htmlfilepath, 'w') as f:
                f.write(newContent)
        except:
            pass

    def construct_row(self, item):
        template = '<tr><td class="noborder"></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
        templateHat = '<tr class="hat-highlight"><td class="noborder">></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
        if item.material.lower() in ['hat', 'misc']:
            template = templateHat
        row = template % (item.time, item.account, item.material.capitalize(), item.name)
        return row

if __name__ == '__main__':
    options = Options()
    
    steam.base.set_api_key(options.apiKey)
    global log
    log = Log()
    if options.logging == 1:
        log.enabled = 1
    
    for acc in options.accounts:
        t = DropThread(acc)
        t.start()
        print 'Initialized drop monitor for', acc
        
    
    print '-'*75
    print '%s  | %s | %s | %s' %(string.ljust('TIME', 14),
                                string.ljust('ACCOUNT', 12),
                                string.ljust('TYPE', 6),
                                'NAME')
    print '-'*75
