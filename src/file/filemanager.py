class Person:
  def __init__(self, _name, _age):
    self.name = _name
    self.age = _age

  def sayHi(self):
    print('Hello, my name is ' + self.name + ' and I am ' + self.age + ' years old!')
