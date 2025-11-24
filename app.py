import streamlit as st
from PIL import Image, ExifTags
import numpy as np
from utils.doencas import get_doencas, exibir_doenca
import importlib
from streamlit_option_menu import option_menu
from streamlit_geolocation import streamlit_geolocation
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from utils.auth_config import setup_authenticator
from utils.location import display_location
from utils.image_processing import preprocess_image
from utils.db_operations import save_scan, get_disease_by_name, is_user_admin
from utils.auth import get_user_id, get_user_id_from_db

def get_gps_coordinates(image):
    try:
        exif_data = image._getexif()
        if exif_data is None:
            return None

        gps_info = {}
        for tag_id, value in exif_data.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            if tag == 'GPSInfo':
                for key, val in value.items():
                    sub_tag = ExifTags.GPSTAGS.get(key, key)
                    gps_info[sub_tag] = val

        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
            lat = convert_to_decimal(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])
            lon = convert_to_decimal(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])
            return lat, lon
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao obter coordenadas GPS: {e}")
        return None

def convert_to_decimal(dms, ref):
    degrees, minutes, seconds = dms
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

#Função para obter o nome da cidade a partir das coordenadas
def get_city_from_coords(lat, lon):   
    try:
        geolocator = Nominatim(user_agent="haber_app")
        location = geolocator.reverse((lat, lon), language='pt')
        if location and location.raw.get('address'):
            address = location.raw['address']
            city = address.get('city') or address.get('town') or address.get('village')
            state = address.get('state')
            if city and state:
                return f"{city}, {state}"
            return "Localização encontrada"
    except (GeocoderTimedOut, Exception) as e:
        return None
    return None

# Função para obter localização baseada no IP
def get_location_from_ip():
    try:
        response = requests.get('https://ipapi.co/json/')
        if response.status_code == 200:
            data = response.json()
            lat = data.get('latitude')
            lon = data.get('longitude')
            if lat and lon:
                return (float(lat), float(lon)), "IP"
    except Exception as e:
        st.error(f"Erro ao obter localização por IP: {str(e)}")
    return None, None

def get_location(image=None):
    """Função que implementa a estratégia de localização em camadas"""
    location = None
    location_source = None
    
    # Variáveis de estado para controle de UI
    if 'location_error' not in st.session_state:
        st.session_state.location_error = None
    if 'show_manual_input' not in st.session_state:
        st.session_state.show_manual_input = False
    if 'retry_count' not in st.session_state:
        st.session_state.retry_count = 0
    if 'using_ip_location' not in st.session_state:
        st.session_state.using_ip_location = False

    # Tentativa 1: Dados EXIF
    if image is not None:
        coordinates = get_gps_coordinates(image)
        if coordinates:
            location = coordinates
            location_source = "EXIF"
            st.success("✅ Localização detectada automaticamente a partir da imagem!")
            return location, location_source

    # Tentativa 2: Localização por IP
    if not location:
        location, source = get_location_from_ip()
        if location:
            location_source = source
            return location, location_source

    # Se nenhuma localização foi encontrada, retorna None
    return None, None

st.set_page_config(
    page_title="Haber",
    page_icon="images/haber.png"
)

# Inicializa o authenticator
authenticator = setup_authenticator()

# Tenta fazer login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Usuário ou senha incorretos')
elif authentication_status == None:
    st.info('Por favor, insira seu usuário e senha')
elif authentication_status:
    st.session_state['username'] = username
    st.session_state['user_id'] = get_user_id_from_db(username)
    # Usuário está logado
    st.sidebar.image("images/haber_logo.png", width=200)

    # Verifica se o usuário é admin
    user_id = st.session_state['user_id']
    is_admin = is_user_admin(user_id)

    # Define menu dinâmico baseado em permissões
    if is_admin:
        menu_items = ["Home", 'Doenças', 'Modelo', 'Histórico', 'Admin']
        menu_icons = ['house', 'search', 'info-circle', 'collection', 'shield-lock']
    else:
        menu_items = ["Home", 'Doenças', 'Modelo', 'Histórico']
        menu_icons = ['house', 'search', 'info-circle', 'collection']

    with st.sidebar:
        selected = option_menu(
            '',
            menu_items,
            icons=menu_icons,
            default_index=0,
            menu_icon="cast",
            styles={
                "container": {"background-color": "#2D2D2D"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {"color": "white", "font-weight": "bold"},
                "nav-link-selected": {"background-color": "green", "color": "white"}
            }
        )
        # Botão de logout na sidebar
        authenticator.logout('Logout', 'sidebar')

    if selected == "Doenças":
        doenças_module = importlib.import_module('paginas.doencas')
        doenças_module.display_content()
    elif selected == "Modelo":
        modelo_module = importlib.import_module('paginas.modelo')
        modelo_module.display_content()
    elif selected == "Histórico":
        historico_module = importlib.import_module('paginas.historico')
        historico_module.display_content()
    elif selected == "Admin":
        admin_module = importlib.import_module('paginas.admin')
        admin_module.display_content()
    elif selected == "Home":
        st.title('🪲 Identificação de Doenças em Folhas de Soja')

        uploaded_file = st.file_uploader("📷 Envie uma imagem de folha de soja", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagem carregada", use_column_width=True)

            image_array = preprocess_image(image)

            class_names = [
                'Mossaic Virus',
                'Southern Blight',
                'Sudden Death Syndrome',
                'Yellow Mosaic',
                'Bacterial Blight',
                'Brown Spot',
                'Crestamento',
                'Ferrugem',
                'Powdery Mildew',
                'Septoria'
            ]

            predicted_class = class_names[0]  # Placeholder fixo
            confidence = 0.95

            # Salva os dados no session_state
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['predicted_class'] = predicted_class
            st.session_state['confidence'] = confidence

            st.markdown(f"### 🧠 Predição: **{predicted_class}**")
            st.write(f"Confiabilidade: {confidence * 100:.2f}%")

            doencas = get_doencas()
            if predicted_class in doencas:
                st.markdown("## 📖 Detalhes sobre a doença detectada:")
                exibir_doenca(predicted_class, doencas[predicted_class])
            else:
                st.info("Nenhuma informação detalhada disponível para essa doença.")

            # Fluxo de localização
            if 'location_confirmed' not in st.session_state or not st.session_state['location_confirmed']:
                st.markdown("### 📍 Confirme sua localização para salvar a análise")
                location_method = st.radio(
                    "Como deseja informar sua localização?",
                    ["Digitar Cidade", "Selecionar no Mapa", "Baseado em IP"],
                    key="location_method"
                )
                if location_method == "Digitar Cidade":
                    city = st.text_input("Digite sua cidade:", key="city_input")
                    if st.button("Confirmar localização (cidade)") and city:
                        geolocator = Nominatim(user_agent="haber_app")
                        location_data = geolocator.geocode(city + ", Brasil")
                        if location_data:
                            st.session_state['latitude'] = location_data.latitude
                            st.session_state['longitude'] = location_data.longitude
                            st.session_state['location_source'] = "Manual (Cidade)"
                            st.session_state['city_name'] = city
                            st.session_state['location_confirmed'] = True
                            st.success(f"Localização confirmada: {city}")
                            st.rerun()
                        else:
                            st.error("Cidade não encontrada. Tente ser mais específico (ex: 'São Paulo, SP')")
                elif location_method == "Selecionar no Mapa":
                    st.markdown("Clique no mapa para marcar sua localização.")
                    map_center = [-15.788497, -47.879873]
                    lat = st.session_state.get('map_lat', map_center[0])
                    lon = st.session_state.get('map_lon', map_center[1])
                    m = folium.Map(location=[lat, lon], zoom_start=4)
                    folium.Marker([lat, lon], tooltip="Localização selecionada").add_to(m)
                    map_data = st_folium(m, width=700, height=400)
                    if map_data and map_data['last_clicked']:
                        lat = map_data['last_clicked']['lat']
                        lon = map_data['last_clicked']['lng']
                        st.markdown(f"**Coordenadas selecionadas:** {lat}, {lon}")
                        st.session_state['map_lat'] = lat
                        st.session_state['map_lon'] = lon
                    button_disabled = not ('map_lat' in st.session_state and 'map_lon' in st.session_state)
                    if st.button("Confirmar localização (mapa)", disabled=button_disabled):
                        st.session_state['latitude'] = st.session_state['map_lat']
                        st.session_state['longitude'] = st.session_state['map_lon']
                        st.session_state['location_source'] = "Manual (Mapa)"
                        st.session_state['city_name'] = get_city_from_coords(st.session_state['map_lat'], st.session_state['map_lon'])
                        st.session_state['location_confirmed'] = True
                        st.success(f"Localização confirmada: {st.session_state['map_lat']}, {st.session_state['map_lon']}")
                        st.rerun()
                elif location_method == "Baseado em IP":
                    if st.button("Confirmar localização (IP)"):
                        location, source = get_location_from_ip()
                        if location:
                            lat, lon = location
                            st.session_state['latitude'] = lat
                            st.session_state['longitude'] = lon
                            st.session_state['location_source'] = source
                            st.session_state['city_name'] = get_city_from_coords(lat, lon)
                            st.session_state['location_confirmed'] = True
                            st.success(f"Localização confirmada pelo IP: {lat}, {lon}")
                            st.rerun()
            else:
                # Exibe resumo da localização e botão de salvar análise
                st.markdown(f"**Localização confirmada:** {st.session_state.get('city_name', '')}")
                st.markdown(f"**Latitude:** {st.session_state.get('latitude', '')}")
                st.markdown(f"**Longitude:** {st.session_state.get('longitude', '')}")
                st.markdown(f"**Fonte:** {st.session_state.get('location_source', '')}")
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("💾 Salvar análise"):
                        user_id = get_user_id()
                        if user_id:
                            disease = get_disease_by_name(st.session_state['predicted_class'])
                            if disease:
                                if st.session_state.get('latitude') is not None and st.session_state.get('longitude') is not None:
                                    lat = st.session_state['latitude']
                                    lon = st.session_state['longitude']
                                    source = st.session_state.get('location_source')
                                    city_name = st.session_state.get('city_name')
                                else:
                                    lat = lon = source = city_name = None

                                if save_scan(
                                    user_id=user_id,
                                    image_path=st.session_state['uploaded_file_name'],
                                    disease_id=disease['id'],
                                    confidence=st.session_state['confidence'],
                                    latitude=lat,
                                    longitude=lon,
                                    location_source=source,
                                    city_name=city_name
                                ):
                                    st.success("✅ Análise salva com sucesso!")
                                    for key in ['predicted_class', 'uploaded_file_name', 'confidence', 'latitude', 'longitude', 'location_source', 'city_name', 'location_confirmed', 'map_lat', 'map_lon']:
                                        if key in st.session_state:
                                            del st.session_state[key]
                                else:
                                    st.error("❌ Erro ao salvar a análise.")
                            else:
                                st.error("Usuário não autenticado.")

def display_location(image=None):
    """Função para exibir a localização obtida"""
    location, source = get_location(image)
    if location and None not in location:
        lat, lon = location
        
        # Obtendo nome da cidade
        city_name = get_city_from_coords(lat, lon)
        
        st.markdown(f"### 🌍 Localização ({source})")
        if city_name:
            st.markdown(f"**Local:** {city_name}")
        
        # Show more precise coordinate information
        st.markdown("""
        **Coordenadas precisas:**
        """)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Latitude:** {lat}")
            st.markdown(f"*Formato decimal:* {lat:.8f}")
        with col2:
            st.markdown(f"**Longitude:** {lon}")
            st.markdown(f"*Formato decimal:* {lon:.8f}")
        
        # Exibindo o mapa com a localização
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon]).add_to(m)
        folium_static(m)
    else:
        if not st.session_state.show_manual_input and st.session_state.retry_count > 2:
            st.warning("🔍 Está tendo problemas? Tente a entrada manual de localização.")
