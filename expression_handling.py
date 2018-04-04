"""
数据类型：
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

variables={'A':'String("3445")','B':'Integer(3)'}
reserved_words=['IF', 'ELSE', 'ENDIF', 'WHILE', 'DO', 'ENDWHILE', 'FUNCTION', 'PROCEDURE', 'RETURN', 'DECLARE',
                'NOT', 'STRING', 'INTEGER', 'REAL', 'CHAR', 'BOOLEAN', 'DATE', 'MOD', 'DIV', 'AND', 'OR',
                'INPUT', 'OUTPUT', 'READ', 'WRITE', 'CASE', 'OF', 'ENDCASE', 'ENDPROCEDURE', 'ENDFUNCTION',
                'FOR', 'NEXT', 'TO', 'CALL']
operators=['NOT','OR','AND','>=','>','<=','<','!=','==','+','-','*','/','//']
class_names=['Integer','Real','Character','String','Boolean']
#>=在>之前，<=在<之前，因为之后会根据顺序分割表达式
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
class Character(Variable): #不能进行加减乘除
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
def value_transformation(value): #辨认变量类型
    # print('val',value,type(value))
    if re.match(r'^[+-]?[0-9]+$', value) :
        return 'Integer('+str(value)+')'
    if len(value) >= 2 and value[0] == value[-1] == '"' and "'" not in value:
        return 'String('+str(value)+')'
    if len(value) == 3 and value[0] == value[-1] == "'":
        return 'Char('+str(value)+')'
    if re.match(r'^[+-]?[0-9]+[.][0-9]+$', value):
        return 'Real('+str(value)+')'
    if value=='True' or value=='False':
        return 'Boolean('+str(value)+')'
    if re.match(r'^(String|Integer|Real|Character|Boolean)\((.+)\)$', value):
        match=re.match(r'^(String|Integer|Real|Character|Boolean)\((.+)\)$', value)
        if value_transformation(match.group(2)) == value: # 3.0->Real(3.0)
            return value
    print('未知数据类型:',value)
    return '' #False
print(value_transformation('String("3445")'))


def clean_exps(exps): #去除每个的后面空格，拒绝''
    result = []
    for i in exps:
        if i!='' and i!= (' '*len(i)): #不要'','  '之类
            result.append(i.rstrip().lstrip()) #去掉右边的空格
    for i in range(1,len(result)): #第二个开始左边的也去掉
        result[i]=result[i].lstrip().lstrip()
    return result
def sep_expression(exp,sep): #以sep分隔，去除每个的后面空格，拒绝''
    #TODO 可能有更好地算法
    if isinstance(sep,str):
        sep=[sep]
    original=[exp]
    for op in sep:
        result = []
        for ori in original:
            for t in ori.split(op):
                result.append(t)
                result.append(op)
            result=result[:-1]
        original=result
    result=clean_exps(result)
    for i in range(len(result) - 1):
        if i>= len(result)-1:
            break
        if result[i] in '><' and result[i + 1] == '=': #合并>=和<=
            result[i:i+2] = [result[i] + result[i + 1]]
        if result[i] in '+-' and re.match(r'^\d+\.\d+$',result[i + 1]) and re.match(r'^\d+\.\d+$',result[i + 1]) :
            #合并+/- (int) #TODO 应该判断前后是否都是小数或整数
            result[i:i+2] = [result[i] + result[i + 1]]
    print("sep_expression, result:",result)
    return clean_exps(result)


def sep_exps_eval(exp,operators=[]): #以同一级别的运算符分隔
    #TODO 可能有更好地算法
    result=sep_expression(exp,operators)
    #选择在这里加入判断是否运算符在括号内
    # eg. ['(1','+','2)*3','+','2'] 5项
    op_positions=[i for i in range(len(result)) if result[i] in operators]
    # op_in_bracket_count=0
    print('sep_exps_eval分隔结果，运算符位置，运算符：',result,op_positions,operators)
    for op in operators:
        op_in_bracket_count=0
        op_count=-1 #第一次遇到了变成0，op_in_bracket的时候就可以用正确的op_count
        for real_operator_position in range(len(result)):
            real_operator_position -= op_in_bracket_count * 2  # 每一次都会少2项
            if real_operator_position >= len(result):
                break
            if op in result[real_operator_position]: #只要在里面就+1，应和op_in_bracket需要（保持同步）
                op_count += 1
            if result[real_operator_position]==op and op_in_bracket(result[real_operator_position], op_count,
                                                                             result):
                result[real_operator_position - 1:real_operator_position + 2] = [
                    ''.join(result[real_operator_position - 1:real_operator_position + 2])]
                op_in_bracket_count += 1

    print('sep_exp_eval结果：',result)
    return result
    # return clean_exps(original)




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
        if op in seps[exp_count]:
            op_count+=1
        if op_count==op_seq:
            break
        exp_count+=1
    original_exp = ''.join(seps[:exp_count])
    # print(original_exp)
    if original_exp.count('(') > original_exp.count(')'):
        return True
    else:
        return False  # TODO 检验'）'数量>'（'数量
# print(op_in_bracket('+',0,['(1','+','1)*2']))

def evaluate_transformed_exp(exp): #替换，识别，运算
    flag = False
    for ops in [
        [['NOT', 1]],
        [['OR', 2], ['AND', 2]],
        [['>=', 2], ['<=', 2], ['>', 2], ['<', 2], ['!=', 2], ['==', 2]],
        [['+', 2], ['-', 2]],
        [['*', 2], ['/', 2], ['//', 2]]
    ]:
        # 思路：若是单目，处理之后继续循环；如果是双目，搞完就跑。

        if flag == True:  # 分隔了
            break
        seps = sep_exps_eval(exp, [i[0] for i in ops])  # 提取运算符并分隔
        if seps != [exp]:
            flag = True
        if seps[0]=='+': #单目 （＋－是唯一的双目和单目同一符号，所以当第一个是+-时，和第二项合并）
            seps[0:2]= [seps[0]+seps[1]]
        if seps[0] == '-':  #单目 （＋－是唯一的双目和单目同一符号，所以当第一个是+-时，和第二项合并）
            seps[0:2] = [seps[0]+seps[1]]
        #example: ['-', 'Integer( - 1)']
        if ops[0][1] == 2:
            assert len(seps) % 2  # 双目运算符分割后应该是单数个表达式
            for index in range(1, len(seps), 2):  # index->运算符位置，不就是奇数么
                py_op = seps[1].lower()
                replace_str = str(
                    eval(
                        evaluate_exp(seps[0])+' '+
                        py_op +' '+
                        evaluate_exp(seps[2]) #要有空格
                    ))  # eval('1 AND True')
                seps = [replace_str] + seps[3:]
            continue
        for op in ops:  # op:['AND',2(双目运算符)]
            if ops[0][1] == 1 and op[0] in exp:  # 处理单目运算符,要求存在该运算符+
                flag = False  # 如果是单目，允许进行下一轮
                for op_seq in range(seps.count(op[0])):
                    py_op = op[0].lower()
                    index = seps.index(op[0])
                    replace_str = str(eval(
                        py_op +
                        evaluate_exp(seps[index+1])
                    ))  # eval('not 1') -> 'False'
                    seps = seps[:index] + [replace_str] + seps[index + 2:]

    print('输入:', exp, 'evaluate_transformed_exp的结果是:', seps)
    assert len(seps) == 1  # 化简后应该只有一个
    result = seps[0]
    if value_transformation(result):
        return value_transformation(result)
def strip_surface_brackets(exp): #若最前最后2括号为多余，则舍弃，否则返回原字符串
    print('准备去除前后括号：',exp)
    if exp[0] != '(' or exp[-1] != ')':
        return exp #压根不是
    left_count=0
    for i in exp[1:-1]:
        if left_count<0:
            print('无法去除前后括号：', exp)
            return exp
        if i=='(':
            left_count+=1
        if i==')':
            left_count-=1
    print('已经去除前后括号：', exp[1:-1])
    return exp[1:-1]
def transform_exp(exp): #替换，识别，运算
    print('transform_exp接收到:',exp)
    # if exp[0]=='(' and exp[-1]==')': #TODO 有问题 eg. (1+2)*(3) - > 1+2)*3
    exp=strip_surface_brackets(exp)
    #把所有东西都替换成例如Integer(1)或者String("111")这种玩意就没那么多事了
    if value_transformation(exp): #可能与eval_exp重复
        return value_transformation(exp)
    separated_exps=sep_expression(exp,['(',')']+operators)
    #>=一定要在>前面
    print('transform_exp第1步（分隔）:',separated_exps)
    for exp in range(len(separated_exps)):
        if exp>=len(separated_exps):
            break
        if separated_exps[exp] in class_names:
            separated_exps[exp:exp+4]=[''.join(separated_exps[exp:exp+4])]
            #example: ['Integer', '(', '1', ')', '>=', 'Integer', '(', '2', ')'] -> Integer(1)
        # if separated_exps[exp] =='(' and separated_exps[exp+2]==')': #TODO Necessary?
        #     separated_exps[exp:exp+3]=[separated_exps[exp+1]]
            #example: ['Integer', '(', '1', ')', '>=', 'Integer', '(', '2', ')'] -> Integer(1)
        if separated_exps[0]=='+': #单目 （＋－是唯一的双目和单目同一符号，所以当第一个是+-时，和第二项合并）
            separated_exps[0:2]= [separated_exps[0]+separated_exps[1]]
        if separated_exps[0] == '-':  #单目 （＋－是唯一的双目和单目同一符号，所以当第一个是+-时，和第二项合并）
            separated_exps[0:2] = [separated_exps[0]+separated_exps[1]]


    print('transform_exp第2步（特殊处理）:', separated_exps)
    # for variable_name in variables:
    #     while separated_exps.count(variable_name)>0:
    #         index=separated_exps.index(variable_name)
    #         separated_exps[index] = variables[variable_name]
    for count in range(len(separated_exps)):
        this_term=separated_exps[count]
        if this_term in ['(',')']+operators:
            continue
        elif this_term in variables:
            separated_exps[count] = variables[this_term]
        else:
            separated_exps[count] = value_transformation(this_term)
    exp=' '.join(separated_exps)
    print("transformed_exp:",exp)
    return exp
    #TODO DIV,MOD
evaluate_exp=lambda exp:value_transformation(exp) if value_transformation(exp) else evaluate_transformed_exp(transform_exp(exp))
def assignment(line):
    i = sep_expression(line,'<-')
    identifier, value = i[0], i[1]
    print('identifier=',identifier,'value=',value)
    if variable_name_check(identifier):# and value_transformation(value): #Questioned
        global variables
        variables[identifier] = evaluate_exp(value)
    else:
        pass
# print(evaluate_exp('-(-1)'))
print(evaluate_exp('A AND 4 OR 7 AND (7+5)*6'))