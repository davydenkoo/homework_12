from collections import UserDict
from datetime import datetime
import pickle

class Field:  
      
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value = ""):
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value
    
    
    @value.setter
    def value(self, value: str):
        if value:
            if type(value) == str and len(value) == 10 and value.isdigit():
                self.__value = value
            else:
                raise ValueError
        else:
            self.__value = ""


class Birthday(Field):
    # Birthday must be in format dd.mm.yyyy:
    # 07.06.1984, 20.12.1990, ...

    def __init__(self, value = ""):
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value
    

    @value.setter
    def value(self, value: str):
        if value:
            try:
                self.__value = datetime.strptime(value, '%d.%m.%Y').date()
            except:
                raise ValueError
        else:
            self.__value = ""


    def __str__(self):
        return self.value.strftime('%d.%m.%Y') if self.value else ""


class Record:

    def __init__(self, name, phones = [], birthday = ""):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

        if phones:
            for phone in phones:
                self.phones.append(Phone(phone))


    def add_phone(self, phone: str):
        if phone not in map(lambda item: item.value, self.phones): 
            self.phones.append(Phone(phone))

        return self
    

    def remove_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                self.phones.remove(item)
                break
        
        return self
    

    def edit_phone(self, old_phone: str, new_phone: str):
        for item in self.phones:
            if item.value == old_phone:
                item.value = new_phone
                return self

        raise ValueError
    

    def find_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return item
                    
        return None


    def find(self, find_str: str):
        for item in self.phones:
            if item.value.find(find_str) != -1:
                return item
            
        return None


    def set_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

        return self


    def days_to_birthday(self):
        if self.birthday:

            date_now = datetime.now().date()
            year_now = date_now.year

            birthday_in_this_year = self.birthday.value.replace(year=year_now)
            birthday_in_next_year = self.birthday.value.replace(year=year_now + 1)

            delta1 = birthday_in_this_year - date_now
            delta2 = birthday_in_next_year - date_now

            if int(delta1.days) < 0:
                return delta2.days
            else:
                return delta1.days
        
        return None


    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def __init__(self):  

        self.records_per_page = 3
        self.current_record = 0

        super().__init__()


    def add_record(self, record: Record):
        if self.data.get(record.name.value, "") == "": 
            self.data[record.name.value] = record

        return self
    

    def find_by_name(self, name: str):
        if name in self.data:
            return self.data[name]
        
        return None
    

    def delete(self, name: str):
        self.data.pop(name, "")
        
        return self


    def clear(self):
        self.data = {}

        return self 


    def set_records_per_page(self, records_per_page):
        if type(records_per_page) == int and records_per_page > 0:
            self.records_per_page = records_per_page

            return self

        raise ValueError


    def __iter__(self):
        return self


    def __next__(self):
        if self.current_record < len(self.data):
            if self.current_record > 0:
                input("--------- Press 'Enter' to continue ---------")

            record_vals = list(self.data.values())  
            res = "\n".join(map(lambda x: str(x), record_vals[self.current_record:self.current_record + self.records_per_page]))

            self.current_record += self.records_per_page

            return res
        else:
            self.current_record = 0     
            raise StopIteration
        

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)


    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            content = pickle.load(file)
        
        return content
    

    def find(self, find_str: str):
        res = []
   
        for user_name, user_record in self.data.items():
            if (user_name.find(find_str) != -1 or user_record.find(find_str)):
                res.append(self.data[user_name])

        return res


if __name__ == "__main__":

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John", ["3333333333", "4444444444"], "18.02.1990")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.set_birthday("10.03.1970")
    jane_record.set_birthday("11.03.1970")
    book.add_record(jane_record)

    # Знаходження та редагування телефону для John
    john = book.find_by_name("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 3333333333; 4444444444; 1112223333; 5555555555, birthday: 18.02.1990

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print(book.find_by_name("Jane")) # Виведення: Contact name: Jane, phones: 9876543210, birthday: 11.03.1970

    # Видалення запису Jane
    book.delete("Jane")

    # Додавання записів до книги
    for i in range(1, 30):
        book.add_record(Record(f"fks{i}", ["1111111111", "1111111112"], f"{i}.01.1991"))

    book.add_record(Record(f"Test444", ["4442345678"], f"06.07.1984"))
    book.add_record(Record(f"Test555", ["4442345678"], f"01.07.1985"))

    # Вивід адресної книги посторінково зі значенням records_per_page = 3
    # for record in book:
    #     print(record)

    # print("\n----------------------\n")

    # Вивід адресної книги посторінково зі значенням records_per_page = 5
    # book.set_records_per_page(5)
    # for record in book:
    #     print(record)

    # Збереження книги в файл addressbook.dat
    book.save_to_file("addressbook.dat")

    # Очистка книги
    book.clear()    

    # Перевірка того, що книга очищена
    print("\n----------------------\n")
    for record in book:
        print(record)
    print("\n----------------------\n")

    # Завантаження книги з файлу addressbook.dat
    book = book.load_from_file("addressbook.dat")

    # Перевірка того, що книга завантажилась
    print("\n----------------------\n")
    for record in book:
        print(record)
    print("\n----------------------\n")

    # Пошук по частині імені або номеру телефона 
    find_data = book.find("444")
    for item in find_data:
        print(item)
