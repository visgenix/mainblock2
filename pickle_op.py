import pickle
import regex as re

def find_count(s_id):
    x = pickle.load(open("X.sav", "rb"))
    y = pickle.load(open("Y.sav", "rb"))
    count=0
    for id in y:
        if re.search(s_id, str(id)):
            count+=1
            print("Index: ",y.index(id))
    print("Count: ",count)
    
def del_data():
    x = pickle.load(open("X.sav", "rb"))
    y = pickle.load(open("Y.sav", "rb"))
    start=int(input("Enter start index:"))
    end=int(input("Enter end index:"))
    del x[start:end]
    del y[start:end]
    pickle.dump(x,open("X.sav", "wb"))
    pickle.dump(y,open("Y.sav", "wb"))

def count_del(s_id):
    x = pickle.load(open("X.sav", "rb"))
    y = pickle.load(open("Y.sav", "rb"))
    count=0
    for id in y:
        if re.search(s_id, str(id)):
            count+=1
            start = y.index(id)
    end = start+count+1
    del x[start:end]
    del y[start:end]
    pickle.dump(x,open("X.sav", "wb"))
    pickle.dump(y,open("Y.sav", "wb"))
    print("Deleted")

s_id=input("Enter id:")
print("Press 1 for count \nPress 2 for delete \nPress 3 for both \n")

while True:
    choice=int(input("Enter operation:"))
    if choice == 1:
        find_count(s_id)
    elif choice == 2:
        del_data()
    elif choice == 3:
        count_del(s_id)
    else:
        print("Invalid choice!!!")
        break










