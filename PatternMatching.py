def getFrontIdx(before, after):   
    bl = len(before)
    al = len(after)
    minl = min(al,bl)
    i=0
    while(i<minl):
        if before[i]==after[i]:
            i+=1
        else:
            return i

def getEndIdx(before, after): # -형태로 반환
    bl = len(before)
    al = len(after)
    minl = min(al,bl)
    i = -1
    while(i>=(-minl)):
        if before[i]==after[i]:
            i-=1
        else:
            return i

def patternMatch(line, before, after):   
    fi = getFrontIdx(before, after)
    ei = getEndIdx(before, after)
    beforeWord = before[fi:ei+1]
    afterWord = after[fi:ei+1]
    
    if beforeWord == "":
        result = "혹시 '" + afterWord + "'를 깜박하지 않으셨나요? " +  line + "번째 줄의 " + str(fi) + "번째 인덱스에 '" + afterWord + "'을 추가해주세요." 
    elif afterWord == "":
        result = "혹시 '" + beforeWord + "'를 실수로 쓰지 않으셨나요? " + line + "번째 줄의 " + str(fi) + "번째 인덱스에 '" + beforeWord + "'을 지워주세요." 
    else: 
        result = "혹시 '" + beforeWord + "' 라는 변수 대신에 '" + afterWord + "' 라는 변수를 사용하는 것이 맞지 않을까요? "

    result += line + "번째 줄의 '" + beforeWord+ "'를 '" + afterWord + "'으로 바꿔주세요."
    return result

print(patternMatch("3", "print('sdfs';", "print('sdfs');"))
print(patternMatch("3", "word = 10", "new = 10"))