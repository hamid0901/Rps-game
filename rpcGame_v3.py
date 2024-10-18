import random
import time
import sys
import os
import json

def exituser(userName, userPass):
    with open('users.txt', 'r') as f:
        userlist = json.loads(f.read())

    # 삭제할 사용자들의 인덱스를 찾아서 저장
    indexes_to_remove = []
    userfound = False
    for user in userlist:
        if user['name'] == userName:
            userfound = True
            trytime = 1

            while trytime < 3:
                if user['pass'] == userPass:
                    deletemember = userlist.index(user)
                    indexes_to_remove.append(deletemember)
                    break
                    
                else:
                    print("[!] 비밀번호가 틀렸습니다. 다시 시도하세요.")
                    userPass = input("[$] User Password : ")
                    trytime += 1  # 시도 횟수 증가
                
            if trytime >= 3:
                print("[!] 비밀번호 입력 시도가 3회를 초과했습니다. 해킹 우려가 있어 종료됩니다.")
                sys.exit("[^_^] 프로그램이 종료되었습니다.")
               
    if not userfound == True:
            return 1

         
    for index in indexes_to_remove:
        del userlist[index]
            
        with open('users.txt', 'w') as f:
            f.write(json.dumps(userlist))
            print("[$] 계정이 삭제되었습니다.")
            return

def end():
    with open('users.txt', 'r') as f:
        userlist = json.loads(f.read())

    indexes_to_remove = []
    for user in userlist:
        if user['coin'] >= 100000:
            indexes_to_remove.append(userlist.index(user))

    for index in indexes_to_remove:
        del userlist[index]

    with open('users.txt', 'w') as f:
        f.write(json.dumps(userlist))

def deleteuser():
    with open('users.txt', 'r') as f:
        userlist = json.loads(f.read())

    # 삭제할 사용자들의 인덱스를 찾아서 저장
    indexes_to_remove = []
    for user in userlist:
        if user['coin'] <= 0:
            deletemember = userlist.index(user)
            indexes_to_remove.append(deletemember) #if조건이 만족할 때의
    #userlist변수에 있는 그 user 값의 인덱스를 찾아라.

    # 저장된 인덱스를 순서대로 삭제
    for index in indexes_to_remove:
        del userlist[index]

    # 업데이트된 리스트를 파일에 쓰기
    with open('users.txt', 'w') as f:
        f.write(json.dumps(userlist))


def userCreate():
    print("[$] RPC Game Register")

    print("[$] 사용할 이름과 비밀번호를 입력해주세요.")
    userName = input("[$] User Name : ")
    userPass = input("[$] User Password : ")

    dbUserInfo = loaduser(userName) #유저가 등록된 유저인지 확인
    if (dbUserInfo == 0):
        #사용자 등록
        with open('users.txt',"r")  as f:
            filedata = f.read()

            if filedata != "":
                filedata = json.loads(filedata)
            else:
                filedata = []
        userCoin = 1000
        newuser = {"name" : userName,"pass" : userPass,"coin":userCoin}
        filedata.append(newuser)
        
        with open("users.txt","w") as f:
            filedata1 = json.dumps(filedata)
            f.write(filedata1)
            print("{}님의 정보를 생성했습니다.".format(userName))
            print("[$] 웰컴 서비스! 1000코인 지급")
            return newuser
        
def login():
    print("[$] RPC Game Login")
    
    userName = input("[$] User Name : ")
    dbUserInfo = loaduser(userName)

    if dbUserInfo == 0:
        print("[?]존재하지 않는 ID입니다.")
        return 0
    
    trytime = 1
    while trytime <= 3:  # 3번까지 시도
        userPass = input("[$] User Password : ")
        if dbUserInfo["pass"] == userPass:
            return dbUserInfo #로그인 성공
        #break는 루프를 빠져나오는 용도로 쓰이지만,
        #return은 함수 전체를 끝내기 때문에 따로 break가 필요 없습니다.
        
        else:
            print(f"[!]잘못된 비밀번호입니다.{3-trytime}회 남았습니다.")
            trytime += 1

    print("[!] 3회 로그인 실패! 프로그램을 종료합니다.")
    sys.exit("[^_^] 프로그램이 종료되었습니다.")


def saveuser(username,usercoin):
    with open("users.txt","r") as f:
        userlist = json.loads(f.read())

        for user in userlist:
            if username == user["name"]:

                newuserinfo = {"name" : username,"pass":user["pass"],"coin":usercoin}

                index = userlist.index(user) #리스트에서 if username == user["name"]
#이 조건이 만족할때의 인덱스번호를 찾는 역할을 합니다.
                userlist[index] = newuserinfo #이 코드는
                #리스트에서 특정 인덱스에 해당하는 값을 newuserinfo값으로 바꾸는 역할.
    with open('users.txt','w') as f:
        newlist = json.dumps(userlist)
        f.write(newlist)

def loaduser(username):
    with open('users.txt',"r") as f:
        userlist = f.read()
        if userlist != "":
            userlist = json.loads(userlist)
        else:
            print("[!] 계정 정보가 없습니다. 계정을 생성하세요.")
            sys.exit("[^_^] 프로그램이 종료되었습니다.")
        for user in userlist:
            if user['name'] == username:
                return user #username 과 같은 name 의 딕셔너리 정보"만" 반환함.
                #return 문이 실행되면 함수가 즉시 종료되고
                #return 문 이후의 코드는 실행되지 않습니다.
        return 0 #일치하는 사용자를 못 찾았을때

##중요##
#users.txt 에 {"name": "admin", "coin": 10000} 이렇게 쓰면 오류가 나는 이유:
#json.loads() 함수는 JSON 형식의 문자열을 Python 객체로 디코딩합니다.
#이 경우에는 JSON 데이터가 딕셔너리 형태이면 딕셔너리로 반환되고
#배열 형태이면 리스트로 반환됩니다.

def clearConsole():
    command = "clear"
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def rpcComp(user,com):
    if (user + 1) % 3 == com:
        return -1
    elif user == com :
        return 0
    else:
        return 1

rpcValue = {0 : "바위", 1 : "보" , 2 : "가위"}
gameResDic = {-1 : "Lose", 0 : "Draw", 1 : "Win"}

print("[$] 가위/바위/보 게임 Machine [$]")
print("$-+-+-+-+-+-+-+-+-+-+-+-+-$")

print("[$] Main Menu ")
print("-- (1) Login")
print("-- (2) Create User")
print("-- (3) delete User")

while True:
    userinput = input(">")
    userInfo = ""

    if userinput == "1":
        n = 0
        while True:
            
            userInfo = login()

            if userInfo == 0:
                print("[?] 계정이 존재하지 않습니다. 계정을 생성하시겠습니까? (1: 네, 2: 아니요)")
                choice = input("[<] : ")
                if choice == "1":
                    userInfo = userCreate()  # 계정 생성 함수 호출
                    if userInfo:
                        userName = userInfo["name"]
                        userCoin = userInfo["coin"]
                elif choice == "2":
                    print("[^_^] 프로그램을 종료합니다.")
                    sys.exit()

            elif userInfo:
                userName = userInfo["name"]
                userCoin = userInfo["coin"]
                break



    elif(userinput == "2"):
        userInfo = userCreate()
    elif(userinput == "3"):
        userName1 = input("[$]user name : ")
        while True:
            userPass = input("[$]user password : ")
            result = exituser(userName1,userPass)
            if result == 0:
                sys.exit("[^_^] 프로그램이 종료되었습니다.")
            elif result == 1:
                print("[!] id가 존재하지 않습니다.")
                time.sleep(2)
                print("[$] Main Menu ")
                print("-- (1) Login")
                print("-- (2) Create User")
                print("-- (3) delete User")
                break
            
    else:
        print("[!]1,2,3 중 하나만 골라주세요.")
        continue
    
    if userInfo != "":
        break
    
print("[$] {} 님! 대박나세요!".format(userInfo["name"]))
print("[$] 입장을 도와드리겠습니다. 잠시만 기다려주세요...")
time.sleep(3)

while True:
    clearConsole()
    
    print("[User Info]")
    print("-- User Name : {}".format(userInfo["name"]))
    print("-- User Coin : {}".format(userInfo["coin"]))

    if userInfo["coin"] <= 0:
        deleteuser()
        print("[$] 당신은 파산했습니다.")
        print("[$] 퇴장처리됩니다.")
        print("[$] *파산으로 인해 자동으로 계정이 삭제처리됩니다.*")
        sys.exit("[^_^] 또 찾아와주세요! :)")

    if userInfo["coin"] >= 100000:
        print("[$] 100000원을 모은 자.")
        print("""
⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢏⣿⣿⡵⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣮⣷⣿⣿⣿⣿⣷⣄⣄⠀⠀⠀⠀⠈⢞⣿⣿⡵⡀⠀⠀⠀⠀⠀
 ⠀⠀⡠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣏⢦⣤⡀⠀⠀⠀⠫⣻⣿⣾⢄⠀⠀⠀
 ⠀⣔⣿⣿⣿⣿⣿⣿⠿⣿⠻⢟⣿⣿⣿⣿⣿⡆⠀⠀⠀⠑⡿⣿⣯⢆⠀⠀
 ⢰⣸⢿⣻⢟⠃⠉⠉⠀⡠⠤⠸⣸⣿⣿⣿⡳⠁⠀⠀⠀⠀⡨⠺⠿⠇⢓⡄
 ⠧⠊⠁⠘⣖⣳⠠⣶⣋⡹⠁⠀⠛⣩⢻⠋⠀⠀⠀⠀⠀⢀⠇⠀⠀⠀⠀⢾⠀
⠀⠀⢠⠂⠁⠓⠒⠊⠀⡠⠤⡀⢠⠀⠚⠀⠀⠀⠀⠀⡠⠊⢀⠤⡤⣔⠩⠼⡀
⠀⠀⢇⠀⠀⢀⡠⢔⣪⠠⠖⠇⡘⠀⠀⠀⢀⠄⠒⠉⢀⠔⠁⠀⣧⢞⠮⠭⠵⡀
⠀⠀⠘⠒⠉⣾⣀⣀⠀⣀⣀⠦⠗⠹⠙⠃⠁⠀⡠⠔⡡⠔⠒⠉⡨⢴⢹⣿⣏⡆
⠀⠀⠀⠀⡸⠉⠀⠀⠁⠀⠀⠀⠀⣇⡠⡄⡶⠯⠔⠈⠀⠀⡠⠊⠀⠀⡿⣿⣿⡇
⠀⠀⠀⢀⠇⠀⠀⠀⠀⢀⣀⠤⡤⠵⠊⢸⠀⡠⠤⠤⠐⠉⠀⠀⠀⠀⣷⣿⢿⡇
⠀⠀⢀⠃⠀⢀⣀⣀⣀⣠⣀⣀⣿⠉⠉⠉⠉⠀⠀""")
        print("[???]:게임 중독 치료를 시작한다.")
        print("[!]당신의 계정은 ???에 의해서 삭제되었습니다.")
        end()
        sys.exit("Thank you for playing!")
    
    print()
    print("[+] Menu")
    print("0", ":" , "Play")
    print("1", ":", "Exit")
    
    userChoice = input("Choice > ")

    if(userChoice == "1"):
        sys.exit("[^_^] 또 찾아와주세요! :)")
          
    while True:
        print()
        print("이번 게임에 베팅할 코인을 입력해주세요.")
        while True:
            try:
                betCoin = int(input("> "))
            except:
                print("[!] 베팅할 코인 숫자를 입력해주세요.")
                continue
            
            if betCoin > userInfo["coin"]:
                print("[!] 가지고 있는 코인보다 많은 코인을 배팅할 수 없습니다.")
            else:
                break # 아닐경우(정상적인 경우) 루프탈출

        comChoice = random.randint(0,2)
        print()
        print("[-] 아래 선택지 중 선택해주세요.")
        for key in rpcValue:
            print(key, ":", rpcValue[key]) #key는 사전의 키를 나타내며
            #rpcValue[key]는 해당 키에 대응하는 값을 나타냅니다. 

        print()
        try:
            userChoice = int(input("> "))
        except:
            print("[!] 선택지 0, 1, 2 중에 입력해주세요.")
            continue
        break
    
    print()
    print("[$] 가위!", end="\r")
    time.sleep(1)
    print("[$] 바위!!", end="\r")
    time.sleep(1)
    print("[$] 보!!!!!", end="\r")
    time.sleep(1)
    print("        " * 10)

    print("[$] User : " + rpcValue[userChoice])
    print("[$] Computer : " + rpcValue[comChoice])

    gameRes = rpcComp(userChoice,comChoice)

    print("[$] Game 결과 :", gameResDic[gameRes])
    print()

    if(gameRes == 1):
        userInfo["coin"] += betCoin
        print("[$] Olleh~~~! 축하합니다! ")
        print("[$] 베팅한 코인을 얻으셨습니다.")
        print("[$] 획득한 코인 : {}".format(betCoin))
    elif(gameRes == -1):
        userInfo["coin"] -= betCoin
        print("[$] 게임에 지셨습니다. ")
        print("[$] 베팅한 코인이 차감됩니다..")
        print("[$] 차감된 코인 : {}".format(betCoin))
    else:
        print("[$] 게임이 무승부 입니다. ")
    saveuser(userInfo["name"],userInfo["coin"])
    input("[>] 계속하려면 Enter를 누르세요.")