from fastapi import FastAPI, HTTPException
from db import get_db_connection
from models import Bet  # Asegúrate de tener la clase Bet en models.py

app = FastAPI()

# ... aquí irían tus otros endpoints (usuaris, materials, etc.) ...

# -------------------
#     BETS CRUD
# -------------------

# Crear apuesta (POST)
@app.post("/bets/")
def crear_bet(bet: Bet):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Ejecutamos el INSERT, omitiendo el id porque es autoincrement
        cursor.execute(
            "INSERT INTO bets (partido, team, bet, win) VALUES (%s, %s, %s, %s)",
            (bet.partido, bet.team, bet.bet, bet.win),
        )
        conn.commit()
        # Obtenemos el id generado
        new_id = cursor.lastrowid
        # Recuperamos la apuesta recién creada
        cursor.execute("SELECT * FROM bets WHERE id = %s", (new_id,))
        created_bet = cursor.fetchone()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {
        "id": new_id,
        "partido": created_bet["partido"],
        "team": created_bet["team"],
        "bet": created_bet["bet"],
        "win": created_bet["win"]
    }

# Obtener todas las apuestas (GET)
@app.get("/bets/")
def obtener_todas_las_bets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bets")
    bets = cursor.fetchall()
    cursor.close()
    conn.close()
    return bets

# Obtener una apuesta por ID (GET)
@app.get("/bets/{bet_id}")
def obtener_bet(bet_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bets WHERE id = %s", (bet_id,))
    bet = cursor.fetchone()
    cursor.close()
    conn.close()
    if not bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    return bet

# Modificar apuesta (PUT)
# Si solo quieres aumentar la cantidad del campo 'bet', podrías usar un UPDATE sumando.
# Por ejemplo: "UPDATE bets SET bet = bet + %s WHERE id = %s"
@app.put("/bets/{bet_id}")
def modificar_bet(bet_id: int, nueva_bet: Bet):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE bets SET partido = %s, team = %s, bet = %s, win = %s WHERE id = %s",
            (nueva_bet.partido, nueva_bet.team, nueva_bet.bet, nueva_bet.win, bet_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {
        "id": bet_id,
        "partido": nueva_bet.partido,
        "team": nueva_bet.team,
        "bet": nueva_bet.bet,
        "win": nueva_bet.win
    }

# Eliminar apuesta (DELETE)
@app.delete("/bets/{bet_id}")
def eliminar_bet(bet_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM bets WHERE id = %s", (bet_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "Apuesta eliminada correctamente"}