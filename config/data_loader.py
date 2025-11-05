from sqlalchemy.orm import Session
from models.author import Author
from models.category import Category
from models.book import Book
from models.user import User
from datetime import date, datetime

class DataLoader:
    def __init__(self, db: Session):
        self.db = db
    
    def load_test_data(self):
        """Загрузка тестовых данных в базу"""
        
        if self.db.query(Author).count() > 0:
            print(" Тестовые данные уже загружены")
            return
        
        print(" Загрузка тестовых данных...")
        
        fiction = Category(
            name="Художественная литература",
            description="Романы, повести, рассказы"
        )
        
        science = Category(
            name="Научная литература", 
            description="Учебники, научные труды"
        )
        
        history = Category(
            name="История",
            description="Исторические книги"
        )
        
        self.db.add_all([fiction, science, history])
        self.db.commit()
        
        tolstoy = Author(
            first_name="Лев",
            last_name="Толстой",
            birth_date=date(1828, 9, 9),
            biography="Русский писатель и мыслитель"
        )
        
        pushkin = Author(
            first_name="Александр", 
            last_name="Пушкин",
            birth_date=date(1799, 6, 6),
            biography="Русский поэт, драматург и прозаик"
        )
        
        self.db.add_all([tolstoy, pushkin])
        self.db.commit()
        
        war_and_peace = Book(
            title="Война и мир",
            isbn="978-5-17-123456-7",
            publication_date=date(1869, 1, 1),
            available_copies=5,
            author_id=tolstoy.id,
            category_id=fiction.id
        )
        
        eugene_onegin = Book(
            title="Евгений Онегин",
            isbn="978-5-17-123457-4", 
            publication_date=date(1833, 1, 1),
            available_copies=3,
            author_id=pushkin.id,
            category_id=fiction.id
        )
        
        self.db.add_all([war_and_peace, eugene_onegin])
        self.db.commit()
        
        admin = User(
            email="admin@library.com",
            password="admin123",
            first_name="Администратор",
            last_name="Системы"
        )
        
        librarian = User(
            email="librarian@library.com",
            password="librarian123",
            first_name="Библиотекарь", 
            last_name="Главный"
        )
        
        self.db.add_all([admin, librarian])
        self.db.commit()
        
        print(" Тестовые данные успешно загружены!")
        print(f"   - Авторов: {self.db.query(Author).count()}")
        print(f"   - Категорий: {self.db.query(Category).count()}")
        print(f"   - Книг: {self.db.query(Book).count()}")
        print(f"   - Пользователей: {self.db.query(User).count()}")