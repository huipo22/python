# -*- coding:utf-8 -*-

# self传参  __init__在实例化时被调用


class AddPerson(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def updateName(self, newName):
        self.name = newName

    def updateAge(self, newAge):
        self.age = newAge

    def updateData(self, newName, newAge):
        self.name = newName
        self.age = newAge


if __name__ == '__main__':
    XiaoMing = AddPerson('Hu XiaoMing', 20)
    print XiaoMing.name, '------', XiaoMing.age
    # XiaoMing.updateName('Li XiaoMing22')
    # XiaoMing.updateAge(50)
    XiaoMing.updateData('Xue rengun', 100)
    print XiaoMing.name, '++++++++++', XiaoMing.age
