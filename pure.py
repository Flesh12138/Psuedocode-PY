'''INTEGER: Whole number. E.g. 9, 16
REAL: A decimal number. E.g. 3.4 or -3.5
CHAR: One character E.g. ‘A’
STRING: A sequences of blanks, letters or words E.g. “Love”, “Today is a lovely day.”, “ “
BOOLEAN: Logical values. E.g. TRUE or FALSE
DATE: Any date in date format. E.g. 03/12/2016
The assignment operator is ← (ID:8592)
'''

#class 代码块
import re

variables={}
reserved_words=['IF', 'ELSE', 'ENDIF', 'WHILE', 'DO', 'ENDWHILE', 'FUNCTION', 'PROCEDURE', 'RETURN', 'DECLARE',
                'NOT', 'STRING', 'INTEGER', 'REAL', 'CHAR', 'BOOLEAN', 'DATE', 'MOD', 'DIV', 'AND', 'OR',
                'INPUT', 'OUTPUT', 'READ', 'WRITE', 'CASE', 'OF', 'ENDCASE', 'ENDPROCEDURE', 'ENDFUNCTION',
                'FOR', 'NEXT', 'TO', 'CALL']
class Variable:
    pass
    def __init__(self,value):
        self.value=value
    def change_value(self):
        pass
class Integer(int,Variable):
    pass
class Real(float,Variable):
    pass
class String(str,Variable):
    def __repr__(self):
        return '"'+self.value+'"'
class Char(Variable): #不能进行加减乘除
    def __repr__(self):
        assert len(self.value)==1
        assert isinstance(self.value,str)
        return "'"+self.value+"'"
Boolean=bool
#......
def variable_name_check(name):
    if not re.match(r'^[a-zA-Z_][0-9a-zA-Z_]*$', name): #以字母或下划线开头，仅有数字下划线和字母
        print("变量名称不符合要求，须以字母或下划线开头，且仅含有数字，下划线和字母")
        return False
    if name in reserved_words:
        print("不能以保留字作为变量名称")
        return False
    return True
def variable_type_recognition(value): #辨认变量类型
    if re.match(r'^-?[0-9]+$', value):
        return 'Integer'
    if len(value) >= 2 and value[0] == value[-1] == '"' and "'" not in value:
        return 'String'
    if len(value) == 3 and value[0] == value[-1] == "'":
        return 'Char'
    if re.match(r'^-?[0-9]+[.][0-9]+$', value):
        return 'Real'
    if value=='True' or value=='False':
        return 'Boolean'
    print('未知数据类型:',value)
    return False
def unindent(lines):
    result=[]
    for i in lines:
        if i[0]=='\t':
            result.append(i[1:])
        else:
            print('不是Tab，无法unindent')
            return False
    return result
def IF_executor(lines):
    print('This is if_exe:',lines)
    condition=sep_expression(lines[0],' ')[1] #WHILE (1==1) THEN
    condition=eval(condition)
    print('condition:',condition)
    print('执行区域:',lines[1:-1])
    if condition:
        compile_lines(unindent(lines[1:-1]))
def WHILE_executor(lines):
    print('This is while_exe:',lines)
    while True:
        condition=sep_expression(lines[0],' ')[1] #WHILE (1==1) THEN
        condition=eval(condition)
        print('condition:',condition)
        print('执行区域:',lines[1:-1])
        if condition:
            compile_lines(unindent(lines[1:-1]))
        else:
            break
def find_pair(word,lines,start): #Accepts iterator for lines
    'Find the pairs in the context(start-end). For example, if word=="IF", it returns the position of "ENDIF"'
    for i in range(start, len(lines)):
        if 'END'+word in lines[i]:
            return i
    return -1
def sep_expression(exp,sep): #以sep分隔，去除每个的后面空格，拒绝''
    result=[]
    for i in exp.split(sep):
        if i!='':
            result.append(i.rstrip()) #去掉右边的空格
    for i in range(1,len(result)): #第二个开始左边的也去掉
        result[i]=result[i].lstrip()
    return result
def compile_lines(lines):
    line_num=0
    while line_num<len(lines):
        # for line_num in range(len(lines)): #废弃：无法实时修改line_num
        #记得删除空格
        line=lines[line_num]
        line=line.rstrip()
        if '=' in line and '=='not in line:
            assignment(lines[line_num])
            line_num+=1
        if 'IF' in line:
            end_sub=find_pair('IF',lines,line_num) #IF 结束序号
            IF_executor(lines[line_num:end_sub+1])
            line_num=end_sub+1
        if 'WHILE' in line:
            end_sub=find_pair('WHILE',lines,line_num) #IF 结束序号
            WHILE_executor(lines[line_num:end_sub+1])
            line_num=end_sub+1
def evaluate(exp): #替换，识别，运算
    for i in variables:
        exp=exp.replace(i,variables[i])
    try:
        return eval(exp)
    except TypeError as e:
        return False
    #DIV,MOD
def assignment(line):
    i = sep_expression(line,'=')
    identifier, value = i[0], i[1]
    print('identifier,value=',identifier,value)
    if variable_name_check(identifier) and variable_type_recognition(value): #Questioned
        global variables
        variables[identifier] = eval(variable_type_recognition(value) + '(' + value + ')')
    else:
        pass


if __name__=='__main__':
    #暂定为读取文件
    with open('p1.txt','r') as file:
        lines=file.read().split('\n') #以\n为分隔符
        compile_lines(lines)
        print(lines)
    print(variables)