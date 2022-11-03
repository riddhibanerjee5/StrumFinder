import board

arr = list()
# get wav file as array for numpy
with open('input.txt') as f:
    arr = f.readlines()
    arr = [int(data) for data in arr]
    arr = arr[:] * 5

try: 
    f = open('output.txt', 'x')
    arr = [str(data) for data in arr]
    for data in arr:
        f.write(data + "\n")
    f.close()
except OSError:
    print('error!')
    f.close()
        
print('done!')

