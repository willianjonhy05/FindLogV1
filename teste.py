def primo(n):
    if n == 1:
        return False
    for i in range(2, n):
        if(n % i == 0):
            return False
        return True


assert primo(13) == True
assert primo(10) == False
assert primo(2) == True
assert primo(1) == True
print("Todos os testes ok!")