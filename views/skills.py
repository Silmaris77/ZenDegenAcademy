import streamlit as st
from utils.components import zen_header, zen_button, notification, skill_node
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from data.users import load_user_data, save_user_data

def show_skill_tree():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    st.title("Drzewko umiejętności inwestycyjnych 🌳")
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    user_skills = user_data.get("skills", {})
    user_xp = user_data.get("xp", 0)
    user_completed_lessons = set(user_data.get("completed_lessons", []))
    
    # Definicja bloków tematycznych bez zmian
    blocks = {
        1: {
            'name': '🔥 Emocje & Mózg: Dlaczego inwestowanie tak nas rusza?',
            'description': 'Czemu boli, kiedy tracisz? Jak działa dopamina? Dlaczego biasy psują strategię?',
            'categories': [1, 2, 3]  # ID kategorii należących do tego bloku
        },
        2: {
            'name': '🧘‍♀️ Wewnętrzny Kompas: Jak nie dać się sobie?',
            'description': 'Budujesz nawyki, tworzysz system decyzyjny i uczysz się zarządzać uwagą.',
            'categories': [4, 5, 6, 7]
        },
        3: {
            'name': '🧩 Kim jesteś, gdy inwestujesz?',
            'description': 'Odkrywasz własny profil inwestora, intencje i osobistą strategię.',
            'categories': [8, 9, 14]
        },
        4: {
            'name': '💪 Odporność: Rynek to nie spa – przygotuj się na fale',
            'description': 'Trenujesz siłę psychiczną, uczysz się na błędach i dopasowujesz się do zmienności.',
            'categories': [10, 12, 13]
        },
        5: {
            'name': '🌍 Ludzie, presja i wpływy: Inwestor w społecznym świecie',
            'description': 'Budujesz własną niezależność mimo presji, opinii i otoczenia.',
            'categories': [11, 15]
        }
    }
    
    # Definicja kategorii (kompetencji) bez zmian
    categories = {
        1: {
            'name': 'Emocje w inwestowaniu',
            'id': 'emotions_investing',
            'block': 1,
            'icon': '🔴',
            'description': 'Rozpoznawanie i zarządzanie emocjami w kontekście inwestycyjnym',
            'lessons': get_lessons_for_category(1),
            'level': user_skills.get('emotions_investing', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,  # Zawsze odblokowane
            'cost': 50  # Koszt ulepszenia w XP
        },
        2: {
            'name': 'Neurobiologia i chemia mózgu',
            'id': 'neurobiology',
            'block': 1,
            'icon': '🔬',
            'description': 'Zrozumienie procesów neurobiologicznych zachodzących podczas podejmowania decyzji inwestycyjnych',
            'lessons': get_lessons_for_category(2),
            'level': user_skills.get('neurobiology', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,  # Zmiana z warunkowego na zawsze odblokowane
            'cost': 60
        },
        3: {
            'name': 'Błędy poznawcze',
            'id': 'cognitive_biases',
            'block': 1,
            'icon': '⚠️',
            'description': 'Identyfikowanie i przeciwdziałanie błędom poznawczym w procesie inwestycyjnym',
            'lessons': get_lessons_for_category(3),
            'level': user_skills.get('cognitive_biases', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 70
        },
        4: {
            'name': 'Ukryte filtry poznawcze',
            'id': 'cognitive_filters',
            'block': 2,
            'icon': '🧠',
            'description': 'Odkrywanie i neutralizowanie ukrytych filtrów wpływających na decyzje inwestycyjne',
            'lessons': get_lessons_for_category(4),
            'level': user_skills.get('cognitive_filters', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 70
        },
        5: {
            'name': 'Zarządzanie sobą',
            'id': 'self_management',
            'block': 2,
            'icon': '🧘',
            'description': 'Praktyki i techniki efektywnego zarządzania własnym stanem mentalnym',
            'lessons': get_lessons_for_category(5),
            'level': user_skills.get('self_management', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 80
        },
        6: {
            'name': 'Rozwój osobisty',
            'id': 'personal_growth',
            'block': 2,
            'icon': '🌱',
            'description': 'Rozwijanie kluczowych umiejętności i nawyków inwestora',
            'lessons': get_lessons_for_category(6),
            'level': user_skills.get('personal_growth', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 80
        },
        7: {
            'name': 'Decyzyjność',
            'id': 'decision_making',
            'block': 2,
            'icon': '🎯',
            'description': 'Optymalizacja procesu podejmowania decyzji inwestycyjnych',
            'lessons': get_lessons_for_category(7),
            'level': user_skills.get('decision_making', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 90
        },
        8: {
            'name': 'Metapoznanie',
            'id': 'metacognition',
            'block': 3,
            'icon': '🧩',
            'description': 'Rozwijanie świadomości własnych procesów myślowych w kontekście inwestycyjnym',
            'lessons': get_lessons_for_category(8),
            'level': user_skills.get('metacognition', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 90
        },
        9: {
            'name': 'Styl inwestora',
            'id': 'investor_style',
            'block': 3,
            'icon': '👤',
            'description': 'Odkrywanie i rozwijanie własnego stylu inwestycyjnego',
            'lessons': get_lessons_for_category(9),
            'level': user_skills.get('investor_style', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 100
        },
        10: {
            'name': 'Odporność i adaptacja',
            'id': 'resilience',
            'block': 4,
            'icon': '🧱',
            'description': 'Budowanie odporności psychicznej na zmienność rynku',
            'lessons': get_lessons_for_category(10),
            'level': user_skills.get('resilience', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 100
        },
        11: {
            'name': 'Interakcje społeczne i środowisko inwestora',
            'id': 'social_interactions',
            'block': 5,
            'icon': '🌐',
            'description': 'Efektywne nawigowanie społecznym aspektem inwestowania',
            'lessons': get_lessons_for_category(11),
            'level': user_skills.get('social_interactions', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 110
        },
        12: {
            'name': 'Testowanie i analiza własnych strategii',
            'id': 'strategy_testing',
            'block': 4,
            'icon': '🧪',
            'description': 'Metodyczne testowanie i doskonalenie strategii inwestycyjnych',
            'lessons': get_lessons_for_category(12),
            'level': user_skills.get('strategy_testing', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 110
        },
        13: {
            'name': 'Elastyczność, transformacja i rozwój',
            'id': 'flexibility',
            'block': 4,
            'icon': '🔄',
            'description': 'Rozwijanie zdolności adaptacji do zmieniających się warunków rynkowych',
            'lessons': get_lessons_for_category(13),
            'level': user_skills.get('flexibility', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 120
        },
        14: {
            'name': 'Motywacja i sens działania',
            'id': 'motivation',
            'block': 3,
            'icon': '🌟',
            'description': 'Odkrywanie i wzmacnianie wewnętrznej motywacji do inwestowania',
            'lessons': get_lessons_for_category(14),
            'level': user_skills.get('motivation', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 120
        },
        15: {
            'name': 'Mistrzostwo psychologiczne',
            'id': 'psychological_mastery',
            'block': 5,
            'icon': '🧭',
            'description': 'Osiąganie psychologicznej doskonałości w inwestowaniu',
            'lessons': get_lessons_for_category(15),
            'level': user_skills.get('psychological_mastery', {}).get('level', 0),
            'max_level': 10,
            'unlocked': True,
            'cost': 150
        }
    }
    
    # Zaktualizuj wszystkie kategorie jako odblokowane
    for cat_id in categories:
        categories[cat_id]['unlocked'] = True
    
    # Usuwamy informację o dostępnych punktach XP, gdyż nie jest już potrzebna
    # st.info(f"Dostępne punkty XP: {user_xp}")
      # Dodaj krótką informację o mechanice
    st.markdown("""
        <div class="info-box">
            <h4>📋 Jak zdobywać poziomy umiejętności?</h4>
            <p>Każda ukończona lekcja zwiększa poziom danej umiejętności. Ukończ wszystkie 10 lekcji, aby osiągnąć maksymalny poziom!</p>
            <p>Wszystkie kategorie umiejętności są od razu dostępne - możesz rozpocząć naukę od dowolnego tematu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Dodaj responsywne style dla info-box
    st.markdown("""
    <style>
    /* Styl dla info-box */
    .info-box {
        background: linear-gradient(135deg, rgba(100, 180, 255, 0.2) 0%, rgba(70, 150, 220, 0.3) 100%);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(70, 150, 220, 0.3);
    }
    
    .info-box h4 {
        margin-top: 0;
        color: rgba(40, 40, 40, 0.9);
    }
    
    /* Responsywne style dla info-box na telefonach */
    @media (max-width: 640px) {
        .info-box {
            padding: 12px;
            margin-bottom: 15px;
        }
        
        .info-box h4 {
            font-size: 1.1rem;
            margin-bottom: 8px;
        }
        
        .info-box p {
            font-size: 0.9rem;
            margin: 6px 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Wyświetl wszystkie bloki i ich kategorie
    for block_id, block in blocks.items():
        st.markdown(f"## {block['name']}")
        st.markdown(f"*{block['description']}*")
        
        # Dodaj responsywne style dla nagłówków bloków
        st.markdown("""
        <style>
        /* Nowe style dla bloków */
        .block-header {
            background: linear-gradient(135deg, rgba(150, 150, 160, 0.6) 0%, rgba(120, 120, 130, 0.7) 100%);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #4CAF50;
        }
        
        /* Responsywne style dla nagłówków bloków na telefonach */
        @media (max-width: 640px) {
            .block-header {
                padding: 12px;
                margin-bottom: 15px;
            }
            
            h2 {
                font-size: 1.4rem !important;
                margin-bottom: 8px !important;
            }
            
            h2 + p {
                font-size: 0.9rem !important;
                margin-bottom: 12px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Kontener na blok kategorii
        with st.container():
            st.markdown('<div class="block-container">', unsafe_allow_html=True)
            
            # Wyświetl wszystkie kategorie w bloku
            display_categories_in_block(block_id, categories, user_skills, user_xp, users_data, user_data, user_completed_lessons)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Dodaj separator między blokami
        st.markdown("---")
    
    # Dodaj CSS do stylizacji drzewa umiejętności
    st.markdown("""
    <style>
    .skill-node {
        background: linear-gradient(135deg, rgba(180, 180, 190, 0.7) 0%, rgba(150, 150, 160, 0.8) 100%);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(250, 250, 250, 0.3);
        transition: all 0.3s;
        color: rgba(20, 20, 20, 0.9);  /* Ciemniejszy tekst dla lepszej czytelności */
    }
    
    .skill-node.unlocked:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, rgba(190, 190, 200, 0.8) 0%, rgba(160, 160, 170, 0.9) 100%);
    }
    
    .skill-node.locked {
        opacity: 0.7;
        filter: grayscale(0.8);
        background: linear-gradient(135deg, rgba(150, 150, 160, 0.5) 0%, rgba(120, 120, 130, 0.6) 100%);
    }
    
    .skill-progress-bar {
        height: 8px;
        background: rgba(100,100,100,0.2);
        border-radius: 4px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .skill-progress {
        height: 100%;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 4px;
    }
    
    .level-indicator {
        font-size: 0.9rem;
        color: rgba(50,50,50,0.8);
        margin-bottom: 5px;
    }
    
    .completed-lessons {
        color: #4CAF50;
        font-size: 0.9rem;
        margin-top: 10px;
        font-weight: bold;
    }
    
    .skill-unlock-req {
        color: #ff9800;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    
    .max-level {
        color: #4CAF50;
        font-weight: bold;
        margin: 10px 0;
        text-align: center;
    }
    
    .lesson-item {
        padding: 8px;
        margin: 5px 0;
        border-radius: 5px;
        background: rgba(160, 160, 170, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .lesson-item.completed {
        border-left: 3px solid #4CAF50;
    }
    
    .lesson-item.available {
        border-left: 3px solid #2196F3;
    }
    
    .lesson-item.locked {
        border-left: 3px solid #9E9E9E;
        opacity: 0.7;
    }
    
    .lesson-status {
        font-size: 18px;
        margin-left: 10px;
    }
    
    .block-container {
        margin-bottom: 30px;
        border-bottom: 1px solid rgba(150, 150, 150, 0.2);
        padding-bottom: 20px;
    }
    
    /* Nowe style dla bloków */
    .block-header {
        background: linear-gradient(135deg, rgba(150, 150, 160, 0.6) 0%, rgba(120, 120, 130, 0.7) 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    
    /* Zmiana koloru tekstu w nagłówkach kart */
    .skill-node h4 {
        color: rgba(40, 40, 40, 0.9);
    }
    
    /* Zmiana koloru paragrafów w kartach */
    .skill-node p {
        color: rgba(50, 50, 50, 0.8);
    }
    
    /* Styl dla info-box */
    .info-box {
        background: linear-gradient(135deg, rgba(100, 180, 255, 0.2) 0%, rgba(70, 150, 220, 0.3) 100%);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(70, 150, 220, 0.3);
    }
    
    .info-box h4 {
        margin-top: 0;
        color: rgba(40, 40, 40, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)


def display_categories_in_block(block_id, categories, user_skills, user_xp, users_data, user_data, user_completed_lessons):
    """Wyświetla kategorie należące do wybranego bloku"""
    
    block_categories = [cat_id for cat_id, cat in categories.items() if cat['block'] == block_id]
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Dostosuj liczbę kolumn na podstawie urządzenia
    if device_type == 'mobile':
        # Na telefonach wyświetlamy po jednej kategorii w wierszu
        for cat_id in block_categories:
            category = categories[cat_id]
            
            # Oblicz poziom na podstawie ukończonych lekcji
            category_lessons_ids = [lesson["id"] for lesson in category['lessons']]
            completed_category_lessons = [lesson_id for lesson_id in user_completed_lessons if lesson_id in category_lessons_ids]
            lessons_completed_count = len(completed_category_lessons)
            
            # Poziom = liczba ukończonych lekcji (max 10)
            calculated_level = min(lessons_completed_count, 10)
            
            # Aktualizuj poziom w danych użytkownika jeśli się zmienił
            if calculated_level != category['level']:
                if category['id'] not in user_skills:
                    user_skills[category['id']] = {'level': 0}
                
                user_skills[category['id']]['level'] = calculated_level
                user_data['skills'] = user_skills
                users_data[st.session_state.username] = user_data
                save_user_data(users_data)
            
            # Wyświetl kartę kategorii
            progress = int((calculated_level / category['max_level']) * 100)
            st.markdown(f"""
            <div class="skill-node unlocked">
                <h4>{category['icon']} {category['name']}</h4>
                <div class="level-indicator">Poziom {calculated_level}/{category['max_level']}</div>
                <div class="skill-progress-bar">
                    <div class="skill-progress" style="width: {progress}%;"></div>
                </div>
                <p>{category['description']}</p>
                <p class="completed-lessons">Ukończone lekcje: {lessons_completed_count}/10</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Wyświetlenie lekcji dla tej kategorii
            if st.checkbox(f"Pokaż lekcje dla {category['name']}", key=f"show_lessons_{category['id']}"):
                display_category_lessons(category, calculated_level, user_completed_lessons)
    else:
        # Na tabletach i desktopach podziel kategorie na wiersze po 2 w każdym
        for i in range(0, len(block_categories), 2):
            row_categories = block_categories[i:i+2]
            cols = st.columns(len(row_categories))
            
            for j, cat_id in enumerate(row_categories):
                category = categories[cat_id]
                with cols[j]:
                    # Oblicz poziom na podstawie ukończonych lekcji
                    category_lessons_ids = [lesson["id"] for lesson in category['lessons']]
                    completed_category_lessons = [lesson_id for lesson_id in user_completed_lessons if lesson_id in category_lessons_ids]
                    lessons_completed_count = len(completed_category_lessons)
                    
                    # Poziom = liczba ukończonych lekcji (max 10)
                    calculated_level = min(lessons_completed_count, 10)
                    
                    # Aktualizuj poziom w danych użytkownika jeśli się zmienił
                    if calculated_level != category['level']:
                        if category['id'] not in user_skills:
                            user_skills[category['id']] = {'level': 0}
                        
                        user_skills[category['id']]['level'] = calculated_level
                        user_data['skills'] = user_skills
                        users_data[st.session_state.username] = user_data
                        save_user_data(users_data)
                    
                    # Wyświetl kartę kategorii
                    progress = int((calculated_level / category['max_level']) * 100)
                    st.markdown(f"""
                    <div class="skill-node unlocked">
                        <h4>{category['icon']} {category['name']}</h4>
                        <div class="level-indicator">Poziom {calculated_level}/{category['max_level']}</div>
                        <div class="skill-progress-bar">
                            <div class="skill-progress" style="width: {progress}%;"></div>
                        </div>
                        <p>{category['description']}</p>
                        <p class="completed-lessons">Ukończone lekcje: {lessons_completed_count}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Wyświetlenie lekcji dla tej kategorii
                    if st.checkbox(f"Pokaż lekcje dla {category['name']}", key=f"show_lessons_{category['id']}"):
                        display_category_lessons(category, calculated_level, user_completed_lessons)
                        
                # else:
                #     st.markdown(f"""
                #     <div class="skill-node locked">
                #         <h4>{category['icon']} {category['name']} 🔒</h4>
                #         <p>{category['description']}</p>
                #         <p class="skill-unlock-req">Wymagania: Rozwiń poprzednie umiejętności</p>
                #     </div>
                #     """, unsafe_allow_html=True)


def display_category_lessons(category, current_level, completed_lessons):
    """Wyświetla lekcje dla danej kategorii"""
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    for i, lesson in enumerate(category['lessons']):
        lesson_id = lesson['id']
        lesson_completed = lesson_id in completed_lessons
        
        # Dostosuj wygląd lekcji w zależności od urządzenia
        if device_type == 'mobile':
            # Na telefonach używamy innego układu
            if lesson_completed:
                st.markdown(f"""
                <div class="lesson-item completed">
                    <span>{lesson['title']}</span>
                    <span class="lesson-status">✅</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="lesson-item available">
                    <span>{lesson['title']}</span>
                    <span class="lesson-status">⬜</span>
                </div>
                """, unsafe_allow_html=True)
                
            # Dodaj przycisk do rozpoczęcia lekcji
            st.button("Rozpocznij lekcję", key=f"start_{lesson_id}")
        else:
            # Na tabletach i desktopach używamy kolumn
            col1, col2 = st.columns([5,1])
            
            with col1:
                if lesson_completed:
                    st.markdown(f"""
                    <div class="lesson-item completed">
                        <span>{lesson['title']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="lesson-item available">
                        <span>{lesson['title']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Przycisk do oznaczania lekcji jako ukończonej lub nieukończonej
                if lesson_completed:
                    if st.button("✅", key=f"mark_{lesson_id}", help="Oznacz jako nieukończoną"):
                        # Usuń lekcję z ukończonych
                        users_data = load_user_data()
                        user_data = users_data.get(st.session_state.username, {})
                        user_completed = set(user_data.get("completed_lessons", []))
                        user_completed.discard(lesson_id)
                        user_data["completed_lessons"] = list(user_completed)
                        users_data[st.session_state.username] = user_data
                        save_user_data(users_data)
                        st.rerun()
                else:
                    if st.button("⬜", key=f"mark_{lesson_id}", help="Oznacz jako ukończoną"):
                        # Dodaj lekcję do ukończonych
                        users_data = load_user_data()
                        user_data = users_data.get(st.session_state.username, {})
                        user_completed = set(user_data.get("completed_lessons", []))
                        user_completed.add(lesson_id)
                        user_data["completed_lessons"] = list(user_completed)
                        users_data[st.session_state.username] = user_data
                        save_user_data(users_data)
                        st.rerun()


# Usuwamy lub komentujemy tę funkcję, gdyż nie jest już potrzebna
"""
def check_category_unlocked(user_skills, required_category_id, min_level):
    # Ta funkcja nie jest już używana, ponieważ wszystkie kategorie są odblokowane
    # Pozostawiona w kodzie jako komentarz dla dokumentacji
    if required_category_id in user_skills:
        return user_skills[required_category_id].get('level', 0) >= min_level
    return False
"""


def get_lessons_for_category(category_id):
    """Generuje listę lekcji dla danej kategorii na podstawie danych kursu"""
    
    # Dane lekcji dla poszczególnych kategorii
    lessons_data = {
        1: [  # Emocje w inwestowaniu
            {"id": "B1C1L1", "title": "Strach przed stratą (loss aversion)"},
            {"id": "B1C1L2", "title": "Euforia po zyskach"},
            {"id": "B1C1L3", "title": "Regret aversion – lęk przed żalem"},
            {"id": "B1C1L4", "title": "Emocjonalna zmienność a zmienność rynku"},
            {"id": "B1C1L5", "title": "Syndrom FOMO"},
            {"id": "B1C1L6", "title": "Nadmierna pewność siebie"},
            {"id": "B1C1L7", "title": "Panika podczas korekt"},
            {"id": "B1C1L8", "title": "Złość po stracie"},
            {"id": "B1C1L9", "title": "Paraliż decyzyjny przez stres"},
            {"id": "B1C1L10", "title": "Przenoszenie emocji z życia na rynek"}
        ],
        2: [  # Neurobiologia i chemia mózgu
            {"id": "B1C2L1", "title": "Kortyzol i stres"},
            {"id": "B1C2L2", "title": "Endorfiny po porażce"},
            {"id": "B1C2L3", "title": "Dopamina i uzależnienie"},
            {"id": "B1C2L4", "title": "Serotonina a spokój"},
            {"id": "B1C2L5", "title": "Układ nagrody a ryzyko"},
            {"id": "B1C2L6", "title": "Mózg gadzi vs. racjonalny"},
            {"id": "B1C2L7", "title": "Neurofizjologia paniki"},
            {"id": "B1C2L8", "title": "Chemia decyzji"},
            {"id": "B1C2L9", "title": "Neuroplastyczność inwestora"},
            {"id": "B1C2L10", "title": "Ból społeczny i krytyka"}
        ],
        3: [  # Błędy poznawcze
            {"id": "B1C3L1", "title": "Anchoring"},
            {"id": "B1C3L2", "title": "Confirmation bias"},
            {"id": "B1C3L3", "title": "Availability bias"},
            {"id": "B1C3L4", "title": "Framing effect"},
            {"id": "B1C3L5", "title": "Status quo bias"},
            {"id": "B1C3L6", "title": "Herd behavior"},
            {"id": "B1C3L7", "title": "Iluzja kontroli"},
            {"id": "B1C3L8", "title": "Self-attribution bias"},
            {"id": "B1C3L9", "title": "Representativeness heuristic"},
            {"id": "B1C3L10", "title": "Overtrading"}
        ],
        4: [  # Ukryte filtry poznawcze
            {"id": "B2C4L1", "title": "Model SEEDS"},
            {"id": "B2C4L2", "title": "Filtr emocjonalny"},
            {"id": "B2C4L3", "title": "Filtr środowiskowy"},
            {"id": "B2C4L4", "title": "Projekcja emocji"},
            {"id": "B2C4L5", "title": "Name familiarity bias"},
            {"id": "B2C4L6", "title": "Halo effect"},
            {"id": "B2C4L7", "title": "Filtr wartości"},
            {"id": "B2C4L8", "title": "Personalizacja danych"},
            {"id": "B2C4L9", "title": "Iluzja wiedzy"},
            {"id": "B2C4L10", "title": "Efekt pierwszeństwa i świeżości"}
        ],
        5: [  # Zarządzanie sobą
            {"id": "B2C5L1", "title": "Mindfulness"},
            {"id": "B2C5L2", "title": "Rytuały dnia"},
            {"id": "B2C5L3", "title": "Znaczenie snu"},
            {"id": "B2C5L4", "title": "Detox cyfrowy"},
            {"id": "B2C5L5", "title": "Dziennik emocji"},
            {"id": "B2C5L6", "title": "Refleksja tygodniowa"},
            {"id": "B2C5L7", "title": "Zasada STOP"},
            {"id": "B2C5L8", "title": "Self-care jako strategia"},
            {"id": "B2C5L9", "title": "Prośba o wsparcie"},
            {"id": "B2C5L10", "title": "Asertywność decyzyjna"}
        ],
        6: [  # Rozwój osobisty
            {"id": "B2C6L1", "title": "Kaizen"},
            {"id": "B2C6L2", "title": "Mikrocele"},
            {"id": "B2C6L3", "title": "Refleksja poranna i wieczorna"},
            {"id": "B2C6L4", "title": "Praca nad mindsetem"},
            {"id": "B2C6L5", "title": "Kompas inwestycyjny"},
            {"id": "B2C6L6", "title": "Eliminacja rozpraszaczy"},
            {"id": "B2C6L7", "title": "Zarządzanie energią"},
            {"id": "B2C6L8", "title": "Rytuały bezpieczeństwa"},
            {"id": "B2C6L9", "title": "Analiza sukcesów i błędów"},
            {"id": "B2C6L10", "title": "Planowanie odporności psychicznej"}
        ],
        7: [  # Decyzyjność
            {"id": "B2C7L1", "title": "Systemy decyzyjne"},
            {"id": "B2C7L2", "title": "Checklisty"},
            {"id": "B2C7L3", "title": "Decyzje warunkowe"},
            {"id": "B2C7L4", "title": "Fakty vs emocje"},
            {"id": "B2C7L5", "title": "Alternatywy"},
            {"id": "B2C7L6", "title": "Sygnały vs szum"},
            {"id": "B2C7L7", "title": "Scenariusze decyzyjne"},
            {"id": "B2C7L8", "title": "Tempo decyzji"},
            {"id": "B2C7L9", "title": "Presja czasu"},
            {"id": "B2C7L10", "title": "Zmiana zdania bez żalu"}
        ],
        8: [  # Metapoznanie
            {"id": "B3C8L1", "title": "Obserwacja myśli"},
            {"id": "B3C8L2", "title": "Myśli ≠ fakty"},
            {"id": "B3C8L3", "title": "Refleksyjność strategiczna"},
            {"id": "B3C8L4", "title": "Skrypty mentalne"},
            {"id": "B3C8L5", "title": "Źródła emocji"},
            {"id": "B3C8L6", "title": "Moment wyboru"},
            {"id": "B3C8L7", "title": "Automatyzm decyzyjny"},
            {"id": "B3C8L8", "title": "Samoocena decyzji"},
            {"id": "B3C8L9", "title": "Praca z intuicją"},
            {"id": "B3C8L10", "title": "Introspekcja po transakcji"}
        ],
        9: [  # Styl inwestora
            {"id": "B3C9L1", "title": "Rozpoznanie stylu"},
            {"id": "B3C9L2", "title": "Spójność stylu i strategii"},
            {"id": "B3C9L3", "title": "Ja-osoba vs ja-inwestor"},
            {"id": "B3C9L4", "title": "Cele długoterminowe"},
            {"id": "B3C9L5", "title": "Mapa tożsamości decyzyjnej"},
            {"id": "B3C9L6", "title": "Zaufanie do siebie"},
            {"id": "B3C9L7", "title": "Odzwyczajenie od rynku"},
            {"id": "B3C9L8", "title": "Granice zaangażowania"},
            {"id": "B3C9L9", "title": "Dialog wewnętrzny"},
            {"id": "B3C9L10", "title": "Pytanie 'po co inwestuję?'"}
        ],
        10: [  # Odporność i adaptacja
            {"id": "B4C10L1", "title": "Budowanie odporności"},
            {"id": "B4C10L2", "title": "Zarządzanie stresem chronicznym"},
            {"id": "B4C10L3", "title": "Odporność na niepewność"},
            {"id": "B4C10L4", "title": "Szybka regeneracja"},
            {"id": "B4C10L5", "title": "Lekcje z błędów"},
            {"id": "B4C10L6", "title": "Akceptacja pomyłek"},
            {"id": "B4C10L7", "title": "Elastyczność poznawcza"},
            {"id": "B4C10L8", "title": "Tolerancja niejasności"},
            {"id": "B4C10L9", "title": "Oddzielenie od wyniku"},
            {"id": "B4C10L10", "title": "Powrót do równowagi"}
        ],
        11: [  # Interakcje społeczne i środowisko inwestora
            {"id": "B5C11L1", "title": "Wpływ otoczenia (grupa, rodzina, media)"},
            {"id": "B5C11L2", "title": "Porównywanie się z innymi inwestorami"},
            {"id": "B5C11L3", "title": "Zarządzanie krytyką i opiniami innych"},
            {"id": "B5C11L4", "title": "Rola coacha, mentora, społeczności"},
            {"id": "B5C11L5", "title": "Efekt 'influencera' - jak go rozpoznać i neutralizować"},
            {"id": "B5C11L6", "title": "Komunikacja z partnerem o finansach"},
            {"id": "B5C11L7", "title": "Samotność inwestora - jak jej przeciwdziałać"},
            {"id": "B5C11L8", "title": "Odpowiedzialność społeczna inwestowania"},
            {"id": "B5C11L9", "title": "Inwestowanie w zgodzie z wartościami"},
            {"id": "B5C11L10", "title": "Wspólne inwestowanie - szanse i zagrożenia"}
        ],
        12: [  # Testowanie i analiza własnych strategii
            {"id": "B4C12L1", "title": "Budowanie hipotez inwestycyjnych"},
            {"id": "B4C12L2", "title": "Testowanie scenariuszy w symulacjach"},
            {"id": "B4C12L3", "title": "Retrospektywna analiza transakcji"},
            {"id": "B4C12L4", "title": "Określanie stref emocjonalnych w strategii"},
            {"id": "B4C12L5", "title": "Adaptowanie systemów do własnej osobowości"},
            {"id": "B4C12L6", "title": "Tworzenie mapy błędów poznawczych"},
            {"id": "B4C12L7", "title": "Analiza 'momentów przełomowych' w portfelu"},
            {"id": "B4C12L8", "title": "Definiowanie poziomów komfortu i niepewności"},
            {"id": "B4C12L9", "title": "Praca na danych z dziennika inwestycyjnego"},
            {"id": "B4C12L10", "title": "Eksperymenty z różnymi stylami decyzji"}
        ],
        13: [  # Elastyczność, transformacja i rozwój
            {"id": "B4C13L1", "title": "Cykl przemian inwestora"},
            {"id": "B4C13L2", "title": "Praca z oporem przed zmianą"},
            {"id": "B4C13L3", "title": "Budowanie nowej tożsamości po kryzysie"},
            {"id": "B4C13L4", "title": "Przejście z intuicji do struktury i odwrotnie"},
            {"id": "B4C13L5", "title": "Przeformułowywanie porażek na rozwój"},
            {"id": "B4C13L6", "title": "Transformacja podejścia do ryzyka"},
            {"id": "B4C13L7", "title": "Kultura nieperfekcyjności i ryzyka"},
            {"id": "B4C13L8", "title": "Trening elastyczności poznawczej"},
            {"id": "B4C13L9", "title": "Tworzenie 'psychicznego kapitału'"},
            {"id": "B4C13L10", "title": "Długoterminowa transformacja mentalna inwestora"}
        ],
        14: [  # Motywacja i sens działania
            {"id": "B3C14L1", "title": "Budowanie wewnętrznej motywacji inwestycyjnej"},
            {"id": "B3C14L2", "title": "Różnica między celem a intencją"},
            {"id": "B3C14L3", "title": "Autodyscyplina a motywacja chwilowa"},
            {"id": "B3C14L4", "title": "Ustalanie priorytetów wewnętrznych"},
            {"id": "B3C14L5", "title": "Świadomość konsekwencji emocjonalnych"},
            {"id": "B3C14L6", "title": "Motywacja oparta na wartościach"},
            {"id": "B3C14L7", "title": "Zastosowanie afirmacji i wizualizacji"},
            {"id": "B3C14L8", "title": "Znaczenie postawy 'growth mindset'"},
            {"id": "B3C14L9", "title": "Praca z przekonaniami ograniczającymi"},
            {"id": "B3C14L10", "title": "Inwestowanie jako wyraz tożsamości"}
        ],
        15: [  # Mistrzostwo psychologiczne
            {"id": "B5C15L1", "title": "Samoświadomość jako klucz do sukcesu"},
            {"id": "B5C15L2", "title": "Codzienne zarządzanie sobą w działaniu"},
            {"id": "B5C15L3", "title": "Zarządzanie impulsami - odraczanie decyzji"},
            {"id": "B5C15L4", "title": "Świadomość kosztu mentalnego transakcji"},
            {"id": "B5C15L5", "title": "Przejście od reakcji do odpowiedzi"},
            {"id": "B5C15L6", "title": "Mistrzostwo emocjonalne jako proces"},
            {"id": "B5C15L7", "title": "Umiejętność 'myślenia długiego'"},
            {"id": "B5C15L8", "title": "Integracja wszystkich poziomów inwestora"},
            {"id": "B5C15L9", "title": "Świadomy inwestor - człowiek w równowadze"},
            {"id": "B5C15L10", "title": "Podejście holistyczne w inwestowaniu"}
        ]
    }
    
    return lessons_data.get(category_id, [])