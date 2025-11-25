import requests
import time

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "admin"


class ClienteAPI:
    def __init__(self):
        self.access = None
        self.refresh = None

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

    def request(self, method, endpoint, retry=True, **kwargs):
        headers = {"Authorization": f"Bearer {self.access}"}
        url = f"{BASE_URL}{endpoint}"

        r = requests.request(method, url, headers=headers, **kwargs)

        if r.status_code == 401 and retry:
            if "token_not_valid" in r.text:
                if self.refrescar_token():
                    return self.request(method, endpoint, retry=False, **kwargs)

        return r

    def listar_visitas(self):
        print("\n📋 Listando visitas...")

        resp = self.request("GET", "/api/visitas/")
        if resp.status_code != 200:
            print("❌ Error:", resp.text)
            return

        data = resp.json()
        visitas = data.get("results", [])  

        if not visitas:
            print("⚠️ No hay visitas registradas.")
            return

        for v in visitas:
            url = v["url"]
            visita_id = url.rstrip("/").split("/")[-1]

            print(f"- ID {visita_id}: {v['nombre']} | {v['rut']} | {v['motivo']} | {v['fecha_de_visita']}")
    
    
    def crear_visita(self):
        print("\n📝 Crear nueva visita")
        nombre = input("Nombre: ")
        rut = input("RUT: ")
        motivo = input("Motivo: ")
        fecha = input("Fecha (YYYY-MM-DD): ")

        data = {
            "nombre": nombre,
            "rut": rut,
            "motivo": motivo,
            "fecha_de_visita": fecha
        }

        r = self.request("POST", "/api/visitas/", json=data)

        if r.status_code in (200, 201):
            print("✅ Visita creada correctamente.")
        else:
            print("❌ Error al crear visita:", r.text)




    def eliminar_visita(self):
        visit_id = input("ID de la visita a eliminar: ")
        r = self.request("DELETE", f"/api/visitas/{visit_id}/")

        if r.status_code == 204:
            print("🗑️ Visita eliminada correctamente.")
        else:
            print("❌ Error:", r.text)

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



def menu():
    cliente = ClienteAPI()
    cliente.obtener_token()

    while True:
        print("""
        ==============================
             CLIENTE API VISITAS
        ==============================
        1. Listar visitas
        2. Crear visita
        3. Eliminar visita
        4. Monitorear en tiempo real
        5. Salir
        """)


        opcion = input("Elige una opción: ")

        if opcion == "1":
            cliente.listar_visitas()
        elif opcion == "2":
            cliente.crear_visita()
        elif opcion == "3":
            cliente.eliminar_visita()
        elif opcion == "4":
            cliente.monitorear()
        elif opcion == "5":
            print("👋 Adiós!")
            break



if __name__ == "__main__":
    menu()
