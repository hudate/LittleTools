import random

chrs = [chr(a) for a in range(97,122)] + [chr(a) for a in range(65,91)]
nums = [str(a) for a in range(0, 9)]
others = ['_']

def generatePassword(charset, pwdLength, pwdNum):
    # 将生成的密码保存在集合中，采取集合的原因是，集合中的每个元素都不相同，确保每次生成的一批密码，都不会相同
    pwdSet = set()
    
    while len(pwdSet) < pwdNum:
        chars = charset.copy()
        epwd = ''
        for eChar in range(0, pwdLength):
            # 获取随机数，范围0～len(chars)
            chrIndex = random.randint(0, len(chars) - 1)
            # 获取字符
            epwd += chars[chrIndex]
            # 移除字符，确保每次取到的字符都不一样
            chars.remove(chars[chrIndex])
        
        pwdSet.add(epwd)
    
    return pwdSet
    
chrs = [chr(a) for a in range(97,113)]
nums = [str(a) for a in range(0, 9)]
others = []
chars = chrs + nums + others
pwds = generatePassword(chars, 8, 1000000)
print(pwds)

if '__name__' == '__main__':

    h = [chr(a) for a in range(97,113)]
    n = [str(a) for a in range(0, 9)]
    chars = h + n
    pwds = generatePassword(chars, 8, 10)
    
    print(pwds)


        
    
