import random

# 生成一个随机的身份证号码
def generate_id():
    # 随机生成一个区域码(6位数)
    region_code = str(random.randint(110000, 659004))
    # 生成年份(4位数)
    year = str(random.randint(1970, 2002))
    # 生成月份(2位数)
    month = str(random.randint(1, 12)).rjust(2, '0')
    # 生成日期(2位数)
    day = str(random.randint(1, 28)).rjust(2, '0')
    # 生成顺序码(3位数)
    order = str(random.randint(1, 999)).rjust(3, '0')
    # 生成校验码(1位数)
    check_code = get_check_code(region_code + year + month + day + order)
    # 拼接身份证号码并返回
    return region_code + year + month + day + order + check_code

# 计算校验码
def get_check_code(id17):
    # 系数列表
    factor_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码列表
    check_code_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    # 根据前17位计算出校验码
    check_code = 0
    for i in range(len(id17)):
        check_code += int(id17[i]) * factor_list[i]
    check_code %= 11
    return check_code_list[check_code]

# 生成身份证号码并输出
print(generate_id())