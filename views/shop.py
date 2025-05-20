import streamlit as st
from data.users import load_user_data, save_user_data
from utils.components import zen_button, notification, zen_header, add_animations_css
from utils.material3_components import apply_material3_theme 
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view

def show_shop():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    st.title("Sklep 🛒")
      # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Dodaj style dla wyświetlania waluty
    st.markdown("""
    <style>
    .coin-display {
        background-color: #FFFDE7;
        padding: 12px 16px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        font-size: 18px;
    }
    
    .coin-amount {
        color: #FF6D00;
        font-weight: 700;
        margin: 0 8px;
        font-size: 20px;
    }
    
    /* Responsywny styl dla wyświetlania waluty */
    @media (max-width: 640px) {
        .coin-display {
            padding: 8px 12px;
            font-size: 16px;
            margin-bottom: 15px;
        }
        
        .coin-amount {
            font-size: 18px;
            margin: 0 6px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Wirtualna waluta użytkownika
    degen_coins = user_data.get('degen_coins', 0)
    st.markdown(f"<div class='coin-display'>🪙 <span class='coin-amount'>{degen_coins}</span> DegenCoins</div>", unsafe_allow_html=True)
    
    # Dodaj style dla zakładek w sklepie
    st.markdown("""
    <style>
    /* Style dla zakładek w sklepie */
    .tab-container {
        margin-bottom: 20px;
    }
    
    /* Responsywne style dla zakładek */
    @media (max-width: 640px) {
        /* Na mobilnych urządzeniach zmniejszamy padding w zakładkach */
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 14px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Kategorie produktów z responsywnym kontenerem
    with st.container():
        categories = st.tabs(["Awatary", "Tła", "Specjalne lekcje", "Boostery"])
    
    with categories[0]:
        # Awatary dostępne w sklepie
        avatars = [
            {"id": "diamond_degen", "name": "Diamond Degen", "icon": "💎", "price": 500, "owned": "diamond_degen" in user_data.get('owned_avatars', [])},
            {"id": "crypto_wizard", "name": "Crypto Wizard", "icon": "🧙", "price": 750, "owned": "crypto_wizard" in user_data.get('owned_avatars', [])},
            {"id": "moon_hunter", "name": "Moon Hunter", "icon": "🌕", "price": 1000, "owned": "moon_hunter" in user_data.get('owned_avatars', [])}
        ]
        
        # Wyświetl awatary w responsywnej siatce
        cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
        
        # Dodaj style dla kart produktów
        st.markdown("""
        <style>
        /* Style dla kart produktów w sklepie */
        .shop-item {
            background-color: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .shop-item:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        .shop-item.owned {
            background-color: #F5F5F5;
            border: 2px solid #4CAF50;
        }
        
        .shop-item-icon {
            font-size: 2.5rem;
            margin: 10px 0;
        }
        
        .shop-item-name {
            font-weight: 500;
            font-size: 1.2rem;
            margin: 10px 0;
            color: #1A237E;
        }
        
        .shop-item-price, .shop-item-status {
            font-size: 1rem;
            margin: 10px 0;
            font-weight: 500;
        }
        
        .shop-item-status {
            color: #4CAF50;
        }
        
        .shop-buy-btn, .shop-use-btn {
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 24px;
            padding: 8px 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
            box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3);
        }
        
        .shop-buy-btn:hover, .shop-use-btn:hover {
            background-color: #1976D2;
            box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4);
        }
        
        .shop-use-btn {
            background-color: #4CAF50;
            box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);
        }
        
        .shop-use-btn:hover {
            background-color: #388E3C;
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.4);
        }
        
        /* Responsywne style dla różnych urządzeń */
        @media (max-width: 640px) {
            .shop-item {
                padding: 15px;
            }
            
            .shop-item-icon {
                font-size: 2rem;
                margin: 5px 0;
            }
            
            .shop-item-name {
                font-size: 1rem;
                margin: 5px 0;
            }
            
            .shop-buy-btn, .shop-use-btn {
                padding: 6px 12px;
                font-size: 0.9rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        for i, avatar in enumerate(avatars):
            with cols[i % len(cols)]:
                if avatar["owned"]:
                    st.markdown(f"""
                    <div class="shop-item owned">
                        <div class="shop-item-icon">{avatar['icon']}</div>
                        <div class="shop-item-name">{avatar['name']}</div>
                        <div class="shop-item-status">Posiadasz</div>
                        <button class="shop-use-btn">Użyj</button>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="shop-item">
                        <div class="shop-item-icon">{avatar['icon']}</div>
                        <div class="shop-item-name">{avatar['name']}</div>
                        <div class="shop-item-price">🪙 {avatar['price']}</div>
                        <button class="shop-buy-btn">Kup</button>
                    </div>
                    """, unsafe_allow_html=True)
    
    with categories[1]:
        # Tła dostępne w sklepie
        backgrounds = [
            {"id": "crypto_city", "name": "Crypto City", "icon": "🏙️", "price": 400, "owned": "crypto_city" in user_data.get('owned_backgrounds', [])},
            {"id": "moon_landscape", "name": "Moon Landscape", "icon": "🌙", "price": 600, "owned": "moon_landscape" in user_data.get('owned_backgrounds', [])},
            {"id": "virtual_grid", "name": "Virtual Grid", "icon": "🌐", "price": 800, "owned": "virtual_grid" in user_data.get('owned_backgrounds', [])}
        ]
        
        # Użyj responsywnej siatki
        bg_cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
        
        for i, bg in enumerate(backgrounds):
            with bg_cols[i % len(bg_cols)]:
                if bg["owned"]:
                    st.markdown(f"""
                    <div class="shop-item owned">
                        <div class="shop-item-icon">{bg['icon']}</div>
                        <div class="shop-item-name">{bg['name']}</div>
                        <div class="shop-item-status">Posiadasz</div>
                        <button class="shop-use-btn">Ustaw</button>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="shop-item">
                        <div class="shop-item-icon">{bg['icon']}</div>
                        <div class="shop-item-name">{bg['name']}</div>
                        <div class="shop-item-price">🪙 {bg['price']}</div>
                        <button class="shop-buy-btn">Kup</button>
                    </div>
                    """, unsafe_allow_html=True)
                
    with categories[2]:
        # Specjalne lekcje dostępne w sklepie
        special_lessons = [
            {"id": "advanced_defi", "name": "Advanced DeFi Strategies", "icon": "📚", "price": 1500, "owned": "advanced_defi" in user_data.get('owned_special_lessons', [])},
            {"id": "nft_masterclass", "name": "NFT Masterclass", "icon": "🖼️", "price": 1200, "owned": "nft_masterclass" in user_data.get('owned_special_lessons', [])},
            {"id": "crypto_trading", "name": "Crypto Trading Pro", "icon": "📈", "price": 2000, "owned": "crypto_trading" in user_data.get('owned_special_lessons', [])}
        ]
        
        # Styl dla specjalnych lekcji (bardziej premium)
        st.markdown("""
        <style>
        .special-lesson {
            background: linear-gradient(135deg, #FFFFFF, #F5F5F5);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .special-lesson::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #FF6D00, #FFD700);
        }
        
        .special-lesson:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            transform: translateY(-3px);
        }
        
        .special-lesson.owned::before {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
        }
        
        .special-lesson-icon {
            font-size: 2.8rem;
            margin: 10px 0;
            display: inline-block;
        }
        
        .special-lesson-name {
            font-weight: 600;
            font-size: 1.3rem;
            margin: 12px 0;
            color: #1A237E;
        }
        
        .special-lesson-price {
            font-size: 1.1rem;
            font-weight: 500;
            margin: 12px 0;
            color: #FF6D00;
        }
        
        .special-lesson-status {
            font-size: 1.1rem;
            font-weight: 500;
            margin: 12px 0;
            color: #4CAF50;
        }
        
        .special-lesson-desc {
            color: #555;
            margin: 12px 0;
            line-height: 1.4;
        }
        
        .premium-btn {
            background: linear-gradient(90deg, #FF6D00, #FF9800);
            color: white;
            border: none;
            border-radius: 24px;
            padding: 10px 20px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 15px;
            box-shadow: 0 4px 8px rgba(255, 109, 0, 0.3);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .premium-btn:hover {
            background: linear-gradient(90deg, #F57C00, #FFA726);
            box-shadow: 0 6px 12px rgba(255, 109, 0, 0.4);
            transform: translateY(-1px);
        }
        
        .premium-use-btn {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
        }
        
        .premium-use-btn:hover {
            background: linear-gradient(90deg, #388E3C, #7CB342);
            box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4);
        }
        
        /* Responsywne style dla specjalnych lekcji */
        @media (max-width: 640px) {
            .special-lesson {
                padding: 18px;
            }
            
            .special-lesson-icon {
                font-size: 2.2rem;
            }
            
            .special-lesson-name {
                font-size: 1.1rem;
                margin: 8px 0;
            }
            
            .special-lesson-price, .special-lesson-status {
                font-size: 1rem;
                margin: 8px 0;
            }
            
            .special-lesson-desc {
                font-size: 0.9rem;
                margin: 8px 0;
            }
            
            .premium-btn {
                padding: 8px 16px;
                font-size: 0.9rem;
                margin-top: 10px;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Używamy responsywnej siatki
        lesson_cols = responsive_grid(columns_desktop=3, columns_tablet=2, columns_mobile=1)
        
        for i, lesson in enumerate(special_lessons):
            with lesson_cols[i % len(lesson_cols)]:
                lesson_description = {
                    "advanced_defi": "Zaawansowane strategie DeFi i zarządzanie portfelem.",
                    "nft_masterclass": "Tworzenie, kolekcjonowanie i analiza rynku NFT.",
                    "crypto_trading": "Profesjonalne strategie tradingowe dla kryptowalut."
                }.get(lesson["id"], "Specjalna lekcja dla zaawansowanych użytkowników.")
                
                if lesson["owned"]:
                    st.markdown(f"""
                    <div class="special-lesson owned">
                        <div class="special-lesson-icon">{lesson['icon']}</div>
                        <div class="special-lesson-name">{lesson['name']}</div>
                        <div class="special-lesson-status">Zakupiona</div>
                        <div class="special-lesson-desc">{lesson_description}</div>
                        <button class="premium-btn premium-use-btn">Rozpocznij lekcję</button>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="special-lesson">
                        <div class="special-lesson-icon">{lesson['icon']}</div>
                        <div class="special-lesson-name">{lesson['name']}</div>
                        <div class="special-lesson-price">🪙 {lesson['price']}</div>
                        <div class="special-lesson-desc">{lesson_description}</div>
                        <button class="premium-btn">Kup teraz</button>
                    </div>
                    """, unsafe_allow_html=True)
                
    with categories[3]:
        # Boostery dostępne w sklepie
        boosters = [
            {"id": "double_xp", "name": "2x XP Boost", "icon": "⚡", "price": 300, "duration": "24 godziny"},
            {"id": "extra_coins", "name": "Extra Coins", "icon": "💰", "price": 250, "duration": "7 dni"},
            {"id": "vip_access", "name": "VIP Access", "icon": "🌟", "price": 500, "duration": "30 dni"}
        ]
        
        # Styl dla boosterów
        st.markdown("""
        <style>
        .booster-item {
            background: linear-gradient(135deg, #FFFFFF, #F0F8FF);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
            border-left: 4px solid #2196F3;
        }
        
        .booster-item:hover {
            box-shadow: 0 6px 14px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        .booster-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .booster-icon {
            font-size: 2.2rem;
            margin-right: 15px;
        }
        
        .booster-name {
            font-weight: 600;
            font-size: 1.2rem;
            color: #1A237E;
        }
        
        .booster-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
        }
        
        .booster-price {
            font-size: 1.1rem;
            font-weight: 500;
            color: #FF6D00;
        }
        
        .booster-duration {
            font-size: 0.9rem;
            color: #555;
            background-color: rgba(33, 150, 243, 0.1);
            padding: 5px 10px;
            border-radius: 12px;
        }
        
        .booster-description {
            color: #555;
            margin: 10px 0;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        
        .booster-buy-btn {
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 24px;
            padding: 8px 18px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 3px 6px rgba(33, 150, 243, 0.3);
            display: block;
            margin-left: auto;
        }
        
        .booster-buy-btn:hover {
            background-color: #1976D2;
            box-shadow: 0 5px 10px rgba(33, 150, 243, 0.4);
        }
        
        /* Responsywne style dla boosterów */
        @media (max-width: 640px) {
            .booster-item {
                padding: 15px;
            }
            
            .booster-icon {
                font-size: 1.8rem;
                margin-right: 10px;
            }
            
            .booster-name {
                font-size: 1rem;
            }
            
            .booster-info {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
            
            .booster-price {
                font-size: 1rem;
            }
            
            .booster-duration {
                font-size: 0.8rem;
            }
            
            .booster-description {
                font-size: 0.85rem;
            }
            
            .booster-buy-btn {
                padding: 6px 14px;
                font-size: 0.9rem;
                margin: 10px 0 0 0;
                width: 100%;
                text-align: center;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Używamy responsywnej siatki
        booster_cols = responsive_grid(columns_desktop=2, columns_tablet=1, columns_mobile=1)
        
        booster_descriptions = {
            "double_xp": "Podwaja zdobywane punkty doświadczenia we wszystkich lekcjach i quizach.",
            "extra_coins": "Zwiększa zdobywane DegenCoiny o 50% za wszystkie wykonane zadania.",
            "vip_access": "Dostęp do ekskluzywnych treści, wydarzeń VIP i dodatkowych lekcji."
        }
        
        for i, booster in enumerate(boosters):
            with booster_cols[i % len(booster_cols)]:
                st.markdown(f"""
                <div class="booster-item">
                    <div class="booster-header">
                        <div class="booster-icon">{booster['icon']}</div>
                        <div class="booster-name">{booster['name']}</div>
                    </div>
                    <div class="booster-description">{booster_descriptions.get(booster['id'], 'Booster zwiększający postępy w nauce.')}</div>
                    <div class="booster-info">
                        <div class="booster-price">🪙 {booster['price']}</div>
                        <div class="booster-duration">⏱️ {booster['duration']}</div>
                    </div>
                    <button class="booster-buy-btn">Aktywuj booster</button>
                </div>
                """, unsafe_allow_html=True)

    # Funkcja obsługi zakupów (placeholder)
    if st.session_state.get('purchase_made'):
        st.success("Zakup został zrealizowany pomyślnie!")
        st.session_state.purchase_made = False