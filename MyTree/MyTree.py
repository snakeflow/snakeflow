#-*- coding: utf-8 -*-

class Node(object):
    def __init__(self, key = None, value = None):
        self.__key = key
        self.__value = value
        self.parent = None
        self.children = []

    def isroot(self):
        if self.parent is None:
            return True
        else:
            return False

    def isleaf(self):
        if self.children == []:
            return True
        else:
            return False

    def key(self):
        return self.__key

    def set_key(self,key):
        self.__key = key

    def value(self):
        return self.__value

    def set_value(self,value):
        self.__value = value

    def children_names(self):
        if self.children != []:
            l = []
            for n in self.children:
                l.append(n.key())
            return l
        else:
            return None

    def parent_name(self):
        if self.parent is not None:
            return self.parent.key()
        else:
            return None

    def set_parent(self,parent):
        self.parent = parent
        parent.add_children(self)

    def set_children(self,children):
        self.children = []
        for c in children:
            self.add_children(c)

    def add_children(self,node):
        node.parent = self
        if self.children_names():
            if node.key() not in self.children_names():
                self.children.append(node)
            else:
                raise ValueError('Existing children name')
        else:
            self.children.append(node)

    def __str__(self):
        parentname = str(self.parent_name())
        childrennames = str(self.children_names())
        return '[key]: %s\n[value]: %s\n[parent]: %s\n[children]: %s' %(self.__key,self.__value,parentname,childrennames)

class Tree(object):
    def __init__(self, adict = None):
        self.__root = None
        self.__curnode = self.__root
        if adict and adict != []:
            self.__root = Node(key = '__ROOT__')
            for item in sorted(adict.items(),key=lambda x:x[0]):
                itemnode = Node(key = item[0])
                self.__root.add_children(itemnode)
                if isinstance(item[1],dict):
                    subtree = Tree(item[1])
                    subtree.set_root(itemnode)
                else:
                    itemnode.set_value(item[1])

    def depth(self,node):
        i = 0
        while node.parent is not None:
            i+=1
            node = node.parent
        return i

    def add(self, key, value):
        node = Node(key=key,value=value)
        self.__curnode.add_children(node)

    def setofleaves(self):
        body = self.mlr_travel()
        returnset = set()
        for node in body:
            if node.isleaf():
                returnset.add(node.key())
        return returnset

    def setofsubroot(self):
        body = self.mlr_travel()
        returnset = set()
        for node in body:
            pn = node.parent_name()
            if pn is not None and pn == '__ROOT__':
                returnset.add(node.key())
        return returnset

    def rootchildren(self):
        return self.__root.children

    def set_root(self, node):
        for child in self.rootchildren():
            node.add_children(child)
        self.__root = node

    def travel(self):
        if self.__root is None:
            return None
        queue = [self.__root]
        returnqueue = [self.__root]
        while queue:
            pointer = queue.pop(0)
            if pointer.children != []:
                queue.extend(pointer.children)
                returnqueue.extend(pointer.children)
        return returnqueue

    def mlr_travel(self):
        if self.__root is None:
            return None
        queue = [self.__root]
        returnqueue = []
        #c = []
        while queue:
            pointer = queue.pop(0)
            returnqueue.append(pointer)
            #c.append(pointer.key())
            if pointer.children != []:
                order = pointer.children
                order.reverse()
                for child in order:
                    queue.insert(0,child)
        #print c
        return returnqueue

    def __str__(self):
        returnstr = ''
        body = self.mlr_travel()
        if body is not None:
            for x in body:
                if x.parent is not None:
                    tstr = ''
                    ustr = '_'
                    parent_depth = self.depth(x.parent)
                    if x.parent.key() != '__ROOT__':
                        #parent_length = len(x.parent.key())
                        tstr = '|'
                    else:
                        parent_length = 1
                    for i in range(parent_depth):
                        tstr += '\t'
                    #for j in range(parent_length):
                        #ustr += '_'
                    if x.value():
                        value = ' : '+str(x.value())
                    else:
                        value = ''
                    returnstr += tstr+'|'+ustr+x.key()+value+'\n'
                else:
                    returnstr += '*\n'
        return returnstr


if __name__ == '__main__':
    a = {'Anhui': {'Other_babyformula': {'test':{'test':119518.0}}, 'Non_food': 69688.0, 'Baby_formula ': 311698.0, 'Adult_milkpowder': 53432.0, 'Bellamy': 75368.0, 'Health_supplements': 85082.0, 'Fruit': 48.0, 'Baby_food': 15866.0, 'A2': 620.0, 'Other_food ': 18466.0, 'Aptamil ': 116192.0, 'OTC_med': 3562.0, 'Milk_powder': 365108.0, 'Wine': 474.0}, 'Tianjin': {'Non_food': 58890.0, 'Other_babyformula': 29546.0, 'Baby_formula ': 84598.0, 'Adult_milkpowder': 20296.0, 'Bellamy': 14466.0, 'Health_supplements': 78108.0, 'Baby_food': 7414.0, 'Fruit': 130.0, 'Other_food ': 29516.0, 'Aptamil ': 40486.0, 'OTC_med': 3446.0, 'Milk_powder': 104892.0, 'A2': 100.0, 'Wine': 156.0}, 'Hongkong': {'Non_food': 84.0, 'Other_babyformula': 6.0, 'Baby_formula ': 54.0, 'Adult_milkpowder': 6.0, 'Health_supplements': 46.0, 'Aptamil ': 48.0, 'OTC_med': 8.0, 'Milk_powder': 60.0}, 'Shanghai': {'Other_babyformula': 206328.0, 'Non_food': 212796.0, 'Baby_formula ': 513352.0, 'Adult_milkpowder': 120022.0, 'Bellamy': 71948.0, 'Health_supplements': 253798.0, 'Fruit': 208.0, 'Baby_food': 44726.0, 'A2': 982.0, 'Other_food ': 72194.0, 'Aptamil ': 234094.0, 'OTC_med': 11844.0, 'Milk_powder': 633352.0, 'Wine': 1086.0}, 'Inner Mongoila': {'Other_babyformula': 13812.0, 'Non_food': 29594.0, 'Baby_formula ': 34980.0, 'Adult_milkpowder': 4388.0, 'Bellamy': 5070.0, 'Health_supplements': 38000.0, 'Fruit': 30.0, 'Baby_food': 4816.0, 'A2': 48.0, 'Other_food ': 7568.0, 'Aptamil ': 16050.0, 'OTC_med': 1286.0, 'Milk_powder': 39368.0, 'Wine': 108.0}, 'Gansu': {'Other_babyformula': 17956.0, 'Non_food': 13522.0, 'Baby_formula ': 42888.0, 'Adult_milkpowder': 4192.0, 'Bellamy': 6342.0, 'Health_supplements': 15860.0, 'Fruit': 10.0, 'Baby_food': 3014.0, 'A2': 74.0, 'Other_food ': 3922.0, 'Aptamil ': 18516.0, 'OTC_med': 536.0, 'Milk_powder': 47080.0, 'Wine': 42.0}, 'Jiangsu': {'Other_babyformula': 388254.0, 'Non_food': 283374.0, 'Baby_formula ': 858000.0, 'Adult_milkpowder': 114638.0, 'Bellamy': 143300.0, 'Health_supplements': 334020.0, 'Fruit': 276.0, 'Baby_food': 81050.0, 'A2': 2156.0, 'Other_food ': 65192.0, 'Aptamil ': 324290.0, 'OTC_med': 15288.0, 'Milk_powder': 972584.0, 'Wine': 2160.0}, 'Hainan': {'Non_food': 22482.0, 'Bellamy': 36542.0, 'Other_babyformula': 57254.0, 'Baby_formula ': 155322.0, 'Adult_milkpowder': 35872.0, 'Health_supplements': 30208.0, 'Fruit': 22.0, 'Baby_food': 5996.0, 'A2': 124.0, 'Other_food ': 6452.0, 'Aptamil ': 61402.0, 'OTC_med': 1486.0, 'Milk_powder': 191180.0, 'Wine': 352.0}, 'Tibet': {'Non_food': 1490.0, 'Other_babyformula': 1374.0, 'OTC_med': 70.0, 'Adult_milkpowder': 484.0, 'Bellamy': 224.0, 'Health_supplements': 1524.0, 'Baby_food': 98.0, 'Other_food ': 478.0, 'Aptamil ': 584.0, 'Baby_formula ': 2182.0, 'Milk_powder': 2666.0, 'Wine': 4.0}, 'Yunnan': {'Non_food': 38448.0, 'Other_babyformula': 55128.0, 'Baby_formula ': 115310.0, 'Adult_milkpowder': 14436.0, 'Bellamy': 24704.0, 'Health_supplements': 48710.0, 'Fruit': 54.0, 'Baby_food': 8742.0, 'A2': 282.0, 'Other_food ': 13500.0, 'Aptamil ': 35196.0, 'OTC_med': 2218.0, 'Milk_powder': 129738.0, 'Wine': 106.0}, 'Hubei': {'Non_food': 103912.0, 'Other_babyformula': 154762.0, 'Baby_formula ': 388348.0, 'Adult_milkpowder': 57422.0, 'Bellamy': 56470.0, 'Health_supplements': 129764.0, 'Fruit': 86.0, 'Baby_food': 20646.0, 'A2': 946.0, 'Other_food ': 24810.0, 'Aptamil ': 176170.0, 'OTC_med': 4980.0, 'Milk_powder': 445782.0, 'Wine': 1916.0}, 'Zhejiang': {'Other_babyformula': 372828.0, 'Bellamy': 138868.0, 'Baby_formula ': 840198.0, 'Adult_milkpowder': 96782.0, 'Health_supplements': 305692.0, 'Fruit': 122.0, 'Baby_food': 69826.0, 'A2': 2354.0, 'Other_food ': 52650.0, 'Aptamil ': 326148.0, 'OTC_med': 12432.0, 'Milk_powder': 936976.0, 'Non_food': 221568.0, 'Wine': 1220.0}, 'Na': {'Non_food': 10.0, 'Other_babyformula': 12.0, 'Milk_powder': 18.0, 'Baby_formula ': 12.0, 'Adult_milkpowder': 6.0}, 'Heilongjiang': {'Non_food': 65770.0, 'Other_babyformula': 21238.0, 'Baby_formula ': 50442.0, 'Adult_milkpowder': 11836.0, 'Bellamy': 6552.0, 'Health_supplements': 101976.0, 'Baby_food': 12392.0, 'Fruit': 74.0, 'Other_food ': 20116.0, 'Aptamil ': 22546.0, 'OTC_med': 2438.0, 'Milk_powder': 62300.0, 'A2': 106.0, 'Wine': 878.0}, 'Fujian': {'Other_babyformula': 290890.0, 'Bellamy': 124718.0, 'Baby_formula ': 885504.0, 'Adult_milkpowder': 169650.0, 'Health_supplements': 292946.0, 'Fruit': 186.0, 'Baby_food': 70740.0, 'A2': 1506.0, 'Other_food ': 51848.0, 'Aptamil ': 468390.0, 'OTC_med': 13716.0, 'Milk_powder': 1055682.0, 'Non_food': 215138.0, 'Wine': 690.0}, 'Chongqing': {'Other_babyformula': 109782.0, 'Non_food': 49130.0, 'Baby_formula ': 241848.0, 'Adult_milkpowder': 27750.0, 'Bellamy': 53708.0, 'Health_supplements': 60808.0, 'Fruit': 48.0, 'Baby_food': 7302.0, 'A2': 844.0, 'Other_food ': 11512.0, 'Aptamil ': 77514.0, 'OTC_med': 2426.0, 'Milk_powder': 269640.0, 'Wine': 464.0}, 'Xinjiang': {'Non_food': 37192.0, 'Other_babyformula': 22078.0, 'Baby_formula ': 53712.0, 'Adult_milkpowder': 3638.0, 'Bellamy': 8062.0, 'Health_supplements': 50328.0, 'Fruit': 20.0, 'Baby_food': 4280.0, 'A2': 102.0, 'Other_food ': 8370.0, 'Aptamil ': 23470.0, 'OTC_med': 1868.0, 'Milk_powder': 57342.0, 'Wine': 72.0}, 'Shaanxi': {'Other_babyformula': 71190.0, 'Bellamy': 29614.0, 'Baby_formula ': 176390.0, 'Adult_milkpowder': 15060.0, 'Health_supplements': 66592.0, 'Fruit': 66.0, 'Baby_food': 8526.0, 'A2': 334.0, 'Other_food ': 12162.0, 'Aptamil ': 75252.0, 'OTC_med': 2106.0, 'Milk_powder': 191454.0, 'Non_food': 50882.0, 'Wine': 446.0}, 'Hebei': {'Non_food': 90190.0, 'Bellamy': 24734.0, 'OTC_med': 4260.0, 'Baby_formula ': 139818.0, 'Adult_milkpowder': 24530.0, 'Health_supplements': 113818.0, 'Fruit': 144.0, 'Baby_food': 13258.0, 'A2': 184.0, 'Other_babyformula': 50216.0, 'Aptamil ': 64684.0, 'Other_food ': 22358.0, 'Milk_powder': 164314.0, 'Wine': 732.0}, 'Henan': {'Non_food': 86464.0, 'Bellamy': 47698.0, 'OTC_med': 3842.0, 'Adult_milkpowder': 28702.0, 'Health_supplements': 116416.0, 'Fruit': 98.0, 'Baby_food': 15654.0, 'A2': 458.0, 'Other_babyformula': 105838.0, 'Aptamil ': 115218.0, 'Baby_formula ': 269212.0, 'Other_food ': 21872.0, 'Milk_powder': 297890.0, 'Wine': 598.0}, 'Guizhou': {'Other_babyformula': 74746.0, 'Bellamy': 32484.0, 'Baby_formula ': 161430.0, 'Adult_milkpowder': 18266.0, 'Health_supplements': 43276.0, 'Fruit': 26.0, 'Baby_food': 9824.0, 'A2': 266.0, 'Other_food ': 8970.0, 'Aptamil ': 53934.0, 'OTC_med': 2332.0, 'Milk_powder': 179660.0, 'Non_food': 34396.0, 'Wine': 212.0}, 'Chengdu': {'Other_babyformula': 6.0, 'Milk_powder': 12.0, 'Baby_formula ': 12.0, 'Bellamy': 6.0}, 'Jiangxi': {'Other_babyformula': 98044.0, 'Non_food': 45094.0, 'Baby_formula ': 277904.0, 'Adult_milkpowder': 54484.0, 'Bellamy': 47998.0, 'Health_supplements': 57318.0, 'Fruit': 38.0, 'Baby_food': 16880.0, 'A2': 522.0, 'Other_food ': 11204.0, 'Aptamil ': 131340.0, 'OTC_med': 2288.0, 'Milk_powder': 332340.0, 'Wine': 390.0}, 'Beijing': {'Other_babyformula': 103214.0, 'Bellamy': 38906.0, 'Baby_formula ': 268828.0, 'Adult_milkpowder': 34266.0, 'Health_supplements': 184282.0, 'Baby_food': 28478.0, 'Fruit': 260.0, 'Other_food ': 47958.0, 'Aptamil ': 126270.0, 'OTC_med': 7892.0, 'Milk_powder': 303084.0, 'A2': 438.0, 'Non_food': 181132.0, 'Wine': 968.0}, 'Shandong': {'Non_food': 183084.0, 'Other_babyformula': 171834.0, 'Baby_formula ': 413346.0, 'Adult_milkpowder': 67086.0, 'Bellamy': 89738.0, 'Health_supplements': 263336.0, 'Fruit': 152.0, 'Baby_food': 41974.0, 'A2': 930.0, 'Other_food ': 49148.0, 'Aptamil ': 150844.0, 'OTC_med': 9936.0, 'Milk_powder': 480502.0, 'Wine': 1116.0}, 'Hunan': {'Other_babyformula': 154472.0, 'Bellamy': 86024.0, 'Baby_formula ': 418296.0, 'Adult_milkpowder': 87456.0, 'Health_supplements': 115932.0, 'Baby_food': 20110.0, 'Fruit': 78.0, 'Other_food ': 19560.0, 'Aptamil ': 177224.0, 'OTC_med': 4080.0, 'Milk_powder': 505660.0, 'A2': 576.0, 'Non_food': 82760.0, 'Wine': 806.0}, 'Guangxi': {'Non_food': 46004.0, 'Other_babyformula': 105050.0, 'Baby_formula ': 280644.0, 'Adult_milkpowder': 56502.0, 'Bellamy': 70540.0, 'Health_supplements': 60078.0, 'Fruit': 56.0, 'Baby_food': 8920.0, 'A2': 284.0, 'Other_food ': 10324.0, 'Aptamil ': 104770.0, 'OTC_med': 2368.0, 'Milk_powder': 337146.0, 'Wine': 500.0}, 'Qinghai': {'Other_babyformula': 3644.0, 'Non_food': 4424.0, 'Baby_formula ': 7868.0, 'Adult_milkpowder': 702.0, 'Bellamy': 1482.0, 'Health_supplements': 4450.0, 'Fruit': 2.0, 'Baby_food': 782.0, 'A2': 12.0, 'Other_food ': 1006.0, 'Aptamil ': 2730.0, 'OTC_med': 130.0, 'Milk_powder': 8570.0, 'Wine': 44.0}, 'Ningxia': {'Non_food': 5162.0, 'Bellamy': 4236.0, 'OTC_med': 172.0, 'Baby_formula ': 20544.0, 'Adult_milkpowder': 1044.0, 'Health_supplements': 7430.0, 'Fruit': 2.0, 'Baby_food': 924.0, 'A2': 48.0, 'Other_babyformula': 8540.0, 'Aptamil ': 7720.0, 'Other_food ': 1266.0, 'Milk_powder': 21588.0, 'Wine': 772.0}, 'Sichuan': {'Non_food': 114946.0, 'Bellamy': 126876.0, 'Baby_formula ': 569244.0, 'Adult_milkpowder': 98656.0, 'Health_supplements': 143256.0, 'Fruit': 130.0, 'Baby_food': 19436.0, 'A2': 1414.0, 'Other_babyformula': 266016.0, 'Aptamil ': 174938.0, 'OTC_med': 5166.0, 'Other_food ': 28390.0, 'Milk_powder': 667888.0, 'Wine': 1158.0}, 'Liaoning': {'Non_food': 146552.0, 'Other_babyformula': 89918.0, 'Baby_formula ': 249852.0, 'Adult_milkpowder': 35522.0, 'Bellamy': 43030.0, 'Health_supplements': 208396.0, 'Fruit': 214.0, 'Baby_food': 22420.0, 'A2': 470.0, 'Other_food ': 41074.0, 'Aptamil ': 116434.0, 'OTC_med': 8182.0, 'Milk_powder': 285348.0, 'Wine': 888.0}, 'Taiwan': {'Non_food': 2.0}, 'Guangdong': {'Non_food': 396090.0, 'Other_babyformula': 565040.0, 'OTC_med': 24948.0, 'Adult_milkpowder': 249466.0, 'Bellamy': 197072.0, 'Health_supplements': 492252.0, 'Fruit': 426.0, 'Baby_food': 68690.0, 'A2': 4174.0, 'Other_food ': 92604.0, 'Aptamil ': 772244.0, 'Baby_formula ': 1538530.0, 'Milk_powder': 1787912.0, 'Wine': 3510.0}, 'Jilin': {'Other_babyformula': 32936.0, 'Non_food': 51058.0, 'Baby_formula ': 88274.0, 'Adult_milkpowder': 12630.0, 'Bellamy': 17250.0, 'Health_supplements': 81512.0, 'Baby_food': 7478.0, 'Fruit': 18.0, 'Other_food ': 15344.0, 'Aptamil ': 37962.0, 'OTC_med': 2198.0, 'Milk_powder': 100904.0, 'A2': 126.0, 'Wine': 230.0}, 'Shanxi': {'Other_babyformula': 33252.0, 'Non_food': 33670.0, 'Baby_formula ': 87684.0, 'Adult_milkpowder': 12786.0, 'Bellamy': 15324.0, 'Health_supplements': 48814.0, 'Baby_food': 5834.0, 'Fruit': 18.0, 'Other_food ': 8768.0, 'Aptamil ': 38874.0, 'OTC_med': 1392.0, 'Milk_powder': 100470.0, 'A2': 234.0, 'Wine': 240.0}}
    print Tree(a).setofsubroot()