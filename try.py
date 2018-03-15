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
	return result
print(get_bracket_position('(((1+1)*2)*4)'))
