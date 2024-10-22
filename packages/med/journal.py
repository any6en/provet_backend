from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_journal(db: AsyncSession, owner_id: int = None):
    query_rows = text("""
        SELECT 
            primary_visits.id AS id, 
            primary_visits.date_visit AS date, 
            'Первичный прием' AS content,
            users.last_name AS doctor
        FROM provet.primary_visits 
        JOIN provet.users ON primary_visits.user_id = users.id
        WHERE primary_visits.owner_id = :owner_id 

        UNION ALL 

        SELECT 
            vaccination_acts.id AS id, 
            vaccination_acts.vaccination_date AS date, 
            'Акт вакцинации' AS content,
            users.last_name AS doctor
        FROM provet.vaccination_acts 
        JOIN provet.users ON vaccination_acts.user_id = users.id
        WHERE vaccination_acts.owner_id = :owner_id

        UNION ALL

        SELECT 
            repeat_visits.id AS id, 
            repeat_visits.date_visit AS date, 
            'Повторный прием' AS content, 
            users.last_name AS doctor
        FROM provet.repeat_visits 
        JOIN provet.users ON repeat_visits.user_id = users.id
        WHERE repeat_visits.owner_id = :owner_id 

        ORDER BY date;
    """)

    result_rows = await db.execute(
        query_rows, {'owner_id': owner_id}
    )
    rows = result_rows.all()
    result = []
    for row in rows:
        dict = row._asdict()

        date = dict.get('date')
        if date is not None:
            dict['date'] = date.isoformat()

        result.append(dict)
    return result
