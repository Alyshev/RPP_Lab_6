from db_init import *
import cherrypy


class MyWebService:
    def __init__(self, table=FullName):
        self.table = table

    @cherrypy.expose
    def index(self):
        objects = get_data(self.table)
        edit_form = build_form(self.table)

        template = ("""
            <html>
            <head>
                <title>lab6</title>
            </head>
            <body>
                    <form method="POST" action="/change_table">  <!-- Кнопки переключения таблиц -->
                        <input type="submit" name="table" value=FullName>
                        <input type="submit" name="table" value=Characteristics>
                    </form>
                    
                    <h1>{0}</h1>  <!-- Имя таблицы -->
                    
                    <table border="1" width="600" style="border-collapse:collapse; margin-bottom:20px;">  <!-- Таблица -->
                        {1}
                    </table>
                    <form method="POST" action="/apply">  <!-- Поле ввода -->
                        {2}
                        <input id="cb" type="checkbox" name="is_del"><label for="cb">Delete</label>
                        <input type="submit" value=Apply>
                    </form>
            </body>
            </html>
        """).format(self.table.__name__, objects, edit_form)
        return template

    @cherrypy.expose
    def apply(self, **kwargs):
        print(self.table, kwargs)
        if not kwargs.get('is_del'):
            if kwargs.get('id'):  # Редактирование
                item = kwargs.get('id')
                kwargs.pop('id')
                for k, v in list(kwargs.items()):
                    if v == '':
                        kwargs.pop(k)
                self.table.update(kwargs).where(self.table.id == item).execute()
            else:  # Добавление
                kwargs.pop('id')
                self.table.insert(kwargs).execute()
        else:  # Удаление
            self.table.delete().where(self.table.id == kwargs['id']).execute()
        raise cherrypy.HTTPRedirect('/')


    @cherrypy.expose
    def change_table(self, table):
        self.table = table_getter(table)
        raise cherrypy.HTTPRedirect('/')


def get_data(table):
    data = table.select().dicts()
    header = '<tr>{0}</tr>'.format(''.join(['<th>{0}</th>'.format(key) for key in data[0].keys()]))
    rows = ''.join(['<tr>{0}</tr>'.format(''.join(['<td>{0}</td>'.format(value) for value in row.values()])) for row in data])
    return '{0}{1}'.format(header, rows)


def build_form(table):
    res = ""
    names = get_fields(table)
    for i in names:
        res += f'<input type="text" name="{i}" placeholder="{i}">'
    return res


if __name__ == '__main__':
    cherrypy.quickstart(MyWebService())
