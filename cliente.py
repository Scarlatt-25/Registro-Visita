import requests

BASE_URL = "http://127.0.0.1:8000"   # Cambia si usas otro host o puerto
USERNAME = "admin"                   # Cambia por tu usuario
PASSWORD = "admin"                   # Cambia por tu contraseña


# ----------------------------------------------------
# 1. OBTENER TOKEN JWT
# ----------------------------------------------------
def obtener_token():
    url = f"{BASE_URL}/api/token/"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }

    resp = requests.post(url, data=data)

    if resp.status_code == 200:
        tokens = resp.json()
        print("✅ Token obtenido correctamente.")
        return tokens["access"], tokens["refresh"]
    else:
        print("❌ Error al obtener token:", resp.text)
        return None, None


# ----------------------------------------------------
# 2. LISTAR VISITAS
# ----------------------------------------------------
def listar_visitas(token):
    url = f"{BASE_URL}/api/visitas/"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        print("\n📋 Listado de visitas:")
        print(resp.json())
    else:
        print("\n❌ Error al listar visitas:", resp.status_code, resp.text)


# ----------------------------------------------------
# 3. CREAR VISITA
# ----------------------------------------------------
def crear_visita(token):
    url = f"{BASE_URL}/api/visitas/"
    headers = {"Authorization": f"Bearer {token}"}

    nueva_visita = {
        "nombre": "Juan Pérez",
        "rut": "12345678-5",               # ¡Ojo! No repetir rut o dará error 400
        "motivo": "Entrega de documentos",
        "fecha_de_visita": "2025-01-01"
    }

    resp = requests.post(url, json=nueva_visita, headers=headers)

    if resp.status_code == 201:
        print("\n✅ Visita creada correctamente.")
        print(resp.json())
    else:
        print("\n❌ Error al crear visita:", resp.status_code, resp.text)


# ----------------------------------------------------
# 4. ACTUALIZAR VISITA
# ----------------------------------------------------
def actualizar_visita(token, visita_id):
    url = f"{BASE_URL}/api/visitas/{visita_id}/"
    headers = {"Authorization": f"Bearer {token}"}

    datos_actualizados = {
        "nombre": "Juan Pérez Modificado",
        "rut": "12345678-5",
        "motivo": "Motivo actualizado",
        "fecha_de_visita": "2025-01-02"
    }

    resp = requests.put(url, json=datos_actualizados, headers=headers)

    if resp.status_code == 200:
        print("\n🔄 Visita actualizada:")
        print(resp.json())
    else:
        print("\n❌ Error al actualizar:", resp.status_code, resp.text)


# ----------------------------------------------------
# 5. ELIMINAR VISITA
# ----------------------------------------------------
def eliminar_visita(token, visita_id):
    url = f"{BASE_URL}/api/visitas/{visita_id}/"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.delete(url, headers=headers)

    if resp.status_code == 204:
        print("\n🗑️ Visita eliminada correctamente.")
    else:
        print("\n❌ Error al eliminar:", resp.status_code, resp.text)

# ----------------------------------------------------
# BÚSQUEDA DE VISITAS (por nombre, rut o motivo)
# ----------------------------------------------------
def buscar_visitas(token, termino):
    url = f"{BASE_URL}/api/visitas/?search={termino}"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)

    print(f"\n🔎 Resultados de la búsqueda: '{termino}'")
    print(resp.json())
    print("--------------------------------------------------")


# ----------------------------------------------------
# ORDENAR VISITAS POR CUALQUIER CAMPO
# ----------------------------------------------------
def ordenar_visitas(token, campo):
    url = f"{BASE_URL}/api/visitas/?ordering={campo}"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)

    print(f"\n📌 Visitas ordenadas por: '{campo}'")
    print(resp.json())
    print("--------------------------------------------------")


# ----------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------------------
if __name__ == "__main__":
    access, refresh = obtener_token()

    if access:
        listar_visitas(access)
        crear_visita(access)
        listar_visitas(access)
        buscar_visitas(access, "amara")
        ordenar_visitas(access, "nombre")          # A → Z
        ordenar_visitas(access, "-fecha_de_visita") # Nuevas primero

