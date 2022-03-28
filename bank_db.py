import sqlite3
import datetime

db = sqlite3.connect('bank.db')
ex = db.cursor()

ex.execute('create table bankcustomer(id integer primary key,Name text,Amount float)')
ex.execute('create table customertransaction(id integer ,AmountTransacted,TransactedDate)')
ex.execute('alter table customertransaction add column Debit')
ex.execute('alter table customertransaction add Particualrs')
ex.execute('alter table customertransaction rename "Particualrs" to "Particulars"')
ex.execute('alter table customertransaction rename "Debit" to "Credit"')
ex.execute('alter table customertransaction rename "AmountTransacted" to "Debit"')
ex.execute('alter table customertransaction add column TransactionNumber')
ex.execute('alter table customertransaction add column Balance')

created = []
ac_num = list(ex.execute("select id from bankcustomer"))

ac = list(ex.execute("select id from customertransaction"))

for i in range(len(ac_num)):
    created.append(ac_num[i][0])

print("*********************")
print("STATE BANK OF INDIA")
print("*********************")
print("1.Creation")
print("2.Deposit")
print("3.Withdraw")
print("4.Balance Enquiry")
print("5.Show All Customers")
print("6.Delete Account Number")
print("7.Transaction Report")
print("8.Deleting Transaction")
print("9.Exit")

while 1:
    b = 0
    c = 0

    choice = int(input("Enter your choice: "))

    for j in range(len(created) - 1):
        if created[j] == 101:
            if created[j] + 1 not in created:
                b = created[j] + 1
        else:
            if created[j] + 1 not in created or created[j] - 1 not in created:
                if not created[j] - 1 in created:
                    c = created[j] - 1
                    break
                else:
                    b = created[j] + 1
                    break


    def creation():
        a = 0
        global ex
        if b:
            created.insert(j + 1, b)
        elif c:
            created.insert(j - 1, c)
        else:
            a = created[len(created) - 1]
            a += 1
            created.append(a)
        print("Welcome To SBI")
        print("*********************")
        print("   Account Creation  ")
        print("*********************")
        if a:
            print("Your Account number is :" + str(a))
        elif b:
            print("Your Account Number is :" + str(b))
        elif c:
            print("Your Account Number is :" + str(c))
        else:
            print("No Account Number")
        name = input("Enter your name:")
        ini_dep = 500
        print("Deposited amount:" + str(ini_dep))
        today_date = str(datetime.date.today())
        if a:
            ex.execute('insert into bankcustomer(id,Name,Amount,Date)values(?,?,?,?)', (a, name, ini_dep, today_date))
        elif b:
            ex.execute('insert into bankcustomer(id,Name,Amount,Date)values(?,?,?,?)', (b, name, ini_dep, today_date))
        elif c:
            ex.execute('insert into bankcustomer(id,Name,Amount,Date)values(?,?,?,?)', (c, name, ini_dep, today_date))
        else:
            print("Nothing to insert")

        db.commit()


    def deposit():
        trans_his = []
        trans = 1
        global ex
        acc = int(input("Enter your Account Number:"))
        num = list(ex.execute('select TransactionNumber from customertransaction where id = (:ac)', {'ac': acc}))

        for i in range(len(num)):
            trans_his.append(num[i][0])

        if acc not in created:
            print("Invalid Account Number")
        else:
            if trans_his:
                trans += trans_his[len(trans_his) - 1]
            else:
                trans = 1
            de = list(ex.execute('select * from bankcustomer where id = (:account)', {'account': acc}))
            print("Account number:" + str(de[0][0]))
            print("Name:" + de[0][1])
            print("Your Transaction number is:" + str(trans))
            old = de[0][2]
            new = de[0][2]

            print("Deposit:" + str(old))

            particulars = input("How you wanna deposit: Cash/Cheque")
            if particulars.capitalize() == 'Cash':
                today_date = datetime.date.today()
                particulars = 'By Cash'
                credit = int(input("How amount to be credited:"))
                new += credit
                print("Total amount in your account is:" + str(new))
                ex.execute('update bankcustomer set Amount = (:newbalance) where Amount = (:oldbalance)',
                           {"newbalance": new, 'oldbalance': old})
                ex.execute(
                    'insert into customertransaction(id,TransactedDate,Credit,Particulars,TransactionNumber,Balance) values(?,?,?,?,?,?)',
                    (acc, today_date, credit, particulars, trans, new))
            elif particulars.capitalize() == 'Cheque':
                today_date = datetime.date.today()
                particulars = 'By Cheque' + str(int(input("Cheque Number:")))
                credit = int(input("How amount to be credited:"))
                new += credit
                print("Total amount in your account is:" + str(new))
                ex.execute('update bankcustomer set Amount = (:newbalance) where Amount = (:oldbalance)',
                           {"newbalance": new, 'oldbalance': old})
                ex.execute(
                    'insert into customertransaction(id,TransactedDate,Credit,Particulars,TransactionNumber,Balance) values(?,?,?,?,?,?)',
                    (acc, today_date, credit, particulars, trans, new))
            else:
                print("Not Valid")

            db.commit()


    def withdraw():
        trans_his = []
        trans = 1

        acount = int(input("Enter your account number:"))
        num = list(ex.execute('select TransactionNumber from customertransaction where id = (:ac)', {'ac': acount}))

        for i in range(len(num)):
            trans_his.append(num[i][0])

        if trans_his:
            trans += trans_his[len(trans_his) - 1]
        else:
            trans = 1

        print("Withdrawl date" + str(datetime.date.today()))
        print("Your Transaction Number is:" + str(trans))
        today_date = str(datetime.date.today())
        if acount not in created:
            print("Invalid Account Number")
        else:
            am = list(
                ex.execute('select Amount from bankcustomer where id = (:accountnumber)', {"accountnumber": acount}))
            total = am[0][0]
            print("The account balance is", str(total))
            particulars = input("How do you want to withdraw by Cash/Cheque : ")
            if particulars.capitalize() == 'Cash':
                particulars = 'By Cash'
                debit = int(input("Enter amount to be withdraw : "))
                if debit > total:
                    print("You don't have entered amount in your account")
                else:
                    old = total
                    total -= debit
                    print("Your renewed account balance is:" + str(total))
                    ex.execute('update bankcustomer set Amount = (:newbalance) where Amount = (:oldbalance)',
                               {'newbalance': total, 'oldbalance': old})
                    ex.execute(
                        'insert into customertransaction(id,Debit,TransactedDate,Particulars,TransactionNumber,Balance) values(?,?,?,?,?,?)',
                        (acount, debit, today_date, particulars, trans, total))
                    print("Transaction Added")
                    db.commit()
            elif particulars.capitalize() == 'Cheque':
                particulars = "By Cheque" + " " + str(int(input("Enter cheque number:")))
                debit = int(input("Enter amount to be withdraw : "))
                if debit > total:
                    print("You don't have entered amount in your account")
                else:
                    old = total
                    total -= debit
                    print("Your renewed account balance is:" + str(total))
                    ex.execute('update bankcustomer set Amount = (:newbalance) where Amount = (:oldbalance)',
                               {'newbalance': total, 'oldbalance': old})
                    ex.execute(
                        'insert into customertransaction(id,Debit,TransactedDate,Particulars,TransactionNumber,Balance) values(?,?,?,?,?,?)',
                        (acount, debit, today_date, particulars, trans, total))
                    print("Transaction Successful")
                    db.commit()
            else:
                print("Not Valid Form Of Transaction")


    def balance_enquiry():
        global ex
        ac = int(input("Enter your account number : "))
        if ac not in created:
            print("Invalid Account Number")
        else:
            # print("Your current account balance:" + str(info[ac][1]))
            ac = list(ex.execute('select Amount from bankcustomer where id = (:accountnumber)', {'accountnumber': ac}))
            print("Your current account balance:", ac[0][0])


    def delete_records():
        global ex
        ac = int(input("Enter account number you want to delete: "))
        if ac not in created:
            print("Invalid Account Number")
        else:
            ex.execute("delete from bankcustomer where id  = ?", (ac,))
            created.remove(ac)
        db.commit()


    def show_all_records():
        global ex
        ex.execute("select * from bankcustomer")
        record = ex.fetchall()
        print("Account Number     Name          Amount")
        for row in record:
            print("{0}               {1}        {2}".format(row[0], row[1], row[2]))


    def transaction_report():
        acount = int(input("Enter your account number: "))
        if acount not in created:
            print("Invalid Account Number")
        else:
            date = input("Report from which date (yyyy-mm-dd): ")
            upto_date = input("Report to which date (yyyy-mm-dd): ")
            ex.execute(
                'select TransactionNumber,Particulars,Credit,Debit,Balance,TransactedDate from customertransaction where id = (:ac) and TransactedDate between (:da) and (:de)',
                {'ac': acount, 'da': date, 'de': upto_date})
            record = ex.fetchall()
            print("Account Number :" + str(acount))
            print(f"Period {date} - {upto_date} ")
            print("-----------------------------------------------------------------------------------")
            print("Transaction Number      Particulars         Credit       Debit      Balance       Date ")
            for row in record:
                print(
                    " {0}              {1}                 {2}             {3}         {4}          {5}".format(row[0],
                                                                                                                row[1],
                                                                                                                row[2],
                                                                                                                row[3],
                                                                                                                row[4],
                                                                                                                row[5]))


    def delete_transaction():
        acount = int(input("Enter account number:"))
        ex.execute("delete from customertransaction where id = (:ac)", {'ac': acount})
        print("Transaction Deleted")
        db.commit()


    if choice == 1:
        creation()
    elif choice == 2:
        deposit()
    elif choice == 3:
        withdraw()
    elif choice == 4:
        balance_enquiry()
    elif choice == 5:
        show_all_records()
    elif choice == 6:
        delete_records()
    elif choice == 7:
        transaction_report()
    elif choice == 8:
        delete_transaction()
    elif choice == 9:
        print("THANK YOU FOR YOUR VISIT")
        break
    else:
        print("INVALID CHOICE")
