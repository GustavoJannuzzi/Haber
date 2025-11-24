import streamlit as st
from PIL import ExifTags
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests

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

def get_city_from_coords(lat, lon):
    """Função para obter o nome da cidade a partir das coordenadas"""
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

def get_location_from_ip():
    """Função para obter localização baseada no IP"""
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

    st.markdown("""
    ### 📍 Localização Atual
    Para melhor precisão na identificação de doenças em sua região, precisamos da sua localização.
    
    > Isso nos ajuda a:
    > - Mapear a ocorrência de doenças em diferentes regiões
    > - Fornecer recomendações mais precisas
    > - Alertar sobre surtos na sua área
    """)

    # Tentativa 1: Dados EXIF
    if image is not None:
        coordinates = get_gps_coordinates(image)
        if coordinates:
            location = coordinates
            location_source = "EXIF"
            st.success("✅ Localização detectada automaticamente a partir da imagem!")
            return location, location_source
        else:
            st.info("""
            ℹ️ **Não foi possível detectar a localização automaticamente**
            
            Por favor, escolha uma das opções abaixo para informar sua localização:
            """)

    # Opções de localização
    location_method = st.radio(
        "Escolha como deseja fornecer sua localização:",
        ["Digitar Cidade", "Selecionar no Mapa", "Baseado em IP"],
        help="Escolha o método mais conveniente para você"
    )

    if location_method == "Digitar Cidade":
        city = st.text_input("Digite sua cidade:", placeholder="Ex: Curitiba, PR")
        if city:
            try:
                with st.spinner("Buscando localização..."):
                    geolocator = Nominatim(user_agent="haber_app")
                    location_data = geolocator.geocode(city + ", Brasil")
                    if location_data:
                        location = (location_data.latitude, location_data.longitude)
                        location_source = "Manual (Cidade)"
                        return location, location_source
                    else:
                        st.error("Cidade não encontrada. Tente ser mais específico (ex: 'São Paulo, SP')")
            except Exception as e:
                st.error("Erro ao buscar localização. Tente usar o mapa.")

    elif location_method == "Selecionar no Mapa":
        st.markdown("""
        👉 **Como usar o mapa:**
        1. Navegue pelo mapa usando dois dedos para mover e dar zoom
        2. Toque no local desejado para marcar
        3. Ajuste a posição do marcador se necessário
        4. Toque em 'Confirmar Localização'
        """)
        
        # Criando um mapa centralizado no Brasil
        m = folium.Map(
            location=[-15.788497, -47.879873],
            zoom_start=4,
            scrollWheelZoom=True,
            dragging=True
        )
        
        # Adicionando um marcador que pode ser arrastado
        marker = folium.Marker(
            [-15.788497, -47.879873],
            popup="Toque e segure para mover",
            draggable=True
        )
        marker.add_to(m)
        
        # Adicionando controles de zoom mais visíveis para mobile
        folium.plugins.Fullscreen().add_to(m)
        
        # Exibindo o mapa com altura adequada para mobile
        folium_static(m, height=400)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Centralizar Mapa", use_container_width=True):
                m.location = [-15.788497, -47.879873]
                m.zoom_start = 4
                st.rerun()
        with col2:
            if st.button("✅ Confirmar Localização", use_container_width=True):
                location = (marker.location[0], marker.location[1])
                location_source = "Manual (Mapa)"
                return location, location_source

    elif location_method == "Baseado em IP":
        with st.spinner("Obtendo localização baseada em IP..."):
            location, location_source = get_location_from_ip()
            if location:
                return location, location_source
            else:
                st.error("Não foi possível obter localização por IP. Tente digitar sua cidade.")

    return None, None

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