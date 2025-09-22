from sqlmodel import create_engine, Session, SQLModel, select

DATABASE_URL = "sqlite:///starwars.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def populate_sample_data():
    from app.models.starwars import Character, Planet, Starship
    session = Session(engine)
    # Pianeti
    tatooine = Planet(name="Tatooine", climate="arid", population=200000)
    alderaan = Planet(name="Alderaan", climate="temperate", population=2000000000)
    naboo = Planet(name="Naboo", climate="temperate", population=4500000000)
    # Personaggi
    luke = Character(name="Luke Skywalker", species="Human", homeworld="Tatooine")
    leia = Character(name="Leia Organa", species="Human", homeworld="Alderaan")
    anakin = Character(name="Anakin Skywalker", species="Human", homeworld="Tatooine")
    padme = Character(name="Padmé Amidala", species="Human", homeworld="Naboo")
    # Astronavi
    falcon = Starship(name="Millennium Falcon", model="YT-1300", manufacturer="Corellian Engineering Corporation")
    xwing = Starship(name="X-wing", model="T-65B", manufacturer="Incom Corporation")
    tie = Starship(name="TIE Fighter", model="Twin Ion Engine", manufacturer="Sienar Fleet Systems")
    # Inserisci solo se il db è vuoto
    if not session.exec(select(Planet)).first():
        session.add_all([tatooine, alderaan, naboo])
    if not session.exec(select(Character)).first():
        session.add_all([luke, leia, anakin, padme])
    if not session.exec(select(Starship)).first():
        session.add_all([falcon, xwing, tie])
    session.commit()
    session.close()
