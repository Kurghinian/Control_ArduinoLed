import color_recognition
import video5
def main():
    print("--------------------------------------------------------------")
    print("----------------------Helloooo DigiCode-----------------------")
    print("--------------------------------------------------------------")
    print('Ընտրեք Նախընտրելին')
    print("1 - Կառավարել լույսերը մատների օգնությամբ")
    print("2 - Կառավարել լույսերը պատկերների օգնությամբ")
    q = input()
    if q == "1":
        video5.video()
    elif q == "2":
        color_recognition.color_recognition()
    else:
        print("Ձեր պատասխանը սխալ է")
        main()
main()