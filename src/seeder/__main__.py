from src.seeder.cadastros import main as seed_cadastros
from src.seeder.pacientes import main as seed_pacientes


if __name__ == "__main__":
    seed_cadastros()
    seed_pacientes()
