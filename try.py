"""
INTEGER: Whole number. E.g. 9, 16
REAL: A decimal number. E.g. 3.4 or -3.5
CHAR: One character E.g. ‘A’
STRING: A sequences of blanks, letters or words E.g. “Love”, “Today is a lovely day.”, “ “
BOOLEAN: Logical values. E.g. TRUE or FALSE
DATE: Any date in date format. E.g. 03/12/2016
The assignment operator is ← (ID:8592)
"""

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
    def __repr__(self): #TODO '''"""'''111 这尼玛这么处理或者就这么算了？？
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
    # print('val',value,type(value))
    if re.match(r'^[+-]?[0-9]+$', value):
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
    condition=' '.join(sep_expression(lines[0],' ')[1:-1]) #WHILE (NOT a/1==1) THEN
    print('条件:',condition)
    condition=evaluate_exp(condition)
    print('条件结果:',condition)
    print('执行区域:',lines[1:-1])
    if condition:
        compile_lines(unindent(lines[1:-1]))
def WHILE_executor(lines):
    print('This is while_exe:',lines)
    while True:
        condition=sep_expression(lines[0],' ')[1] #WHILE (1==1) THEN
        print('条件:', condition)
        condition=evaluate_exp(condition)
        print('条件结果:',condition)
        print('执行区域:',lines[1:-1])
        if condition:
            compile_lines(unindent(lines[1:-1]))
        else:
            break
def find_pair(word,lines,start): #Accepts iterator for lines
    """Find the pairs in the context(start-end). For example, if word=="IF", it returns the position of "ENDIF"""
    for i in range(start, len(lines)):
        if 'END'+word in lines[i]:
            return i
    return -1
def clean_exps(exps): #去除每个的后面空格，拒绝''
    result = []
    for i in exps:
        if i!='' and i!= (' '*len(i)): #不要'','  '之类
            result.append(i.rstrip()) #去掉右边的空格
    for i in range(1,len(result)): #第二个开始左边的也去掉
        result[i]=result[i].lstrip()
    return result
def sep_expression(exp,sep): #以sep分隔，去除每个的后面空格，拒绝''
    return clean_exps(exp.split(sep))
def compile_lines(lines):
    line_num=0
    while line_num<len(lines):
        # for line_num in range(len(lines)): #废弃：无法实时修改line_num
        #记得删除空格
        line=lines[line_num]
        line=line.rstrip()
        if '<-' in line: #and '=='not in line:
            assignment(lines[line_num])
            line_num+=1
        if 'IF' in line:
            end_sub=find_pair('IF',lines,line_num) #IF 结束序号
            IF_executor(lines[line_num:end_sub+1])
            line_num=end_sub+1
        if 'WHILE' in line:
            end_sub=find_pair('WHILE',lines,line_num) #WHILE 结束序号
            print(end_sub)
            WHILE_executor(lines[line_num:end_sub+1])
            line_num=end_sub+1
        print('variables:',variables)
def sep_exps_eval(exp,operators=[]): #以同一级别的运算符分隔
    #还没有考虑括号！
    #TODO 可能有更好地算法
    original=[exp]
    for op in operators:
        result = []
        for ori in original:
            for t in ori.split(op):
                result.append(t)
                result.append(op)
            result=result[:-1]
        original=result
    result=clean_exps(result)
    #选择在这里加入判断是否运算符在括号内
    # eg. ['(1','+','2)*3','+','2'] 5项
    op_positions=[i for i in range(len(result)) if result[i] in operators]
    op_in_bracket_count=0
    print('运算符位置',result,op_positions,operators)
    for i in range(len(op_positions)):
        real_operator_position=i-op_in_bracket_count*2 #每一次都会少2项
        if result[real_operator_position] in operators and op_in_bracket(result[real_operator_position],real_operator_position,result):
            result[i-1:i+2]=[''.join(result[i-1:i+2])]
            op_in_bracket_count+=1
    return result
    # return clean_exps(original)

def evaluate_sinmple_exp(exp):
    pass


def op_in_bracket(op, op_seq, seps):
    """
    seps为分隔列表，op_seq代表是exp中的第op_seq个op
    判断方法：该current_exp之前是否(数量=)数量
    大于则在括号内
    注意op_seq从0开始
    """
    in_bracket=False
    op_count=-1 #记数：遇到了第几个op了(0开始)
    exp_count=0 #记数：第几个表达式包含第op_seq个op(0开始)
    while True:
        if seps[exp_count]==op:
            op_count+=1
        if op_count==op_seq:
            break
        exp_count+=1
    original_exp = ''.join(seps[:exp_count])
    # print(original_exp)
    if original_exp.count('(') > original_exp.count(')'):
        return True
    else:
        return False  # TODO 检验）数量>（数量
print(op_in_bracket('+',0,['(1','+','1)*2']))


def evaluate_exp(exp): #替换，识别，运算
    '''
    1.是否能直接给出答案
    2.代入
    3.分隔
    4.最底层分隔。分割了？
        a)    YES:返回
        b)    NO:再下一层
    '''
    print('evaluate_exp接收到:',exp)
    if exp[0]=='(' and exp[-1]==')':
        exp=exp[1:-1]
    if variable_type_recognition(exp):
        return eval(variable_type_recognition(exp) + '(' + exp + ')')
    for i in variables:
        # exp='('+exp.replace(i,str(variables[i]))+')'
        exp = exp.replace(i, str(variables[i]))
    flag = False
    for ops in [
        [['AND',2],['OR',2],['NOT',1]],
        [['>=',2],['>',2],['<',2],['<=',2],['!=',2],['==',2]],
        [['+',2],['-',2]],
        [['*',2],['/',2],['//',2]]
        #正负号？
    ]:
        if flag==True: #分隔了
            break
        seps = sep_exps_eval(exp, [i[0] for i in ops]) #提取运算符并分隔
        if seps!=[exp]:
            flag=True
        if seps[0]=='+': #单目 （＋－是唯一的双目和单目同一符号，所以当第一个是+-时，和第二项合并）
            seps[0:2]= [seps[0]+seps[1]]
        if seps[0] == '-':  #单目 （＋－是唯一的双目和单目同一符号，所以当第一个是+-时，和第二项合并）
            seps[0:2] = [seps[0]+seps[1]]
        for op in ops: #op:['AND',2(双目运算符)]
            for op_seq in range(seps.count(op[0])):
                if op[1]==1 and op[0] in exp: #处理单目运算符,要求存在该运算符+
                    py_op=op[0].lower()
                    index=seps.index(op[0])
                    replace_str=str(eval('%s evaluate_exp(seps[index+1])'%py_op)) #eval('not 1') -> 'False'
                    seps=seps[:index]+[replace_str]+seps[index+2:]
                    #为了允许多次处理，再次转化为str
                if op[1]==2 and op[0] in exp: #处理双目运算符,要求存在该运算符
                    py_op=op[0].lower()
                    index=seps.index(op[0])
                    replace_str=str(eval('evaluate_exp(seps[index-1]) %s evaluate_exp(seps[index+1])'%py_op)) #eval('1 AND True')
                    seps=seps[:index-1]+[replace_str]+seps[index+2:]
                #也许应该么每次都转化为str，最后再variabe_type_recognition() -> 1+1+1?
    print('输入:',exp,'evaluate_exp的结果是:',seps)
    assert len(seps)==1 #化简后应该只有一个
    result=seps[0]
    if variable_type_recognition(result):
        return eval(variable_type_recognition(result) + '(' + result + ')')
    # return seps[0]

    # try:
    #     return eval(exp)
    # except TypeError as e:
    #     return False
    #DIV,MOD
def assignment(line):
    i = sep_expression(line,'<-')
    identifier, value = i[0], i[1]
    print('identifier=',identifier,'value=',value)
    if variable_name_check(identifier):# and variable_type_recognition(value): #Questioned
        global variables
        variables[identifier] = evaluate_exp(value)
    else:
        pass

# print(evaluate_exp('1<2'))
if __name__=='__main__':
    #暂定为读取文件
    with open('test.txt','r') as file:
        lines=file.read().rstrip().split('\n') #以\n为分隔符
        print('所有行:',lines)
        compile_lines(lines)
    print(variables)
