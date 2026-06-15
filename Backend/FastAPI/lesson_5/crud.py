#here we write all functions which refer to database

#this is something like a fake database (just to test out this dict which resembles database)
FAKE_DB = {
    1: {
        "id": 1,
        "client_name": "Иван",
        "arrival_time": "2026-06-16T14:30:00",
        "parts_to_change": "Свечи зажигания, моторное масло",
        "status": "Мастер выехал"
    }
}

def get_order_by_id(order_id: int):
    #here in the future we will have a real SQL-request
    return FAKE_DB.get(order_id)
