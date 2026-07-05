import json
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

def seed_data():
    db = SessionLocal()
    # Create tables if not exist
    models.Base.metadata.create_all(bind=engine)

    # Clear existing questions to ensure clean state
    db.query(models.Question).delete()
    db.commit()
    print("Cleared existing questions.")

    questions = [
        # Mathematics - 10 questions
        {"subject": "Mathematics", "difficulty": "Easy", "text": "What is 12 + 15?", "options": ["25", "27", "30", "22"], "correct_option": 1},
        {"subject": "Mathematics", "difficulty": "Easy", "text": "What is 5 x 6?", "options": ["30", "25", "35", "20"], "correct_option": 0},
        {"subject": "Mathematics", "difficulty": "Easy", "text": "What is 100 / 4?", "options": ["20", "50", "25", "30"], "correct_option": 2},
        {"subject": "Mathematics", "difficulty": "Easy", "text": "What is 50 - 15?", "options": ["45", "30", "35", "25"], "correct_option": 2},
        {"subject": "Mathematics", "difficulty": "Medium", "text": "What is the square root of 144?", "options": ["10", "12", "14", "16"], "correct_option": 1},
        {"subject": "Mathematics", "difficulty": "Medium", "text": "Solve for x: 2x + 5 = 15", "options": ["5", "10", "2", "7"], "correct_option": 0},
        {"subject": "Mathematics", "difficulty": "Medium", "text": "What is 3^4?", "options": ["12", "27", "81", "64"], "correct_option": 2},
        {"subject": "Mathematics", "difficulty": "Medium", "text": "What is the area of a rectangle with length 5 and width 6?", "options": ["11", "30", "25", "20"], "correct_option": 1},
        {"subject": "Mathematics", "difficulty": "Hard", "text": "What is the derivative of x^2?", "options": ["x", "2x", "2", "x^3"], "correct_option": 1},
        {"subject": "Mathematics", "difficulty": "Hard", "text": "What is the integral of 2x dx?", "options": ["2", "x^2", "x^2 + C", "2x^2"], "correct_option": 2},

        # Science - 10 questions
        {"subject": "Science", "difficulty": "Easy", "text": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus", "Jupiter"], "correct_option": 1},
        {"subject": "Science", "difficulty": "Easy", "text": "What gas do humans breath to survive?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "correct_option": 0},
        {"subject": "Science", "difficulty": "Easy", "text": "What is the boiling point of water in Celsius?", "options": ["50", "90", "100", "120"], "correct_option": 2},
        {"subject": "Science", "difficulty": "Easy", "text": "What part of the plant conducts photosynthesis?", "options": ["Root", "Stem", "Leaf", "Flower"], "correct_option": 2},
        {"subject": "Science", "difficulty": "Medium", "text": "What is the chemical symbol for Gold?", "options": ["Gd", "Ag", "Au", "Fe"], "correct_option": 2},
        {"subject": "Science", "difficulty": "Medium", "text": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi"], "correct_option": 2},
        {"subject": "Science", "difficulty": "Medium", "text": "What force keeps planets in orbit around the sun?", "options": ["Friction", "Magnetism", "Gravity", "Tension"], "correct_option": 2},
        {"subject": "Science", "difficulty": "Hard", "text": "What is the speed of light in a vacuum?", "options": ["~300,000 km/s", "~150,000 km/s", "~1,000,000 km/s", "~343 m/s"], "correct_option": 0},
        {"subject": "Science", "difficulty": "Hard", "text": "What is the most abundant gas in Earth's atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Hydrogen", "Nitrogen"], "correct_option": 3},
        {"subject": "Science", "difficulty": "Hard", "text": "What element has the atomic number 1?", "options": ["Helium", "Oxygen", "Hydrogen", "Carbon"], "correct_option": 2},

        # History - 10 questions
        {"subject": "History", "difficulty": "Easy", "text": "Who was the first President of the United States?", "options": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"], "correct_option": 2},
        {"subject": "History", "difficulty": "Easy", "text": "What ancient civilization built the pyramids?", "options": ["Romans", "Greeks", "Mayans", "Egyptians"], "correct_option": 3},
        {"subject": "History", "difficulty": "Easy", "text": "In what year did the Titanic sink?", "options": ["1905", "1912", "1920", "1898"], "correct_option": 1},
        {"subject": "History", "difficulty": "Medium", "text": "In which year did World War II end?", "options": ["1918", "1945", "1939", "1960"], "correct_option": 1},
        {"subject": "History", "difficulty": "Medium", "text": "Who painted the Mona Lisa?", "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "correct_option": 2},
        {"subject": "History", "difficulty": "Medium", "text": "Which empire was ruled by Julius Caesar?", "options": ["Ottoman", "Mongol", "Roman", "British"], "correct_option": 2},
        {"subject": "History", "difficulty": "Hard", "text": "Who was the leader of the Soviet Union during World War II?", "options": ["Vladimir Lenin", "Leon Trotsky", "Joseph Stalin", "Nikita Khrushchev"], "correct_option": 2},
        {"subject": "History", "difficulty": "Hard", "text": "In what year did the French Revolution begin?", "options": ["1776", "1789", "1812", "1848"], "correct_option": 1},
        {"subject": "History", "difficulty": "Hard", "text": "Who was the first female Prime Minister of the UK?", "options": ["Theresa May", "Angela Merkel", "Margaret Thatcher", "Indira Gandhi"], "correct_option": 2},
        {"subject": "History", "difficulty": "Hard", "text": "What was the name of the ship that brought the Pilgrims to America in 1620?", "options": ["Santa Maria", "Mayflower", "Endeavour", "Discovery"], "correct_option": 1},

        # Geography - 10 questions
        {"subject": "Geography", "difficulty": "Easy", "text": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "correct_option": 3},
        {"subject": "Geography", "difficulty": "Easy", "text": "How many continents are there?", "options": ["5", "6", "7", "8"], "correct_option": 2},
        {"subject": "Geography", "difficulty": "Easy", "text": "What is the capital of France?", "options": ["Rome", "Berlin", "Paris", "Madrid"], "correct_option": 2},
        {"subject": "Geography", "difficulty": "Easy", "text": "Which country is known as the Land of the Rising Sun?", "options": ["China", "Japan", "South Korea", "Thailand"], "correct_option": 1},
        {"subject": "Geography", "difficulty": "Medium", "text": "Mount Everest is located in which mountain range?", "options": ["Alps", "Andes", "Rockies", "Himalayas"], "correct_option": 3},
        {"subject": "Geography", "difficulty": "Medium", "text": "What is the longest river in the world?", "options": ["Amazon", "Yangtze", "Nile", "Mississippi"], "correct_option": 2},
        {"subject": "Geography", "difficulty": "Medium", "text": "The Sahara Desert is located on which continent?", "options": ["Asia", "Africa", "Australia", "South America"], "correct_option": 1},
        {"subject": "Geography", "difficulty": "Hard", "text": "What is the smallest country in the world by land area?", "options": ["Monaco", "San Marino", "Vatican City", "Liechtenstein"], "correct_option": 2},
        {"subject": "Geography", "difficulty": "Hard", "text": "Which imaginary line divides the Earth into Northern and Southern Hemispheres?", "options": ["Prime Meridian", "Equator", "Tropic of Cancer", "Tropic of Capricorn"], "correct_option": 1},
        {"subject": "Geography", "difficulty": "Hard", "text": "What is the capital of Australia?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "correct_option": 2},

        # English - 10 questions
        {"subject": "English", "difficulty": "Easy", "text": "Which word is a noun?", "options": ["Run", "Beautiful", "Apple", "Quickly"], "correct_option": 2},
        {"subject": "English", "difficulty": "Easy", "text": "What is the opposite of 'hot'?", "options": ["Warm", "Boiling", "Cold", "Spicy"], "correct_option": 2},
        {"subject": "English", "difficulty": "Easy", "text": "Which of these is a vowel?", "options": ["B", "C", "D", "E"], "correct_option": 3},
        {"subject": "English", "difficulty": "Easy", "text": "Choose the correctly spelled word:", "options": ["Beautifull", "Beautiful", "Beutiful", "Beautyful"], "correct_option": 1},
        {"subject": "English", "difficulty": "Medium", "text": "What is the past tense of 'run'?", "options": ["Runned", "Running", "Ran", "Runs"], "correct_option": 2},
        {"subject": "English", "difficulty": "Medium", "text": "Identify the adjective: 'The quick brown fox'", "options": ["The", "fox", "Quick", "None"], "correct_option": 2},
        {"subject": "English", "difficulty": "Medium", "text": "What is a synonym for 'happy'?", "options": ["Sad", "Angry", "Joyful", "Tired"], "correct_option": 2},
        {"subject": "English", "difficulty": "Hard", "text": "Which of the following is an oxymoron?", "options": ["Jumbo shrimp", "Dark night", "Bright light", "Hot fire"], "correct_option": 0},
        {"subject": "English", "difficulty": "Hard", "text": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "Jane Austen", "William Shakespeare", "Mark Twain"], "correct_option": 2},
        {"subject": "English", "difficulty": "Hard", "text": "What is the term for a word that sounds like what it means (e.g., buzz)?", "options": ["Alliteration", "Simile", "Metaphor", "Onomatopoeia"], "correct_option": 3}
    ]

    for q in questions:
        # Convert options list to JSON string for the DB
        q["options"] = json.dumps(q["options"])
        new_q = models.Question(**q)
        db.add(new_q)
    
    db.commit()
    print(f"Successfully seeded {len(questions)} questions.")

if __name__ == "__main__":
    seed_data()
