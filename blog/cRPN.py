
"""
d[chr(ord('a')+1-1)]=100
>>> d
{'a': 100}

answer= "37+621-*+"
print("式入力")
ipt1=input()
print("a=?")
ipt2=ipt1.replace("a","("+input()+")")
print("b=?")
ipt3=ipt2.replace("b","("+input()+")")
print("c=?")
ipt4=ipt3.replace("c","("+input()+")")
stack = []
buffer = []
#前置記法からツリーへ
INPUTED_TEXT = ipt4
print("test: (3+7)+6*(2-4)")
print(ipt4)
"""
#中置記法から前置記法へ
def infix_to_prefix(INPUTED_TEXT, buffer=[],stack=[]):
    for token in INPUTED_TEXT:
        if token == '(' or token == 'c' or token == 's' or token == 't':
            stack.append(token)
        elif token == ')':
            while len(stack) > 0:
                te = stack.pop()
                if te == '(':
                    break
                else:
                    buffer.append(te)
            if len(stack) > 0:
                if stack[-1] == 'c' or stack[-1] == 's' or stack[-1] == 't':
                    buffer.append(stack.pop())
        elif token == '*' or token == '/':
            while len(stack) > 0:
                if stack[-1] == '*' or stack[-1] == '/':
                    buffer.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '+' or token == '-':
            while len(stack) > 0:
                if stack[-1] == '*' or stack[-1] == '/' or stack[-1] == '+' or stack[-1] == '-':
                    buffer.append(stack.pop())
                else:
                    break
            stack.append(token)
        else:
            buffer.append(token)

    while len(stack) > 0:
        buffer.append(stack.pop())
    return buffer
#print(INPUTED_TEXT)
#print("".join(buffer))
#前置記法から計算結果を出力
def RPN(states,dict):
    '''
    逆ポーランド記法を計算する関数
    '''
    operator = {
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: float(x) / y)
    }
    stack = []
    #print('RPN: %s' % states)
    for index, z  in enumerate(states):
        if z not in operator.keys():
            stack.append(dict[z])
            continue
        y = stack.pop()
        x = stack.pop()
        stack.append(operator[z](x, y))
        #print('%s %s %s =' % (x, z, y))
    #print(stack[0])
    return stack[0]
#print(RPN(change(ipt4)))
