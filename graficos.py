# graficos.py
import matplotlib.pyplot as plt
from database import get_session
from models import Cliente  # Suponiendo que tienes una clase Cliente en models.py

def generar_graficos():
    # Obtener una sesión de la base de datos
    session = next(get_session())

    # Consulta a la base de datos (por ejemplo, obtener los primeros 10 clientes)
    clientes = session.query(Cliente).limit(10).all()

    # Verificar si obtuvimos clientes
    if clientes:
        print("Clientes obtenidos:")
        for cliente in clientes:
            print(f"{cliente.nombre} - {cliente.email}")
    else:
        print("No se encontraron clientes.")

    # Generar un gráfico simple (por ejemplo, contar los clientes por nombre)
    nombres = [cliente.nombre for cliente in clientes]
    valores = [len(cliente.nombre) for cliente in clientes]  # Usamos la longitud del nombre como valor (solo un ejemplo)

    # Crear un gráfico simple
    plt.figure(figsize=(10, 6))
    plt.bar(nombres, valores)
    plt.title('Clientes por longitud de nombre')
    plt.xlabel('Cliente')
    plt.ylabel('Longitud del Nombre')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

if __name__ == "__main__":
    generar_graficos()
