
"""
 __   __   ___    _   _    ___              ___     ___    _____    ___      _
 \ \ / /  / _ \  | | | |  | _ \            |   \   /   \  |_   _|  /   \    | |
  \ V /  | (_) | | |_| |  |   /            | |) |  | - |    | |    | - |    |_|
  _|_|_   \___/   \___/   |_|_\            |___/   |_|_|   _|_|_   |_|_|   _(_)_

    ____                _             _ 
  / ____|              | |           | |  
 | |     _ __ __ _  __ | | __ ___  __| |
 | |    | '__/ _` |/ _`| |/ // _ \/ _  |
 | |____| | | (_| | (_ |   <   __/ (_) |
  \_____|_|  \__,_|\__,|_|\_\\___|\____|

Ci_nk     MIX                 push k times to right in spesific range
ci_nk     MIX                 push k times to left in spesific range
Ri_n      MIX                 sort from back in spesific range
Ki_nt     ADD                 dublicate t times each word in spesific range
Pi_k      DEPRECATED          add i_ for all mod k
Dt_k      ADD  TODO           dublicate t times for all mod k
Ai_k      MIX  TODO           tooks range from oposite and sort back
Si_n      DEPRECATED          swap with oposite in spesific range

"""

import random
import re

class Encrypte:
    def __init__(self):
        super().__init__()
    
    def change(self, index, n, k, left=True):
        t = self.msg[index: n+index]
        for i in range(k): t.insert(len(t)*int(left), t.pop(int(left)-1))
        self.msg = self.msg[:index] + t + self.msg[n+index:]

    def redo_change(self, index, n, k, left=True):
        self.change(index, n, k, not left)

    def reverse(self, index, n):
        t = self.msg[index: index+n]
        i0,i1 = index,index+n-1
        for i in range(len(t)):
            t.insert(len(t)-i-1,t.pop(0))
        self.msg = self.msg[:index] + t + self.msg[n+index:]
        
    # HAVE ADDITION 
    def addEach(self, index, n, k):
        t = self.msg[index: n+index]
        for i in range(0,len(t)*k,k):
            for ii in range(k-1):
                t.insert(i+1, t[i])

        self.msg = self.msg[:index] + t + self.msg[n+index:]
        return True

    def redo_addEach(self, index, n, k):
        t = self.msg[index: n*k+index]
        for i in range(n):
            m = t[i]
            for _ in range(k-1):
                if m != t.pop(i): print("BROKE");return False

        self.msg = self.msg[:index] + t + self.msg[n*k+index:]
        return True
    
    # HAVE ADDITION Archived
    def addMod(self, index, k):
        if 2>k: print("BROKE"); return False

        t = self.msg[index]
        for i in range(0, len(self.msg)+(len(self.msg)//(k-1)), k):
            self.msg.insert(i, "ttt")
    
    def redo_addMod(self, index, k):
        pass

    def ordinary(self, unlock=False):
        self.key = [ord(i) for i in self.key]
            

class Lock(Encrypte):
    def __init__(self):
        self.key=None
        self.msg=None

    # check key is true and "update the key" return false if key broken
    def reKey(self):
        key = list(self.key)+list("z0")
        self.key = [[key.pop(0)]]

        while match:=re.search('[a-zA-Z]', "".join(key)):
            for _ in range(match.start()): self.key[-1].append(key.pop(0))

            ottr = "".join(self.key[-1][1:])
            regx = '^[0-9][0-9]+$' if self.key[-1][0] in ["R","P","D","S"] else '^[0-9][0-9][0-9]+$' if ["K","C","c"] else f"{random.random()}"
            if not re.search(regx, ottr): return False

            self.key.append([key.pop(0)])
        self.key.pop()
        return True
            
    # create key and crypted_msg from msg and "save the key" return key
    def generateKey(self):
        self.msg = list(self.msg)
        regedits = ["^C.+[0-9][0-9]$","^c.+[0-9][0-9]$","^K.+[0-9][0-9]$","^R.+[0-9]$"]
        regs = ["C","c","K","R"]

        self.key = "".join([ regs[p:=random.randint(0, len(regedits)-1)] + str(random.randint(0, len(self.msg))) + str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9))*(p==3)  for i in range(random.randint(len(self.msg) // 2, len(self.msg)))])
        
        return self.key
    
    # crack msg with key from crypted_msg and "save the msg" return false if key did'nt matches
    def lockKey(self, unlock=False):
        self.msg = list(self.msg)

        for key in [self.key,  [self.key[len(self.key)-k-1] for k in range(len(self.key))]][int(unlock)]:
            if key[0] in ["C", "c"]:
                i_= int("".join(key[1:-2]))
                n = int(key[-2])
                k = int(key[-1])
                left = key[0] == "c"
                
                # if i_ + n  > len(self.msg):return False
                [self.change, self.redo_change][int(unlock)](i_, n, k, left)

            elif key[0] == "R":
                i_= int("".join(key[1:-1]))
                n = int(key[-1])
                self.reverse(i_, n)

            elif key[0] == "K":
                i_= int("".join(key[1:-2]))
                n = int(key[-2])
                k = int(key[-1])
                if not [self.addEach, self.redo_addEach][int(unlock)](i_, n, k):return False

            # elif key[0] == "P":
            #     i_= int("".join(key[1:-1]))
            #     k = int(key[-1])
            #     if not [self.addMod, self.redo_addMod][int(unlock)](i_, k):return False
        return True

