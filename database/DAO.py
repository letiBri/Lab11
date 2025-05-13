from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO:
    @staticmethod
    def getAllColori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select distinct(gp.Product_color) as color
                    from go_products gp"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["color"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(colore):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select *
                    from go_products gp 
                    where gp.Product_color = %s"""

        cursor.execute(query, (colore,))

        for row in cursor:
            result.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesoArco(u, v, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select count(*) as peso
                    from (select gds1.Product_number as p1, gds2.Product_number as p2, gds2.Date
                            from go_daily_sales gds1, go_daily_sales gds2
                            where gds1.Product_number = %s and gds2.Product_number = %s and year(gds1.Date) = %s and gds1.Date = gds2.Date and gds1.Retailer_code = gds2.Retailer_code
                            group by gds2.Date) as t"""

        cursor.execute(query, (u.Product_number, v.Product_number, anno))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result
