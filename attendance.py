import tkinter as tk
import tkinter as tk
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkinter import messagebox
import pymongo


def open_student_portal():
    window.destroy()  # Close the initial window
    student_window = tk.Tk()
    student_window.title("Student Portal")
    student_window.configure(background='pink')
    student_window.geometry("1920x1080")
    x_cord = 75
    y_cord = 20
    checker=0
    message = tk.Label(student_window, text="GCET" ,bg="white"  ,fg="black"  ,width=20  ,height=2,font=('Times New Roman', 25, 'bold')) 
    message.place(x=1150, y=660)

    message = tk.Label(student_window, text="STUDENT MANAGEMENT PORTAL" ,bg="pink"  ,fg="black"  ,width=40  ,height=1,font=('Times New Roman', 35, 'bold underline')) 
    message.place(x=200, y=20)

    lbl3 = tk.Label(student_window, text="ATTENDANCE",width=20  ,fg="white"  ,bg="lightgreen"  ,height=2 ,font=('Times New Roman', 30, ' bold ')) 
    lbl3.place(x=120, y=570-y_cord)


    message2 = tk.Label(student_window, text="" ,fg="red"   ,bg="yellow",activeforeground = "green",width=60  ,height=4  ,font=('times', 15, ' bold ')) 
    message2.place(x=700, y=570-y_cord)

    lbl6 = tk.Label(student_window, text="Click Below to Mark Attendance",width=25  ,fg="green"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 20, ' bold ')) 
    lbl6.place(x=600-x_cord, y=289-y_cord)
    def go_back():
        student_window.destroy()  # Close the student window
        main_window()

    def TrackImages():
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("StudentDetails\StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)   
        def save_to_mongodb(attendance_data):
            try:
                client = pymongo.MongoClient("mongodb+srv://sagar:Qag9XVipIwivbkNU@cluster0.j0zo05g.mongodb.net/")  # Change connection URL if needed
                db = client["test"]  # Create or use an existing database
                collection = db["attendance"]  # Create or use an existing collection

                collection.insert_many(attendance_data.to_dict('records'))

                client.close()
            except Exception as e:
                print("Error saving to MongoDB:", e) 
                
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                    
                else:
                    Id='Unknown'                
                    tt=str(Id)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
            cv2.imshow('im',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        res=attendance
        message2.configure(text= res)
        res = "Attendance Taken"
        attendance['Name'] = attendance['Name'].astype(str)
        save_to_mongodb(attendance)
        message.configure(text= res)
        tk.messagebox.showinfo('Completed','Congratulations ! Your attendance has been marked successfully for the day!!')
        
    def quit_window():
        MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
        if MsgBox == 'yes':
            tk.messagebox.showinfo("Greetings", "Thank You very much for using our software. Have a nice day ahead!!")
            student_window.destroy()
        window.destroy()  # Close the initial window
    trackImg = tk.Button(student_window, text="ATTENDANCE MARKING BUTTON", command=TrackImages  ,fg="white"  ,bg="red"  ,width=30  ,height=3, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
    trackImg.place(x=600-x_cord, y=355-y_cord)
    
    quitWindow = tk.Button(student_window, text="QUIT", command=quit_window  ,fg="white"  ,bg="red"  ,width=10  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
    quitWindow.place(x=700, y=735-y_cord)
    back_button = tk.Button(student_window, text="Back", command=go_back, width=10, height=2, font=('Times New Roman', 15, 'bold'))
    back_button.place(x=50, y=735-y_cord)
    student_window.mainloop()
    
    # Rest of your code for the student portal goes here
    
def open_admin_portal():
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "admin@123":
            admin_login_window.destroy()
            open_admin_dashboard()
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

    def open_admin_dashboard():
        window.destroy()  # Close the initial window
        admin_dashborad = tk.Tk()
        admin_dashborad.title("Admin Portal")
        admin_dashborad.configure(background='pink')
        admin_dashborad.geometry("1920x1080")
        x_cord = 75
        y_cord = 20
        checker=0
        message = tk.Label(admin_dashborad, text="GCET" ,bg="white"  ,fg="black"  ,width=20  ,height=2,font=('Times New Roman', 25, 'bold')) 
        message.place(x=1150, y=660)

        message = tk.Label(admin_dashborad, text="Admin PORTAL" ,bg="pink"  ,fg="black"  ,width=40  ,height=1,font=('Times New Roman', 35, 'bold underline')) 
        message.place(x=200, y=20)

        lbl = tk.Label(admin_dashborad, text="Enter Your College ID",width=20  ,height=2  ,fg="black"  ,bg="Pink" ,font=('Times New Roman', 25, ' bold ') ) 
        lbl.place(x=200-x_cord, y=200-y_cord)


        txt = tk.Entry(admin_dashborad,width=30,bg="white" ,fg="blue",font=('Times New Roman', 15, ' bold '))
        txt.place(x=250-x_cord, y=300-y_cord)

        lbl2 = tk.Label(admin_dashborad, text="Enter Your Name",width=20  ,fg="black"  ,bg="pink"    ,height=2 ,font=('Times New Roman', 25, ' bold ')) 
        lbl2.place(x=600-x_cord, y=200-y_cord)

        txt2 = tk.Entry(admin_dashborad,width=30  ,bg="white"  ,fg="blue",font=('Times New Roman', 15, ' bold ')  )
        txt2.place(x=650-x_cord, y=300-y_cord)

        lbl3 = tk.Label(admin_dashborad, text="NOTIFICATION",width=20  ,fg="black"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 25, ' bold ')) 
        lbl3.place(x=1060-x_cord, y=200-y_cord)

        message = tk.Label(admin_dashborad, text="" ,bg="white"  ,fg="blue"  ,width=30  ,height=1, activebackground = "white" ,font=('Times New Roman', 15, ' bold ')) 
        message.place(x=1075-x_cord, y=300-y_cord)

        lbl4 = tk.Label(admin_dashborad, text="STEP 1",width=20  ,fg="green"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
        lbl4.place(x=240-x_cord, y=375-y_cord)

        lbl5 = tk.Label(admin_dashborad, text="STEP 2",width=20  ,fg="green"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 20, ' bold ')) 
        lbl5.place(x=645-x_cord, y=375-y_cord)
        def go_back():
            admin_dashborad.destroy()  # Close the student window
            main_window()
        
        def clear1():
            txt.delete(0, 'end')    
            res = ""
            message.configure(text= res)

        def clear2():
            txt2.delete(0, 'end')    
            res = ""
            message.configure(text= res)    
            
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                pass
        
            try:
                import unicodedata
                unicodedata.numeric(s)
                return True
            except (TypeError, ValueError):
                pass
        
            return False
        
        def TakeImages():        
            Id=(txt.get())
            name=(txt2.get())
            if not Id:
                res="Please enter Id"
                message.configure(text = res)
                MsgBox = tk.messagebox.askquestion ("Warning","Please enter roll number properly , press yes if you understood",icon = 'warning')
                if MsgBox == 'no':
                    tk.messagebox.showinfo('Your need','Please go through the readme file properly')
            elif not name:
                res="Please enter Name"
                message.configure(text = res)
                MsgBox = tk.messagebox.askquestion ("Warning","Please enter your name properly , press yes if you understood",icon = 'warning')
                if MsgBox == 'no':
                    tk.messagebox.showinfo('Your need','Please go through the readme file properly')
                
            elif(is_number(Id) and name.isalpha()):
                    cam = cv2.VideoCapture(0)
                    harcascadePath = "haarcascade_frontalface_default.xml"
                    detector=cv2.CascadeClassifier(harcascadePath)
                    sampleNum=0
                    while(True):
                        ret, img = cam.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = detector.detectMultiScale(gray, 1.3, 5)
                        for (x,y,w,h) in faces:
                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                            #incrementing sample number 
                            sampleNum=sampleNum+1
                            #saving the captured face in the dataset folder TrainingImage
                            cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                            #display the frame
                            cv2.imshow('frame',img)
                        #wait for 100 miliseconds 
                        if cv2.waitKey(100) & 0xFF == ord('q'):
                            break
                        # break if the sample number is morethan 60
                        elif sampleNum>60:
                            break
                    cam.release()
                    cv2.destroyAllWindows() 
                    res = "Images Saved for ID : " + Id +" Name : "+ name
                    row = [Id , name]
                    with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                    csvFile.close()
                    message.configure(text= res)
            else:
                if(is_number(Id)):
                    res = "Enter Alphabetical Name"
                    message.configure(text= res)
                if(name.isalpha()):
                    res = "Enter Numeric Id"
                    message.configure(text= res)
                    
            
        def TrainImages():
            recognizer = cv2.face_LBPHFaceRecognizer.create()
            faces,Id = getImagesAndLabels("TrainingImage")
            recognizer.train(faces, np.array(Id))
            recognizer.save("TrainingImageLabel\Trainner.yml")
            res = "Image Trained"
            clear1();
            clear2();
            message.configure(text= res)
            tk.messagebox.showinfo('Completed','Your model has been trained successfully!!')
            

        def getImagesAndLabels(path):

            imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
            
            faces=[]

            Ids=[]

            for imagePath in imagePaths:
                #loading the image and converting it to gray scale
                pilImage=Image.open(imagePath).convert('L')
                #Now we are converting the PIL image into numpy array
                imageNp=np.array(pilImage,'uint8')
                #getting the Id from the image
                Id=int(os.path.split(imagePath)[-1].split(".")[1])
                # extract the face from the training image sample
                faces.append(imageNp)
                Ids.append(Id)        
            return faces,Ids
            
        def quit_window():
            MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
            if MsgBox == 'yes':
                tk.messagebox.showinfo("Greetings", "Thank You very much for using our software. Have a nice day ahead!!")
                admin_dashborad.destroy()
            window.destroy()  # Close the initial window
        takeImg = tk.Button(admin_dashborad, text="IMAGE CAPTURE BUTTON", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=25  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
        takeImg.place(x=245-x_cord, y=425-y_cord)
        trainImg = tk.Button(admin_dashborad, text="MODEL TRAINING BUTTON", command=TrainImages  ,fg="white"  ,bg="blue"  ,width=25  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
        trainImg.place(x=645-x_cord, y=425-y_cord)
        quitWindow = tk.Button(admin_dashborad, text="QUIT", command=quit_window  ,fg="white"  ,bg="red"  ,width=10  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
        quitWindow.place(x=700, y=735-y_cord)
        back_button = tk.Button(admin_dashborad, text="Back", command=go_back, width=10, height=2, font=('Times New Roman', 15, 'bold'))
        back_button.place(x=50, y=735-y_cord)
        admin_dashborad.mainloop()
    admin_login_window = tk.Tk()
    admin_login_window.title("Admin Login")
    admin_login_window.geometry("400x300")

    username_label = tk.Label(admin_login_window, text="Username:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(admin_login_window)
    username_entry.pack(pady=5)

    password_label = tk.Label(admin_login_window, text="Password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(admin_login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(admin_login_window, text="Login", command=validate_login)
    login_button.pack(pady=20)

    admin_login_window.mainloop()

def main_window():
    global window  # Declare the window as a global variable to access it outside the function
    window = tk.Tk()
    window.title("Attendance System")
    window.configure(background='pink')
    window.geometry("800x600")

    # Add Admin Button (Dummy)
    admin_button = tk.Button(window, text="Admin", command=open_admin_portal, width=20, height=2, font=('Times New Roman', 15, 'bold'))
    admin_button.place(x=150, y=200)

    # Add Student Button
    student_button = tk.Button(window, text="Student", command=open_student_portal, width=20, height=2, font=('Times New Roman', 15, 'bold'))
    student_button.place(x=450, y=200)

    window.mainloop()
main_window()