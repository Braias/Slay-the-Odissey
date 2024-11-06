# -*- coding: utf-8 -*-
def is_string_decorator(func):
    print("Estou decorando a função")
    
    def interna(*args, **kwargs):
        for arg in args:
            is_string(arg)
        resultado = func(*args, **kwargs)
        print("Estou executando a função decorada")
        return resultado
        
    return interna

def upper_string(string):
    return string.upper()

def reverse_string(string):
    return string[::-1]

def is_string(string):
    if not isinstance(string, str):
        raise TypeError("Parâmetro deve ser uma string")
        
# reverse_string_decorated = is_string_decorator(reverse_string)
# upper_string_decorated = is_string_decorator(upper_string)

#############

def generator_function_1():
    yield 1
    print("Após 1 e antes do 2")
    yield 2
    print("Após 2 e antes do fim")
    return "Fim da função geradora"

geradora = generator_function_1()
iteradora = geradora.__iter__()

print(geradora.__next__())
print(iteradora.__next__())
print(iteradora.__next__())
    
    