import steamodd as steam
import thread
import threading
import time
import string
import ConfigParser
import os

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
                    item.time = time.strftime('%d/%m/%y %H:%M', time.localtime(time.time()))
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
                if item.get_id() > self.lastId:
                    newestItems.append(item)
            if len(newestItems) != 0:
                self.lastId = max([item.get_id() for item in newestItems])
            return newestItems
            
    def dropEvent(self, item):
        print '%s  | %s | %s | %s' %(item.time,
                                string.ljust(item.account, 12),
                                string.ljust(item.material, 6),
                                item.name)

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
        self.get_config_options()

    def get_config_options(self):
        try:
            self.conf.read(os.path.join(os.getcwd(), 'TF2DropMonitor.ini'))
            self.accounts = self.conf.get('General', 'accounts').split(',')
            self.apiKey = self.conf.get('General', 'api_key')
            self.pollMinutes = int(self.conf.get('General', 'poll_minutes'))
        except Exception as e:
            print 'Options Error:', e
            return

if __name__ == '__main__':
    options = Options()
    
    steam.base.set_api_key(options.apiKey)
    
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
