import sys
import re
from io import StringIO
import tokenize

digitspernode=4

def split_expression(str):
    #str.replace("\n","")
    #return re.split("([+*])",str.replace(" ", ""))
    return [token[1] for token in tokenize.generate_tokens(StringIO(str).readline) if token[1]]

def split_number(str,chunk,chunk_size):
    return  [str[i:i+chunk_size] for i in range(0, chunk, chunk_size) ] 


def concatenate_list_data(addition):
    result= ''
    for element in addition:
        result += str(element)
    return result


######addition with loops ###########
def addition(left_list,right_list):
    carry=0
    final_result=[]
    j=len(left_list)-1
    for i in range(len(right_list)-1,-1,-1):
        #print('i=',right_list[i])
        #print('j=',left_list[j])
        add_result=int(right_list[i])+int(left_list[j])+carry
        j=j-1
        #print('add_result=',add_result)
        addition_without_carry=int(add_result%(10**digitspernode))
        #print('addition_without_carry=',addition_without_carry)
        carry=int(add_result/(10**digitspernode))
        #print('carry=',carry)
        final_result.append(str(addition_without_carry))
        #print('Final intermediate addition=',final_result)
    print('Final addition without recursion=',concatenate_list_data(final_result[::-1]))


##########recursive addition#################

def recursive_addition(left_list,right_list,i,carry,final_result):
    if i<0:
        return final_result
    else:
        add_result=int(right_list[i])+int(left_list[i])+carry
        addition_without_carry=int(add_result%(10**digitspernode))
        carry=int(add_result/(10**digitspernode))
        final_result.append(str(addition_without_carry))
        return recursive_addition(left_list,right_list,i-1,carry,final_result)

def for_recursive_addition(left_list,right_list):
    carry=0
    final_result=[]
    i=len(right_list)-1
    final_result=recursive_addition(left_list,right_list,i,carry,final_result)
    print('Final addition with recursion=',concatenate_list_data(final_result[::-1]))
############################## ######

###########multiplication using loop###########
def multiplication(left_list,right_list):
    left_list=concatenate_list_data(left_list)
    right_list=concatenate_list_data(right_list)
    #print(left_list,right_list)
    num1, num2 = left_list[::-1], right_list[::-1]
    res = [0] * (len(num1) + len(num2))
    for i in range(len(num1)):
            for j in range(len(num2)):
                res[i + j] += int(num1[i]) * int(num2[j])
                res[i + j + 1] += int(res[i + j] / 10)  ###carry
                res[i + j] %= 10 ##addition digit
    #print(res)
    # Skip leading 0s.
    i = len(res) - 1
    while i > 0 and res[i] == 0:
        i -= 1

    return ''.join(map(str, res[i::-1]))


###########multiplication using loop###########
def rec_2(num1,num2,i,j,res):
    #print(j)
    if j==len(num2):
        return res
    else:
        res[i+j]+= int(num1[i]) * int(num2[j])
        res[i + j + 1] += int(res[i + j] / 10)  ###carry
        res[i + j] %= 10 ##addition digit
        #print('res in rec_2=',res)
        return rec_2(num1,num2,i,j+1,res)

def recursive_multiplication(num1,num2,i,j,res):
    if i==len(num1):
        return res
    else:
        rec_2(num1,num2,i,j,res)
        recursive_multiplication(num1,num2,i+1,j,res)

def for_recursive_multiplication(left_list,right_list):
    left_list=concatenate_list_data(left_list)
    right_list=concatenate_list_data(right_list)
    #print(left_list,right_list)
    num1, num2 = left_list[::-1], right_list[::-1]
    res = [0] * (len(num1) + len(num2))
    i,j=0,0
    recursive_multiplication(num1,num2,i,j,res)
    '''
    for i in range(len(num1)):
        rec_2(num1,num2,i,j,res)
    '''
    #print('res in recursive_mul=',res)
    # Skip leading 0s.
    i = len(res) - 1
    while i > 0 and res[i] == 0:
        i -= 1
    return ''.join(map(str, res[i::-1]))
    
################

####process text file and main program#####
with open('input.txt',"r") as fp:
    for line in fp:
        exp_list=[]
        print(line)
        exp_list=split_expression(line)  ##split the expression
        #print(exp_list)
        #print(exp_list[0])
        ####split left,right operand and operators
        left_operand=exp_list[0]
        operator=exp_list[1]
        right_operand=exp_list[2]

        #####make both strings/numbers same size with inserting zeros
        max_len = max(len(left_operand), len(right_operand))
        left_operand=left_operand.zfill(max_len)
        right_operand=right_operand.zfill(max_len)
        
        left_operand=left_operand[::-1] ##reverse the string
        right_operand=right_operand[::-1] ##reverse the string
        
        digits = [ int(char) for char in str(left_operand) ]
        
       # print(digits)
       ################# break the numbers into digit nodes list #############
        left_list=[]
        left_list=split_number(left_operand,len(left_operand),digitspernode)    ##create the lists with nodes according to parameter value
        left_list=left_list[::-1]  ##reverse the list
        left_list=[x[::-1] for x in left_list]  ##reverse each element of the list, so the right most node has all the digits
        #print(left_list)
        
        right_list=[]
        right_list=split_number(right_operand,len(right_operand),digitspernode)    ##create the lists with nodes according to parameter value
        right_list=right_list[::-1]##reverse the list
        right_list=[x[::-1] for x in right_list]  ##reverse each element of the list, so the right most node has all the digits
        #print(right_list)

        if operator=='+':  ####when the operator is addition
            print('Addition...')
            addition(left_list,right_list)  ####addition with loops
            for_recursive_addition(left_list,right_list) ###addition with recursion
     
        if operator=='*':  ####when the operator is multiplication
            print('Muliplication....')
            print("Multiplication result with loops=",multiplication(left_list,right_list))
            print("Multiplication result with recursion=",for_recursive_multiplication(left_list,right_list))

        
