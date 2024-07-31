#Importing modules
import mysql.connector
from math import floor, ceil
from datetime import datetime

#Establishing connection
connect = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'Enter Your Database Password', database = 'invoices')
cursor = connect.cursor()

#Function definitions

def spacing(invoice): #For arranging data in form of table
    print(' ', '-'*16, '-'*26, '-'*26, '-'*12, '-'*25, '', sep = '+')
    print('', 'INVOICE NUMBER', '     CUSTOMER NAME      ', '        ADDRESS         ', '   DATE   ', '     INVOICE TOTAL     ', '', sep = ' | ')
    print(' ', '-'*16, '-'*26, '-'*26, '-'*12, '-'*25, '', sep = '+')
    for c in invoice:
        print('', ' '*floor(7-len(str(c[0]))/2) + str(c[0]) + ' '*ceil(7-len(str(c[0]))/2), ' '*floor(12-len(c[1])/2) + c[1] + ' '*ceil(12-len(c[1])/2), ' '*floor(12-len(c[2])/2) + c[2] + ' '*ceil(12-len(c[2])/2), str(c[3]), ' '*floor(11.5-len(str(c[4]))/2) + str(c[4]) + ' '*ceil(11.5-len(str(c[4]))/2), '', sep = ' | ')
    print(' ', '-'*16, '-'*26, '-'*26, '-'*12, '-'*25, '', sep = '+')
    
def date_input():  # Taking date from user
    while True:
        try:
            d = int(input('\n>> Enter Date (DD): '))
            if 1 <= d <= 31:
                break
            else:
                print('\nInvalid date. Enter a number between 01 and 31.')
        except ValueError:
            print('\nInvalid input. Please enter a numeric value for the date.')

    while True:
        try:
            m = int(input('\n>> Enter Month Number (MM): '))
            if 1 <= m <= 12:
                break
            else:
                print('\nInvalid month. Enter a number between 01 and 12.')
        except ValueError:
            print('\nInvalid input. Please enter a numeric value for the month.')

    current_year = datetime.now().year
    
    while True:
        try:
            y = int(input('\n>> Enter Year (YYYY): '))
            if 2000 <= y <= current_year:
                break
            else:
                print(f'\nInvalid year. Enter a year between 2000 and {current_year}.')
        except ValueError:
            print('\nInvalid input. Please enter a numeric value for the year.')

    # Format the date parts to ensure two digits for day and month
    d_str = f'{d:02}'
    m_str = f'{m:02}'
    y_str = str(y)

    req_date = f'{y_str}-{m_str}-{d_str}'
    return req_date


def display(invoice): #Displaying particular customer
    if len(invoice) == 0:
        print('\nNo matching record found!')
    else:
        print()
        spacing(invoice)
        
def invoice_display(no): #Displaying invoice
    cursor.execute('SELECT * FROM INVOICE_%s' %(no,))
    invoice = cursor.fetchall()
    cursor.execute('SELECT * FROM INVOICES_LIST WHERE INVOICE_NO = %s' %(no,))
    display = cursor.fetchall()
    display = display[0]
    date = display[3]
    name = display[1]
    phoneNumber = display[2]
    total = display[4]
    print('\n' + '='*140)
    print('\n• Invoice date  : ', date)
    print('\n• Invoice number: ', no)
    print('\n• Customer name: ', name, '\t  • Phone Number: ', phoneNumber, '\n\n')
    print(' ', '-'*26, '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
    print('', ' '*10 + 'ITEM' + ' '*10, ' QUANTITY  ', '     RATE/ITEM(Rs)     ', 'TAX%', '     TAX VALUE(Rs)     ', '       TOTAL(Rs)       ', '', sep = ' | ')
    print(' ', '-'*26, '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
    for i in invoice:
        print('', ' '*floor(12-len((i[0]))/2) + i[0] + ' '*ceil(12-len((i[0]))/2), ' '*floor(5.5-len(str(i[1]))/2) + str(i[1]) + ' '*ceil(5.5-len(str(i[1]))/2), ' '*floor(11.5-len(str(i[2]))/2) + str(i[2]) + ' '*ceil(11.5-len(str(i[2]))/2), str(i[3]) + ' '*(4-len(str(i[3]))), ' '*floor(11.5-len(str(i[4]))/2) + str(i[4]) + ' '*ceil(11.5-len(str(i[4]))/2), ' '*floor(11.5-len(str(i[5]))/2) + str(i[5]) + ' '*ceil(11.5-len(str(i[5]))/2), '', sep = ' | ')
    print(' ', '-'*26, '-'*13, '-'*25, '-'*6, '-'*25, '-'*25, '', sep = '+')
    print('\nINVOICE TOTAL: Rs', total, '\n')
    print('PDB Mega Mart, Matara')
    
def all(): #Displaying all customers
    cursor.execute('SELECT * FROM INVOICES_LIST')
    invoice = cursor.fetchall()
    if len(invoice) == 0:
        print('No existing record')
    else:
        spacing(invoice)
        
def date(): #Displaying customers by date
    given_date = date_input()
    cursor.execute("SELECT * FROM INVOICES_LIST WHERE DATE = '%s'" %(given_date,))
    invoice = cursor.fetchall()
    display(invoice)
    
def total(): # Displaying customers by total
    while True:
        try:
            lower = float(input('\n>> Enter Lower Limit of Total (Rs): '))
            upper = float(input('\n>> Enter Upper Limit of Total (Rs): '))
            
            if lower < 0 or upper < 0:
                print('\nTotal amounts cannot be negative. Please enter valid amounts.')
                continue
            
            if lower > upper:
                print('\nThe lower limit cannot be greater than the upper limit. Please enter again.')
                continue
            
            if upper > 1e12:  # Set a reasonable upper limit
                print('\nThe upper limit is too large. Please enter a smaller amount.')
                continue
            
            break
        except ValueError:
            print('\nInvalid input. Please enter a numeric value.')

    query = 'SELECT * FROM INVOICES_LIST WHERE INVOICE_TOTAL BETWEEN %s AND %s'
    cursor.execute(query, (lower, upper))
    invoices = cursor.fetchall()
    
    display(invoices)

    
def invoice_by_no():  # Displaying invoice by no.
    while True:
        no = get_valid_invoice_no()
        cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
        invoices = cursor.fetchall()
        if (no,) in invoices:
            print()
            invoice_display(no)
            break
        else:
            print('\nInvoice does not exist. Please enter a valid invoice number.')

        
def all_invoices(): #Displaying all invoices
    cursor.execute('SELECT * FROM INVOICES_LIST')
    invoices_list = cursor.fetchall()
    if len(invoices_list) == 0:
        print('No existing invoice')
    for i in invoices_list:
        invoice_display(i[0])
        print()


def get_valid_item_name(): #Get a valid item name
    while True:
        item = input('\n>> Enter Item Name: ').capitalize()
        if item.isalpha():
            if len(item) > 24:
                item = item[:24]
            return item
        else:
            print('\nInvalid input. Item name should contain only letters. Please enter again.')
            
def get_valid_quantity(): #Get a valid quantity
    while True:
        try:
            quantity = int(input('\n>> Enter Quantity: '))
            if 0 < quantity <= 5000:
                return quantity
            else:
                print('\nQuantity must be between 1 and 5000. Please enter again.')
        except ValueError:
            print('\nInvalid input. Quantity must be a number. Please enter again.')

def get_valid_rate(): #Get a valid rate
    while True:
        try:
            rate = float(input('\n>> Please Enter the Rate Per Item (Rs): '))
            rate = round(rate, 2)
            return rate
        except ValueError:
            print('\nInvalid input. Rate must be a number. Please enter again.')

def get_valid_tax(): #Get a valid tax percentage
    while True:
        tax = input('\n>> Enter Tax %, if applicable. If Not, Press Enter: ')
        if len(tax) == 0:
            return 0
        try:
            tax = float(tax)
            if 0 <= tax <= 80:
                return round(tax, 1)
            else:
                print('\nTax must be between 0% and 80%. Please enter again.')
        except ValueError:
            print('\nInvalid input. Tax must be a number. Please enter again.')


        
def new_items(no):  # Entering new items in invoice
    while True:
        # Get a valid item name from the user
        item = get_valid_item_name()

        # Get a valid quantity from the user
        quantity = get_valid_quantity()

        # Get a valid rate from the user
        rate = get_valid_rate()

        # Get a valid tax percentage from the user
        tax = get_valid_tax()


        tax_value = rate * quantity * tax / 100
        total = rate * quantity + tax_value
        total = round(total, 2)
        
        cursor.execute("INSERT INTO INVOICE_%s VALUES('%s', %s, %s, %s, %s, %s)" % (no, item, quantity, rate, tax, tax_value, total))

        while True:
            more = input('\n>> Do you want to enter more items? If not, press Enter: ').strip().lower()
            if more in ['y', 'n', '']:
                if more == '':
                    more = 'n'
                if more == 'n':
                    break
                else:
                    continue
            else:
                print('\nInvalid input. Please enter "Y" for yes or "N" for no.')

        if more == 'n':
            break

    cursor.execute('SELECT SUM(TOTAL) FROM INVOICE_%s' % (no,))
    total = cursor.fetchall()
    total = total[0][0]
    total = round(total, 2)
    return total


def new():  # Making new invoice
    date = date_input()
    
    # Customer name input with validation
    while True:
        name = input('\n>> Enter Customer Name: ').title()
        if name.isalpha():
            if len(name) > 24:
                name = name[:24]
            break
        else:
            print('\nInvalid input. Customer name should contain only letters. Please enter again.')

    # Phone number input with validation
    while True:
        phoneNumber = input('\n>> Enter customer Phone Number: ')
        if phoneNumber.isdigit() and len(phoneNumber) == 10:
            break
        else:
            print('\nInvalid input. Phone number should contain exactly 10 digits. Please enter again.')

    # Insert the new invoice into INVOICES_LIST with auto-generated INVOICE_NO
    cursor.execute("INSERT INTO INVOICES_LIST (CUSTOMER_NAME, PHONE_NUMBER, DATE, INVOICE_TOTAL) VALUES ('%s', '%s', '%s', 0)" % (name, phoneNumber, date))
    connect.commit()

    # Retrieve the auto-generated INVOICE_NO
    cursor.execute("SELECT LAST_INSERT_ID()")
    no = cursor.fetchone()[0]

    cursor.execute('CREATE TABLE INVOICE_%s (ITEM VARCHAR(24), QUANTITY INT, RATE FLOAT, TAX FLOAT, TAX_VALUE FLOAT, TOTAL FLOAT)' % (no,))
    sum_total = new_items(no)

    # Update the invoice total in INVOICES_LIST
    cursor.execute("UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s" % (sum_total, no))
    connect.commit()

    invoice_display(no)


def get_valid_invoice_no():
    while True:
        invoice_no = input('\n>> Enter Invoice No: ')
        if invoice_no.isdigit():
            invoice_no = int(invoice_no)
            if invoice_no > 0:
                return invoice_no
            else:
                print('\nInvoice number must be greater than 0. Please enter again.')
        else:
            print('\nInvalid input. Please enter a valid numeric invoice number.')

def get_valid_name(): #Get a valid customer name
    while True:
        name = input('\n>> Enter Customer Name: ').title()
        if name.isalpha():
            if len(name) > 24:
                name = name[:24]
            return name
        else:
            print('\nInvalid input. Customer name should contain only letters. Please enter again.')

def get_valid_phone_number(): #Get a valid phone number
    while True:
        phoneNumber = input('\n>> Enter Customer Phone Number: ')
        if phoneNumber.isdigit() and len(phoneNumber) == 10:
            return phoneNumber
        else:
            print('\nInvalid input. Phone number should contain exactly 10 digits. Please enter again.')

def get_valid_choice_invoice_edit(): #Get a valid choice for invoice editing
    while True:
        try:
            choice = int(input('\n>> Enter Choice (1-6): '))
            if 1 <= choice <= 6:
                return choice
            else:
                print('\nInvalid choice. Please enter a number between 1 and 6.')
        except ValueError:
            print('\nInvalid input. Please enter a number between 1 and 6.')
            
def get_valid_choice_item_edit(): #Get a valid choice for item editing (1-4)
    while True:
        try:
            choice = int(input('\n>> Enter Choice (1-4): '))
            if 1 <= choice <= 4:
                return choice
            else:
                print('\nInvalid choice. Please enter a number between 1 and 4.')
        except ValueError:
            print('\nInvalid input. Please enter a number between 1 and 4.')
            
def get_valid_item_new_name(): #Get a valid new item name
    while True:
        item = input('\n>> Enter New Item Name: ').capitalize()
        if item.isalpha():
            if len(item) > 24:
                item = item[:24]
            return item
        else:
            print('\nInvalid input. Item name should contain only letters. Please enter again.')

def get_valid_new_rate(): #Get a valid new rate per item
    while True:
        try:
            rate = float(input('\n>> Please Enter the New Rate Per Item (Rs): '))
            rate = round(rate, 2)
            return rate
        except ValueError:
            print('\nInvalid input. Rate must be a number. Please enter again.')

def get_valid_new_tax(): #Get a valid new tax percentage
    while True:
        tax = input('\n>> Enter New Tax %, if applicable. If Not, Press Enter: ')
        if len(tax) == 0:
            return 0
        try:
            tax = float(tax)
            if 0 <= tax <= 80:
                return round(tax, 1)
            else:
                print('\nTax must be between 0% and 80%. Please enter again.')
        except ValueError:
            print('\nInvalid input. Tax must be a number. Please enter again.')



def edit_invoice():  # Editing invoice
    no = get_valid_invoice_no()
    cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
    invoices = cursor.fetchall()
    if (no,) not in invoices:
        print('\nInvoice does not exist.')
    else:
        print('\n\t\t\t\t\t\t' + '='*35)
        print('\n\t\t\t\t\t\t\t CURRENT INVOICE')
        print('\n\t\t\t\t\t\t' + '='*35)
        invoice_display(no)
        print('\n>> What Do You Want to Edit?')
        print('\n1. Date')
        print('2. Customer Name')
        print('3. Customer Phone Number')
        print('4. Delete Item')
        print('5. Enter New Items')
        print('6. Edit Item Details')
        choice3 = get_valid_choice_invoice_edit()
        print()
        if choice3 == 1:  # Editing date
            date = date_input()
            cursor.execute("UPDATE INVOICES_LIST SET DATE = '%s' WHERE INVOICE_NO = %s" % (date, no))
        elif choice3 == 2:  # Editing customer name
            name = get_valid_name()
            cursor.execute("UPDATE INVOICES_LIST SET CUSTOMER_NAME = '%s' WHERE INVOICE_NO = %s" % (name, no))
        elif choice3 == 3:  # Editing customer phone number
            phoneNumber = get_valid_phone_number()
            cursor.execute("UPDATE INVOICES_LIST SET PHONE_NUMBER = '%s' WHERE INVOICE_NO = %s" % (phoneNumber, no))
        elif choice3 == 4:  # Deleting item
             while True:
                item = input('\n>> Enter Name of Item to be Deleted: ').capitalize()
                if item.isdigit():
                     print('\nInvalid input. Item name should not be a number. Please enter again.')
                     continue
                cursor.execute('SELECT ITEM FROM INVOICE_%s' % (no,))
                items = cursor.fetchall()
                if (item,) in items:
                    break
                else:
                    print('\nItem does not exist. Enter again.')
                    
             cursor.execute("DELETE FROM INVOICE_%s WHERE ITEM = '%s'" % (no, item))
             cursor.execute('SELECT SUM(TOTAL) FROM INVOICE_%s' % (no,))
             total = cursor.fetchall()
             total = total[0][0]
             cursor.execute('UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s' % (total, no))
            

        elif choice3 == 5:  # Entering new item
            sum_total = new_items(no)
            cursor.execute('UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s' % (sum_total, no))
        elif choice3 == 6:  # Editing item
            item = input("\n>> Which Item's Details do You Want to Change?: ").capitalize()
            cursor.execute('SELECT ITEM FROM INVOICE_%s' % (no,))
            items = cursor.fetchall()
            while (item,) not in items:
                print('\nItem does not exist. Enter again')
                item = input("\n>> Which Item's Details do You Want to Change?: ").capitalize()
            print('\nCURRENT DETAILS')
            cursor.execute("SELECT * FROM INVOICE_%s WHERE ITEM = '%s'" % (no, item))
            invoice = cursor.fetchall()
            print(' ', '-' * 13, '-' * 25, '-' * 6, '-' * 25, '-' * 25, '', sep='+')
            print('', ' QUANTITY  ', '     RATE/ITEM(Rs)     ', 'TAX%', '     TAX VALUE(Rs)     ', '       TOTAL(Rs)       ', '', sep=' | ')
            print(' ', '-' * 13, '-' * 25, '-' * 6, '-' * 25, '-' * 25, '', sep='+')
            for i in invoice:
                quantity = i[1]
                rate = i[2]
                tax = i[3]
                print('', ' ' * floor(5.5 - len(str(i[1])) / 2) + str(i[1]) + ' ' * ceil(5.5 - len(str(i[1])) / 2),
                      ' ' * floor(11.5 - len(str(i[2])) / 2) + str(i[2]) + ' ' * ceil(11.5 - len(str(i[2])) / 2),
                      str(i[3]) + ' ' * (4 - len(str(i[3]))),
                      ' ' * floor(11.5 - len(str(i[4])) / 2) + str(i[4]) + ' ' * ceil(11.5 - len(str(i[4])) / 2),
                      ' ' * floor(11.5 - len(str(i[5])) / 2) + str(i[5]) + ' ' * ceil(11.5 - len(str(i[5])) / 2), '',
                      sep=' | ')
            print(' ', '-' * 13, '-' * 25, '-' * 6, '-' * 25, '-' * 25, '', sep='+')
            print('\n>> What do you want to change?')
            print('\n1. Item Name')
            print('2. Quantity')
            print('3. Rate')
            print('4. Tax%')
            choice4 = get_valid_choice_item_edit()
            print()
            if choice4 == 1:  # Changing item name
                new_item = get_valid_item_new_name()
                cursor.execute("UPDATE INVOICE_%s SET ITEM = '%s' WHERE ITEM = '%s'" % (no, new_item, item))
            elif choice4 == 2:  # Changing quantity
                while True:
                    try:
                      quantity = int(input('\n>> Enter New Quantity: '))
                      if 0 < quantity <= 5000:
                         break
                      else:
                         print('\nQuantity must be between 1 and 5000. Please enter again.')
                    except ValueError:
                          print('\nInvalid input. Quantity must be a number. Please enter again.')
                tax_value = rate * quantity * tax / 100
                total = rate * quantity + tax_value
                total = round(total, 2)
                cursor.execute("UPDATE INVOICE_%s SET QUANTITY = %s, TOTAL = %s WHERE ITEM = '%s'" % (no, quantity, total, item))
            elif choice4 == 3:  # Changing rate/item
                rate = get_valid_new_rate()
                tax_value = rate * quantity * tax / 100
                total = rate * quantity + tax_value
                total = round(total, 2)
                cursor.execute("UPDATE INVOICE_%s SET RATE = %s, TOTAL = %s WHERE ITEM = '%s'" % (no, rate, total, item))
            elif choice4 == 4:  # Changing tax%
                tax = get_valid_new_tax()
                tax_value = rate * quantity * tax / 100
                total = rate * quantity + tax_value
                cursor.execute("UPDATE INVOICE_%s SET TAX = %s, TAX_VALUE = %s, TOTAL = %s WHERE ITEM = '%s'" % (no, tax, tax_value, total, item))
            else:
                print('\nWrong input')
            cursor.execute('SELECT SUM(TOTAL) FROM INVOICE_%s' % (no,))
            total = cursor.fetchall()
            total = total[0][0]
            cursor.execute('UPDATE INVOICES_LIST SET INVOICE_TOTAL = %s WHERE INVOICE_NO = %s' % (total, no))
        else:
            print('\nWrong input')
        if 0 < choice3 < 6 or (choice3 == 6 and 0 < choice4 < 5):
            connect.commit()
            print('\n\nINVOICE UPDATED')
            invoice_display(no)

            
            
def delete():  # Deleting invoice
    while True:
        no = get_valid_invoice_no()
        cursor.execute('SELECT INVOICE_NO FROM INVOICES_LIST')
        invoices = cursor.fetchall()
        if (no,) in invoices:
            cursor.execute('DROP TABLE INVOICE_%s' % (no,))
            cursor.execute('DELETE FROM INVOICES_LIST WHERE INVOICE_NO = %s' % (no,))
            connect.commit()
            print('\n\nINVOICE DELETED')
            break
        else:
            print('\nInvoice does not exist. Please enter a valid invoice number.')

def display_main_menu():
    print('\n\n' + '='*30)
    print('          Main Menu           ')
    print('='*30)
    print('1. Add New Invoice')
    print('2. View Invoice')
    print('3. Modify Invoice')
    print('4. Exit')
    print('='*30 + '\n')

def display_view_menu():
    print('\n' + '='*40)
    print('\t VIEW INVOICE OPTIONS')
    print('='*40)
    print('1. Display All Customers')
    print('2. Display Customers by Date')
    print('3. Display Customers by Invoice Total Range')
    print('4. Display Invoice of a Customer')
    print('5. Display All Invoices')
    print('6. Return to Main Menu')
    print('='*40 + '\n')


def display_modify_menu():
    print('\n' + '='*35)
    print('\t MODIFY INVOICE OPTIONS')
    print('='*35)
    print('1. Edit Existing Invoice')
    print('2. Delete Existing Invoice')
    print('3. Return to Main Menu')
    print('='*35 + '\n')

def get_choice(prompt, valid_choices):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_choices:
                return choice
            else:
                print(f"\nInvalid choice. Please enter one of the following: {', '.join(map(str, valid_choices))}.\n")
        except ValueError:
            print("\nInvalid input. Please enter a numeric value.\n")

# Main program
print('\t\t\t\t<<< WELCOME TO PDB Mega Mart >>>\n\n')
print('BRN   : PV 12345')
print('VAT No: 114568721-7000')
print('City  : Matara')

while True:
    display_main_menu()
    choice1 = get_choice('>> Enter Choice: ', [1, 2, 3, 4])
    
    if choice1 == 1:
        print('\n' + '='*35)
        print('\t  Add New Invoice')
        print('='*35)
        new()
    
    elif choice1 == 2:
        display_view_menu()
        choice2 = get_choice('>> Enter Choice: ', [1, 2, 3, 4, 5, 6])
        
        if choice2 == 1:
            all()
        elif choice2 == 2:
            date()
        elif choice2 == 3:
            total()
        elif choice2 == 4:
            invoice_by_no()
        elif choice2 == 5:
            all_invoices()
        elif choice2 == 6:
            continue  # Return to the main menu

    elif choice1 == 3:
        display_modify_menu()
        choice2 = get_choice('>> Enter choice: ', [1, 2, 3])
        
        if choice2 == 1:
            edit_invoice()
        elif choice2 == 2:
            delete()
        elif choice2 == 3:
            continue  # Return to the main menu

    elif choice1 == 4:
        print('\nTHANK YOU!')
        break

    else:
        print('\nInvalid input. Please enter a number between 1 and 4.')

# End of program
