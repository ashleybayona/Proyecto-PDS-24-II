from apscheduler.schedulers.background import BackgroundScheduler

from config.connect_mysql import *

def actualizar_entregas():
    try:   
        conexion = conexion_pool.get_connection()
        with conexion.cursor() as cursor:
            #revisa cuales entregas siguen en proceso y se fija si ya pasaron los 15min
            cursor.execute("""select idEntrega from entrega where estadoEntrega = 'en proceso'
                            and timestampdiff(minute, concat(fechaEntrega, '', horaEstimada), now()) >= 15;""")
            entregas_pendientes = cursor.fetchall()

            for entrega in entregas_pendientes:
                idEntrega = entrega[0]
                cursor.callproc('estado_entregado', [idEntrega])
            
            conexion.commit()
    except Exception as e:
        print(f"Error al actualizar entregas: {str(e)}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()