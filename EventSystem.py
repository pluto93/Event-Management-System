#This is an Event Management System that allows access to users as well as admin to perform various actions.

#MAIN MENU
def menu():
    a=0
    while a==0:
        print('''
              
              WELCOME TO SHOPEVENTS.COM !''')
        print("1. Book an event")
        print("2. My Dashboard")
        print("3. Cancel an event")
        print("4. Contact details")
        print("5. Admin Menu")
        print("6. Exit")
        choice =int(input("Choose an option: "))
    
        if choice == 1:
            booking()
        elif choice == 2:
            dashboard()
        elif choice == 3:
            cancelevent()
        elif choice == 4:
            contact()
        elif choice == 5:
            admin()
        elif choice == 6:
            print("Exited")
            a=1
            break
    
    else:
        print("Wrong input")
    
 
#This option allows the user to BOOK AN EVENT that is not sold out.
def booking():
    import mysql.connector
    from tabulate import tabulate
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")


        mycursor = mydb.cursor()
        mycursor.execute("select Eno, EventName, ArtistName, EDate from EventsMaster where Soldout='N'")
        myresult = mycursor.fetchall()
        print(tabulate(myresult, headers=['Eno', 'EventName', 'ArtistName', 'EDate'], tablefmt='psql'))
                
        y = input("Choose event number: ")
        

        mycursor3 = mydb.cursor()
        mycursor3.execute("select max(BookingID) from EventsDetail")
        myresult3 = mycursor3.fetchall()
        for a in myresult3:
            Evalue = a[0]+1
            
            
        nt= input("Please enter the no. of tickets to be purchased: ")
        name= input("Please enter the Customer Name: ")
        
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")
        mycursor2 = mydb.cursor()
        mycursor2.execute("insert into EventsDetail(Eno, BookingID, CustomerName, NoofTickets) values ("+ str(y) +","+ str(Evalue) + ",'" + str(name)+ "'," + str(nt) +")")
        mydb.commit()

        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")
        mycursor2 = mydb.cursor()

        mycursor2.execute("update Eventsdetail set Status='Booked' where Eno ="+str(y))
        mydb.commit()
        
        mycursor2.execute("update Eventsdetail set Bookeddate=curdate() where Eno ="+str(y))
        mydb.commit()
        
        print("Booking ID : "+str(Evalue))
           
        print("Booking sucessfully completed !")
    except Exception as e:
        print(e)

#This option prints the DASHBOARD, which shows information about all the events booked by the user.
def dashboard():
    import mysql.connector
    from tabulate import tabulate
    try:
        
        mydb1 = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")
        mycursor = mydb1.cursor()
        
        mycursor.execute("select Eventsmaster.ENo, Eventsmaster.EventName, Eventsmaster.ArtistName, Eventsmaster.EDate, Eventsdetail.BookedDate, Eventsdetail.BookingID, Eventsdetail.CustomerName, Eventsdetail.NoofTickets, DATEDIFF(Edate, curdate()) as DAYSTOGO from Eventsmaster inner join Eventsdetail on Eventsmaster.ENo = Eventsdetail.ENo where Eventsdetail.status = 'Booked';")
        
        myresult = mycursor.fetchall()
        print(tabulate(myresult, headers=['Eno', 'EventName', 'ArtistName', 'EDate', 'BookedDate', 'BookingID', 'CustomerName', 'NoofTickets', 'DaysToGo'], tablefmt='psql'))
        
    except Exception as e:
        print(e)

#This option is for the user to CANCEL AN EVENT booking that they have done.
def cancelevent():
    import mysql.connector
    from tabulate import tabulate
    try:
        mydb1 = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")
        mycursor1 = mydb1.cursor()
        i = int(input("Enter Booking ID of event to be cancelled: "))
        mycursor1.execute("update Eventsdetail set Status = 'Available' where BookingID ="+ str(i))
    
        mydb1.commit()
        
        print("The event has been successfully cancelled")
    except Exception as e:
        print(e)

#This option is for the user to SEE CONTACT DETAILS, which is to be used if the user has any queries.
def contact():
    print('''
          
          For any queries, please contact:
          shopevents@gmail.com
          9456732100 
          
          ''')
          
          
          
          
#ADMIN MENU          
def admin():
    b=0
    while b==0:
        print("1. Create a new event")
        print("2. Delete an event")
        print("3. Update date of an event")
        print("4. Mark event as SOLD OUT")
        print("5. Exit Admin menu")
        choice1 = int(input("Choose an option: "))
        if choice1 == 1:
            createevent()
        elif choice1 == 2:
            deleteevent()
        elif choice1 == 3:
            updateevent()
        elif choice1 == 4:
            soldout()
        elif choice1 == 5:
            b=1
            break
            
    else:
        print("Wrong input")
        
        
#This option is for the admin to CREATE NEW EVENT.  
def createevent():
    import mysql.connector
    from tabulate import tabulate
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")

        mycursor = mydb.cursor()
        a = input("Enter the event number of new event: ")
        b = input("Enter the name of new event: ")
        c = input("Enter the artist name of new event: ")
        d = input("Enter the date of new event: ")
        
        
        mycursor.execute("insert into EventsMaster ( Eno, EventName, ArtistName, EDate) values ("+ str(a) +",'"+ str(b) +"','"+ str(c) +"','"+ str(d) +"')")
         
        mydb.commit()
        mycursor1 = mydb.cursor()
        mycursor1.execute(" update EventsMaster set Soldout='N'")
        mydb.commit()
        print("The new event has been successfully created")
    except Exception as e:
        print(e)

#This option is for the admin to DELETE EVENT.
def deleteevent():
    import mysql.connector
    from tabulate import tabulate
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")

        mycursor = mydb.cursor()
        e = input("Enter event number of event to be deleted: ")
        mycursor.execute("delete from EventsMaster where Eno = " + str(e))
        mydb.commit()
        print("The event has been deleted")
    except Exception as e:
        print(e)

#This option is for the admin TO UPDATE DATE of existing event.       
def updateevent():
    import mysql.connector
    from tabulate import tabulate
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")

        mycursor = mydb.cursor()
        f = input("Enter event number of event to be updated: ")
        g = input("Enter new date of event:  ")
        mycursor.execute("update EventsMaster set EDate ='"+str(g)+"' where Eno = " + str(f))
        mydb.commit()
        print("The date has been successfully updated")
    except Exception as e:
        print(e)

#This option is for the admin to change status of an event to SOLD OUT. This makes sure the event cannot be booked anymore by users.        
def soldout():
    import mysql.connector
    from tabulate import tabulate
    try:
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="mysqldb",database="events2020")

        mycursor = mydb.cursor()
        h = input("Enter event number of event to be marked as SOLD OUT: ")
        mycursor.execute("update EventsMaster set Soldout = 'Y' where Eno = " + str(h))
        mydb.commit()
        print("The status has been successfully updated")
    except Exception as e:
        print(e)
    
    
    
    
menu()                      
    
    
