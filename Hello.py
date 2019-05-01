# return (1+2+3.....+x)
def function_a(x):
    a = 0
    ret = 0
    while a < 30:
        a = a+1
        ret = ret+a
    return ret

# return (1*2*3.....*x)
def function_b(x):
    a = 0
    ret = 1
    while a < x:
        a = a+1
        ret = ret*a
    return ret

# return [1, 0, 1, 0, 1, 0....1, 0]
def odd_positive(arr):
    a = 0
    while a < len(arr):
        a = a+1
        b = a % 2
        c = a-1
        if b > 0:
            arr[c] = 1
        else:
            arr[c] = 0
            
# return [1, 0, 3, 0, 5, 0, 7......0, N]
def odd_increasing(arr):
#     for a in range(len(arr)):
#         a = a+1
#         b = a%2
#         c = a-1
#         if b > 0:
#             arr[c] = a
#         else:
#             arr[c] = 0
    for i in range(len(arr)):
        if i % 2 == 0:
            arr[i] = 0
        else:
            arr[i] = i
        
            
# return the boolean that whether the snake hits the walls or not
# def hit_the_walls(table, x, y):
    
# this funcion access array in-place, no return value

if __name__ == '__main__':
#     ans = function_b(6) - function_a(30)*function_b(3)
#     print(ans)
    
#     arr = [0]*23
#     odd_positive(arr)
#     print(arr)
#     
#     a = 0
#     while a < 10:
#         b = a%2
#         print(a, b)
#         a = a+1
# #  
#     print('====================')
#     for a in range(10):
#         b = a%2
#         print(a, b)
    
    
    arr = [0]*23
    odd_increasing(arr)
    print(arr)
#     width = 10
#     height = 10
    
#     table = [
                 




