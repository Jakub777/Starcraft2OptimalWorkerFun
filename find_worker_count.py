class Worker:
    production_cost = 50
    # Zasoby na minute
    collection_rate = 40
    def __init__(self, build_time):
        self.build_time = build_time

class Building:
    max_workers = 16
    def __init__(self, build_time, build_cost):
        self.build_time = build_time
        self.build_cost = build_cost
        self.active_workers = 0
        self.is_producing_worker = False
        self.worker_build_time_remaining = 0        

jobless_workers = 0
buildings = []
building_queue = []

def get_total_collection_rate():
    total_active_workers = 0
    for b in buildings:
        total_active_workers += b.active_workers
    # Obliczenie wartosci w ciagu sekundy
    return worker.collection_rate / 60 * total_active_workers

# Wywolywane tylko jesli sa pracownicy bez pracy
def allocate_jobless_workers():
    global jobless_workers
    global buildings
    
    for b in buildings:
        free_spots = b.max_workers - b.active_workers
        # Obydwa warunki musza byc spelnione aby wejsc do srodka
        while (free_spots > 0 and jobless_workers > 0):
            b.active_workers += 1
            jobless_workers -= 1
            free_spots -= 1
    return

# Na czas budowaniaa bazy jeden pracownik jest zajety
def get_worker_to_build_base():
    global jobless_workers
    global buildings
    for b in reversed(buildings):
        if b.active_workers > 0:
            b.active_workers -= 1
            break
    return
    

def calculate_max_workers(time_limit, initial_resources, initial_workers, building):
    global jobless_workers
    global buildings
    global building_queue
    global worker
    current_workers = initial_workers
    current_resources = initial_resources
    current_time = 0
    buildings.append(building)
    jobless_workers = initial_workers

    while current_time < time_limit:
        left_time = time_limit - current_time

        # Dodaj zasoby wyprodukowane przez pracownikow
        current_resources += get_total_collection_rate()
        # print(left_time, current_resources, get_total_collection_rate())

        # Ulokuj pracownikow
        if jobless_workers > 0:
            allocate_jobless_workers()

        # Dodaj budynki do kolejki, gdy mamy wystarczajaco zasobow
        if current_resources >= building.build_cost and building.build_time < left_time:
            building_queue.append(Building(building.build_time, building.build_cost))
            current_resources -= building.build_cost
            get_worker_to_build_base()

        # Produkcja pracowników w dostępnych budynkach
        for b in buildings:
            if not b.is_producing_worker and current_resources >= worker.production_cost:
                current_resources -= worker.production_cost
                b.is_producing_worker = True
                b.worker_build_time_remaining = worker.build_time

        # Przetwarzanie kolejki budynkow
        for b in building_queue:
            if b.build_time > 0:
                b.build_time -= 1

            else:
                buildings.append(b)
                building_queue.remove(b)
                jobless_workers += 1

        # Aktualizacja czasu produkcji pracowników w budynkach
        for b in buildings:
            if b.is_producing_worker:
                if b.worker_build_time_remaining > 0:
                    b.worker_build_time_remaining -= 1
                else:
                    b.is_producing_worker = False
                    current_workers += 1
                    jobless_workers += 1

        # Koniec iteracji
        current_time += 1            

    return current_workers

time_limit = 5 * 60
initial_resources = 100
initial_workers = 12

terran_worker = Worker(12)
protoss_worker = Worker(12)
zerg_worker = Worker(11)

# Pracownik jest instancja uniwersalna w tej wersji i istnieje tylko jedna instancja
worker = terran_worker
building = Building(30, 400)

max_workers = calculate_max_workers(time_limit, initial_resources, initial_workers, building)
print(f"Maksymalna liczba pracowników: {max_workers}")
print(f"Liczba bezrobotnych {jobless_workers}")
print(f"Liczba budynkow: {len(buildings)}")
for b in buildings:
    print(f"active workers: {b.active_workers}")
