from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import random,ast

global counter,J
counter = 0
allowed_attempts=5

def generate_problem(t):
        f = open("removed_permutations.txt", "r")
        permutation_dict = {}
        num = 0
        for x in f:
            permutation_dict[num] = x
            num+=1
        #t = random.randint(0,num-1)
        print(num,t)
        p = permutation_dict[t]
        problem = ast.literal_eval(p)
        return problem

#t = random.randint(0,55)    
t=5
J = generate_problem(t)
print(J)

@app.route('/rules')
def show_rules():
    return render_template("rules.html")

@app.route('/', methods = ['POST', 'GET'])
def guess():

    def give_hint(J,counter):
            if (counter == 1):
                m="Hint 1: A = "+ str(J[0])
            if (counter == 2):
                m="Hint 2: A = "+str(J[0])+", B = "+str(J[1])
            if (counter == 3):
                m="Hint 3: A = "+str(J[0])+", B = "+str(J[1])+", C = "+str(J[2])
            if (counter == 4):
                m="Hint 4: A = "+str(J[0])+", B = "+str(J[1])+", C = "+str(J[2])+", D = "+str(J[3])
            if (counter == 5):
                m="Hint 5: A = "+str(J[0])+", B = "+str(J[1])+", C = "+str(J[2])+", D = "+str(J[3])+", E = "+str(J[4])
            if (counter == 6):
                m="Hint 6: A = "+str(J[0])+", B = "+str(J[1])+", C = "+str(J[2])+", D = "+str(J[3])+", E = "+str(J[4])+", F = "+str(J[5])
            if (counter == 7):
                m="Hint 7: A = "+str(J[0])+", B = "+str(J[1])+", C = "+str(J[2])+", D = "+str(J[3])+", E = "+str(J[4])+", F = "+str(J[5])+", G = "+str(J[6])
            if (counter == 8 or counter > 8):
                m="Hint 8: A = "+str(J[0])+", B = "+str(J[1])+", C = "+str(J[2])+", D = "+str(J[3])+", E = "+str(J[4])+", F = "+str(J[5])+", G = "+str(J[6])+", H = "+str(J[6])
            return m

    global counter,J
    print(counter)
    print(J)
    message = ""
    if request.method == 'POST':
        counter += 1
        form = request.form
        user_guess = (form["guess"])#the guess is supposed to be in the form ABC for example. Or DGE, cannot be of size bigger than 4
        #def give hint
        #def generate input
        #J = [1, 2, 6, 1, 16, 2, 2, 2] #current problem
        
        A = ['A','B','C','D','E','F','G','H']
        L = user_guess
        
        T = [0,0,0,0,0,0,0,0]
    
        okay = True
        if (len(L) > 4):
            okay = False
        for i in range (len(L)):
            if (L[i] == 'A'):
                T[0] +=1
                if (T[0]>1):
                    okay = False
            elif (L[i] == 'B'):
                T[1] +=1
                if (T[1]>1):
                    okay = False
            elif (L[i] == 'C'):
                T[2] +=1
                if (T[2]>1):
                    okay = False
            elif (L[i] == 'D'):
                T[3] +=1
                if (T[3]>1):
                    okay = False
            elif (L[i] == 'E'):
                T[4] +=1
                if (T[4]>1):
                    okay = False
            elif (L[i] == 'F'):
                T[5] +=1
                if (T[5]>1):
                    okay = False
            elif (L[i] == 'G'):
                T[6] +=1
                if (T[6]>1):
                    okay = False
            elif (L[i] == 'H'):
                T[7] +=1
                if (T[7]>1):
                    okay = False
            else:
                okay = False
        
        LP= ''
        RP= ''

        LV=0
        RV=0
        if (not okay):
            counter -= 1 #so the counts stay the same as before
            message = "Invalid input, try again."
            return render_template("guess.html", message = message)
        
        #(we assume below code will only run if okay=True, because in above if-statement we return)
        for i in range (8):
            if (T[i] == 1):
                if (LP == ''):
                    LP= LP+A[i]
                else:
                    LP= LP+'+'
                    LP= LP+A[i]
                LV += J[i]
            else:
                if (RP == ''):
                    RP= RP+A[i]
                else:
                    RP= RP+'+'
                    RP= RP+A[i]
                RV += J[i] 
        
        if (LV == RV):
            counterstr = str(counter)
            if counter == 1:
                message = 'Congratulations! You found the correct answer. Indeed '+LP+' = '+RP+'. You made '+counterstr+' attempt in total.'
            else:
                message = 'Congratulations! You found the correct answer. Indeed '+LP+' = '+RP+'. You made '+counterstr+' attempts in total.'
            return render_template("game_over.html", message=message)
        elif (LV < RV):
            counterstr = str(counter)
            message = 'Attempt '+counterstr+': The outcome of this attempt is '+LP+' < '+RP+'. Make another attempt! '
            s=give_hint(J,counter)
            print(s,type(s))
            message = str(message+s)
        else:
            counterstr = str(counter)
            message = 'Attempt '+counterstr+': The outcome of this attempt is '+LP+' > '+RP+'. Make another attempt! '
            s=give_hint(J,counter)
            message = str(message+s)
        if counter == allowed_attempts or counter > allowed_attempts:
            counterstr = str(counter)
            if (LV == RV):
                if counter == 1:
                    message = 'Congratulations! You found the correct answer. Indeed '+LP+' = '+RP+'. You made '+counterstr+' attempt in total.'
                else:
                    message = 'Congratulations! You found the correct answer. Indeed '+LP+' = '+RP+'. You made '+counterstr+' attempts in total.'
                message = str(message)
            elif (LV < RV):
                message = 'Attempt '+counterstr+': The outcome of this attempt is '+LP+' < '+RP+'. Game over!'
                message = str(message)
            else:
                message = 'Attempt '+counterstr+': The outcome of this attempt is '+LP+' > '+RP+'. Game over!'
                message = str(message)
            return render_template("game_over.html", message=message)
    return render_template("guess.html", message = message)

@app.route('/play_again', methods = ['POST', 'GET'])
def gameover():
    global counter,J
    #t = random.randint(0,55)
    t=5
    counter = 0
    J = generate_problem(t)
    return redirect('/')

if __name__ == "__main__":
    counter = 0
    app.run(debug=True)