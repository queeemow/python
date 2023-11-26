class Solution:
    def letterCombinations(self, digits: str):
        newDig = []
        numOfCombs = 1
        
        for d in digits:
            if int(d) >= 2:
                newDig.append(d)
        comb = {
           2: "abc",
           3: "def",
           4: "ghi",
           5: "jkl",
           6: "mno",
           7: "pqrs",
           8: "tuv",
           9: "wxyz"
        }
        for d in newDig:
            numOfCombs = numOfCombs * len(comb[int(d)])

        res = [[] for i in range(numOfCombs)]

        if len(newDig) < 2:
            try:
                for i in range(len(comb[int(newDig[0])])):
                    res[i] = comb[int(newDig[0])][i]
            except:
                res = []
        elif len(newDig) == 2:
            for i in range(len(comb[int(newDig[0])])):
                for k in range(len(comb[int(newDig[1])])):
                    res[k + i * len(comb[int(newDig[1])])] = comb[int(newDig[0])][i] + comb[int(newDig[1])][k]
        
        elif len(newDig) == 3:
            for i in range(len(comb[int(newDig[0])])):
                for j in range(len(comb[int(newDig[1])])):
                    for k in range(len(comb[int(newDig[2])])):
                        res[k + j * len(comb[int(newDig[2])]) + i * (len(comb[int(newDig[1])]) * len(comb[int(newDig[2])]))] = comb[int(newDig[0])][i] + comb[int(newDig[1])][j] + comb[int(newDig[2])][k]
        
        elif len(newDig) == 4:
            for i in range(len(comb[int(newDig[0])])):
                for j in range(len(comb[int(newDig[1])])):
                    for k in range(len(comb[int(newDig[2])])):
                        for m in range(len(comb[int(newDig[3])])):
                            res[m + k * len(comb[int(newDig[3])]) + j * (len(comb[int(newDig[2])]) * len(comb[int(newDig[3])])) + i * (len(comb[int(newDig[1])]) * len(comb[int(newDig[2])]) * len(comb[int(newDig[3])]))] = comb[int(newDig[0])][i] + comb[int(newDig[1])][j] + comb[int(newDig[2])][k] + comb[int(newDig[3])][m]

        return res

    def isValid(self, s: str):
        if len(s) < 2:
            return False

        for i in range(1,len(s)):
            if not (1 <= ord(s[i]) - ord(s[i-1]) <=2 and s[i] in set(['[',']','{','}','(',')'])):
                return False
            return True

    def divide(self, dividend: int, divisor: int) -> int:
        coaffitient = 1
        newdiv = divisor
        if divisor == 0:
            return False
        if dividend == 0 or abs(dividend) < abs(divisor):
            return 0 
        if divisor == 1:
            return dividend
        if divisor == -1:
            return -dividend
        if (dividend > 0 and divisor < 0) or (dividend < 0 and divisor > 0):
            while abs(divisor) <= abs(dividend):
                if abs(divisor + newdiv) > abs(dividend):
                    return -coaffitient
                divisor = divisor + newdiv
                coaffitient = coaffitient + 1
            return -coaffitient
        else:
            while abs(divisor) <= abs(dividend):
                if abs(divisor + newdiv) > abs(dividend):
                    return coaffitient
                divisor = abs(divisor + newdiv)
                coaffitient = coaffitient + 1
            return coaffitient
    
    def longestValidParentheses(self, s: str) -> int:
        ma = 0
        temp = 0
        
        for i in range(1, len(s)):
            if s[i-1] == '(':
                if s[i] == ')':
                    temp = temp + 2
                else:
                    temp = 0
            if temp > ma:
                ma = temp
        return ma
    MATRIX = None
    def setZeroes(self, matrix) -> None:
        self.MATRIX = matrix
        keyj = None
        keyi = None
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0 or matrix[i+1][j] == 0 or matrix[i][j+1] == 0:
                    keyj = j
                    keyi = i
                if keyj == j or keyi == i:
                    matrix[i][j] = 0
        return matrix
                
            
        pass
if __name__ == "__main__":
    sol = Solution()
    print(sol.setZeroes([[1,1,1],[1,0,1],[1,1,1]]))