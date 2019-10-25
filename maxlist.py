class MaxList:
    
    def __init__(self, size , cmp):
        self.size = size
        self._items = list() 
        self._cmp = cmp

    def setCmp(self,cmp):
        self._cmp = cmp

    def pushAndReplace(self,item):
        if len(self._items) >= self.size:
            for it in self._items:
                if self._cmp(it, item):
                    #print (item ," is bigger than ", it)
                    self._items.remove(it)
                    self._items.append(item)
                    return
        else:
            self._items.append(item)
    
    def getItems(self):
        return self._items


if __name__ == "__main__":
    maxList = MaxList(3,lambda it, inp : ord(inp) > ord(it))
    maxList.pushAndReplace('a')
    print (maxList.getItems())
    maxList.pushAndReplace('b')
    print (maxList.getItems())
    maxList.pushAndReplace('c')
    print (maxList.getItems())
    maxList.pushAndReplace('d')
    print (maxList.getItems())
    maxList.pushAndReplace('e')
    print (maxList.getItems())

            