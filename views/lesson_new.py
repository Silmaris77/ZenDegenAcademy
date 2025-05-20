import streamlit as st
from data.lessons import load_lessons
from data.users import load_user_data, save_user_data
from utils.components import zen_header, zen_button, notification, content_section, tip_block, quote_block, progress_bar, embed_content, lesson_card
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view

def get_difficulty_stars(difficulty):
    """Konwertuje poziom trudności (liczba lub tekst) na odpowiednią liczbę gwiazdek."""
    difficulty_map = {
        "beginner": 1,
        "podstawowy": 1,
        "intermediate": 2,
        "średni": 2,
        "średniozaawansowany": 3,
        "advanced": 4,
        "zaawansowany": 4,
        "expert": 5,
        "ekspercki": 5
    }
    
    if isinstance(difficulty, str):
        difficulty_level = difficulty_map.get(difficulty.lower(), 1)
    else:
        try:
            difficulty_level = int(difficulty)
        except (ValueError, TypeError):
            difficulty_level = 1
    
    return '⭐' * difficulty_level

def show_lesson():
    """Show lesson view"""
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Kurs Zen Degen Academy")
    lessons = load_lessons()
    
    # Check if we're viewing a specific lesson or the overview
    if 'current_lesson' not in st.session_state or not st.session_state.current_lesson:
        # WIDOK PRZEGLĄDU LEKCJI
        st.subheader("Dostępne lekcje")
        
        # Pobierz dane użytkownika dla oznaczenia ukończonych lekcji
        users_data = load_user_data()
        user_data = users_data.get(st.session_state.username, {})
        completed_lessons = user_data.get('completed_lessons', [])
        
        # Grupuj lekcje według kategorii
        lessons_by_category = {}
        for lesson_id, lesson in lessons.items():
            category = lesson.get("category", "Inne")
            if category not in lessons_by_category:
                lessons_by_category[category] = []
            lessons_by_category[category].append((lesson_id, lesson))
          # Wyświetl lekcje w podziale na kategorie
        for category, category_lessons in lessons_by_category.items():
            st.markdown(f"## {category}")
            
            # Zastosuj responsywną siatkę dla lekcji, zależnie od urządzenia
            lesson_cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
            
            # Wyświetlaj karty lekcji w responsywnej siatce
            for i, (lesson_id, lesson) in enumerate(category_lessons):
                # Sprawdź, czy lekcja jest ukończona
                is_completed = lesson_id in completed_lessons
                
                # Szacowanie czasu na podstawie długości treści
                content_length = len(lesson.get('description', '')) + sum(len(section.get('content', '')) 
                                                        for section in lesson.get('sections', {}).get('learning', {}).get('sections', []))
                estimated_minutes = max(1, round(content_length / 1000))
                
                # Użyj odpowiedniej kolumny z responsywnego gridu
                col_index = i % len(lesson_cols)
                with lesson_cols[col_index]:
                    # Użyj komponentu lesson_card zamiast ręcznego HTML
                    lesson_card(
                    title=lesson.get('title', 'Lekcja'),
                    description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                    xp=lesson.get('xp_reward', 30),
                    duration=estimated_minutes,
                    difficulty=lesson.get('difficulty', 'beginner'),
                    category=lesson.get('tag', category),
                    completed=is_completed,
                    button_text="Powtórz lekcję" if is_completed else "Rozpocznij",
                    button_key=f"start_{lesson_id}",
                    lesson_id=lesson_id,
                    on_click=lambda lesson_id=lesson_id: (
                        setattr(st.session_state, 'current_lesson', lesson_id),
                        setattr(st.session_state, 'lesson_step', 'intro'),
                        setattr(st.session_state, 'quiz_score', 0) if 'quiz_score' in st.session_state else None,
                        st.rerun()
                    )
                )
    else:
        # Kod wyświetlania pojedynczej lekcji (całość twojego obecnego kodu)
        lesson_id = st.session_state.current_lesson
        if lesson_id not in lessons:
            st.error("Nie znaleziono wybranej lekcji.")
            return
            
        lesson = lessons[lesson_id]
        
        if 'lesson_step' not in st.session_state:
            st.session_state.lesson_step = 'intro'
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0

        # Lesson navigation in sidebar
        with st.sidebar:
            st.markdown("<h3>Nawigacja lekcji</h3>", unsafe_allow_html=True)
            
            # Dodaj przycisk powrotu do przeglądu lekcji
            if zen_button("Wszystkie lekcje", use_container_width=True):
                st.session_state.current_lesson = None
                st.rerun()
            
            # Define all lesson steps
            lesson_steps = {
                'intro': 'Wprowadzenie',
                'content': 'Merytoryka',
                'reflection': 'Refleksja i Praktyka',
                'application': 'Implementacja',
                'summary': 'Podsumowanie'
            }
            
            # Create navigation buttons
            for step, name in lesson_steps.items():
                if zen_button(
                    name, 
                    key=f"nav_{step}",
                    disabled=st.session_state.lesson_step == step,
                    use_container_width=True
                ):
                    st.session_state.lesson_step = step
                    st.rerun()

            if zen_button("Powrót do dashboard", use_container_width=True):
                st.session_state.lesson_step = 'intro'
                st.session_state.page = 'dashboard'
                st.rerun()
                
        # Main content
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        
        # Main content logic for each step
        if st.session_state.lesson_step == 'intro':
            content_section("Wprowadzenie", lesson["intro"], collapsed=False)

        elif st.session_state.lesson_step == 'content':
            for section in lesson["sections"]["learning"]["sections"]:
                content_section(
                    section["title"], 
                    section["content"], 
                    collapsed=True  # Zmiana z False na True, aby sekcje były domyślnie zwinięte
                )
                
        elif st.session_state.lesson_step == 'reflection':
            # Wersja zabezpieczona przed KeyError:
            if "reflection" in lesson.get("sections", {}) and "sections" in lesson["sections"].get("reflection", {}):
                for section in lesson["sections"]["reflection"]["sections"]:
                    # Use the new embed_content component
                    embed_content(
                        url="https://www.canva.com/design/DAGElemhrt0/-yw2s6fJnKLvyKvz1NDuTA/view?embed",
                        width="1200",
                        height="800",
                        title=section["title"]
                    )
            else:
                # Obsługa przypadku, gdy struktura danych nie zawiera oczekiwanych kluczy
                st.warning("Brak sekcji refleksji dla tej lekcji.")
                
        elif st.session_state.lesson_step == 'summary':
            total_xp = st.session_state.quiz_score + lesson["xp_reward"]

            users_data = load_user_data()
            user_data = users_data[st.session_state.username]

            if lesson_id not in user_data.get('completed_lessons', []):
                user_data['xp'] = user_data.get('xp', 0) + total_xp
                if 'completed_lessons' not in user_data:
                    user_data['completed_lessons'] = []            
                user_data['completed_lessons'].append(lesson_id)
                users_data[st.session_state.username] = user_data
                save_user_data(users_data)

                notification(f"""
                🎉 Gratulacje! Ukończyłeś lekcję!

                Zdobyte punkty:
                - Quiz: {st.session_state.quiz_score} XP
                - Ukończenie lekcji: {lesson["xp_reward"]} XP
                - Łącznie: {total_xp} XP
                """, type="success")

            if zen_button("Powrót do dashboardu"):
                st.session_state.lesson_step = 'intro'
                st.session_state.current_quiz_step = 0
                st.session_state.closing_quiz_step = 0
                st.session_state.quiz_score = 0
                st.session_state.page = 'dashboard'
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
