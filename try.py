# def get_bracket_position(exp):
# 	bracket_position=[]
# 	left_now=0
# 	right_now=0
# 	exp_now=exp
# 	for i in range(exp.count('(')):
# 		left_now+=exp.find('(')
# 		right_now+=exp.rfind(')')
# 		bracket_position.append([left_now,right_now])
# 		exp_now=exp_now[left_now:right_now]
def get_bracket_position(exp):
	left_bracket_position=[]
	#right_bracket_position=[]
	result=[]
	for char_pos in range(len(exp)):
		if exp[char_pos]=='(':
			left_bracket_position.append(char_pos)
		if exp[char_pos]==')':
			result.append([left_bracket_position.pop(),char_pos])
	assert len(left_bracket_position)==0
	return result

def op_in_bracket(op_position,bracket_positions):
    """
	接受来自get_bracket position的数组，判断运算符是否在括号内
	格式：[[2,4],[1,6]]
	"""
    result=False
    for i in bracket_positions: #TODO 确认op不是括号
        if i[0]<op_position<i[1]:
            result=True
    return result
print(op_in_bracket(4,get_bracket_position('(((1+1)*2)*4)')))