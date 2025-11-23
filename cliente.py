import requests
import time

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "admin"


class ClienteAPI:
    def __init__(self):
        self.access = None
        self.refresh = None

    # ----------------------------------------------------
    # 1. OBTENER TOKEN
    # ----------------------------------------------------
    def obtener_token(self):
        url = f"{BASE_URL}/api/token/"
        data = {"username": USERNAME, "password": PASSWORD}

        print("\n🔐 Obteniendo token JWT...")

        r = requests.post(url, data=data)

        if r.status_code == 200:
            self.access = r.json().get("access")
            self.refresh = r.json().get("refresh")
            print("✅ Token obtenido con éxito.\n")
        else:
            print("❌ Error al obtener token:", r.text)
            exit()

    # ----------------------------------------------------
    # 2. REFRESCAR TOKEN
    # ----------------------------------------------------
    def refrescar_token(self):
        print("🔄 Token expirado. Intentando refrescar...")
        url = f"{BASE_URL}/api/token/refresh/"
        r = requests.post(url, data={"refresh": self.refresh})

        if r.status_code == 200:
            self.access = r.json().get("access")
            print("✅ Token renovado.\n")
            return True
        else:
            print("❌ No se pudo refrescar el token:", r.text)
            return False

    # ----------------------------------------------------
    # 3. REQUEST AUTOMÁTICA
    # ----------------------------------------------------
    def request(self, method, endpoint, retry=True, **kwargs):
        headers = {"Authorization": f"Bearer {self.access}"}
        url = f"{BASE_URL}{endpoint}"

        r = requests.request(method, url, headers=headers, **kwargs)

        if r.status_code == 401 and retry:
            if "token_not_valid" in r.text:
                if self.refrescar_token():
                    return self.request(method, endpoint, retry=False, **kwargs)

        return r

    # ----------------------------------------------------
    # 4. LISTAR VISITAS (ARREGLADO)
    # ----------------------------------------------------
    def listar_visitas(self):
        print("\n📋 Listando visitas...")

        resp = self.request("GET", "/api/visitas/")
        if resp.status_code != 200:
            print("❌ Error:", resp.text)
            return

        data = resp.json()
        visitas = data.get("results", [])  # paginación DRF

        if not visitas:
            print("⚠️ No hay visitas registradas.")
            return

        for v in visitas:
            # obtener ID desde la URL
            url = v["url"]
            visita_id = url.rstrip("/").split("/")[-1]

            print(f"- ID {visita_id}: {v['nombre']} | {v['rut']} | {v['motivo']} | {v['fecha_de_visita']}")
    


    # ----------------------------------------------------
    # 5. ELIMINAR VISITA
    # ----------------------------------------------------
    def eliminar_visita(self):
        visit_id = input("ID de la visita a eliminar: ")
        r = self.request("DELETE", f"/api/visitas/{visit_id}/")

        if r.status_code == 204:
            print("🗑️ Visita eliminada correctamente.")
        else:
            print("❌ Error:", r.text)

    # ----------------------------------------------------
    # 6. MONITOREO EN TIEMPO REAL
    # ----------------------------------------------------
    def monitorear(self):
        print("\n📡 Modo monitoreo activado.")
        print("Se consultará la API cada 10 segundos para mostrar nuevas visitas.\n")

        ultimo_conteo = 0

        while True:
            r = self.request("GET", "/api/visitas/")

            if r.status_code == 200:
                data = r.json()
                visitas = data.get("results", [])
                total = len(visitas)

                if total != ultimo_conteo:
                    print("\n🔔 Cambio detectado en visitas:")
                    for v in visitas:
                        visita_id = v["url"].rstrip("/").split("/")[-1]
                        print(f"- {visita_id} | {v['nombre']} | {v['rut']} | {v['motivo']}")
                    ultimo_conteo = total

            else:
                print("❌ Error:", r.text)

            time.sleep(10)


# ----------------------------------------------------
# 7. MENÚ PRINCIPAL
# ----------------------------------------------------
def menu():
    cliente = ClienteAPI()
    cliente.obtener_token()

    while True:
        print("""
==============================
     CLIENTE API VISITAS
==============================
1. Listar visitas
2. Eliminar visita
3. Monitorear en tiempo real
4. Salir
""")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            cliente.listar_visitas()
        elif opcion == "2":
            cliente.eliminar_visita()
        elif opcion == "3":
            cliente.monitorear()
        elif opcion == "4":
            print("👋 Adiós!")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    menu()
