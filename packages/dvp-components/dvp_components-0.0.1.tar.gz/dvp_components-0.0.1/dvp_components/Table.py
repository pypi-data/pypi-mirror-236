from .DvpTable import DvpTable
from pandas import Series

class Table(object):
    def __init__(
        self,
        dataframe,
        id=None,
        className=None,
        rename={},
        groupby=[],
        verticalTh=[],
        style={},
        columnclassNames={},
        columnalign={},
        pagination={
            'pageSize': 50,
            'hideOnSinglePage': True,
            'showSizeChanger': False,
            'showTotal': True,
            'position': 'bottomRight'
        },
        maxHeight=None,
        maxWidth=None,
        filterColumns=[],
        searchColumns=[],
        linkedColumns=[],
        rawhtmlColumns=[],
        checkboxColumns=[],
        checkboxGroupColumns=[],
        radioColumns=[],
        radioGroupColumns=[],
        pubURL='',
        tagColumns=[],
        tagsColumns=[],
        pubColumns=[],
        selectedValues=[],
        loadScript=[]
    ):
        """
        Arguments:
        - dataframe (pandas.DataFrame; required): A pandas dataframe as input
        - id (str, optional): ID of the table
        - className (str, optional): class names assigned to the table
        - rename (dict, optional): A dict object to rename the columns for display purpose. Specify columns to rename only.
        - groupby (list, optional): List of columns to enable cells merging for same values. Make sure data is sorted in a proper order.
        - verticalTh (list, optional): List of column headers to be rotated (90 degree).
        - style (dict, optional): CSS style applied to the table.
        - columnalign (dict, optional): Alignment of columns. The alignment is set to left by default. For e.g., {'col1': 'left', 'col2': 'right', 'col3': 'center'}
        - columnclassNames (dict, optional): Assign classname to columns. For elg., {'col1': 'class1', 'col2': 'class1'}
        - maxHeight (int, optional): Max height in numbers
        - maxWidth(int, optional): Max width in numbers
        - loadScript (list): List of scripts ot load
        - pubURL (str): ublication URL, if render mode is publicatoin
        - filterColumns (list, optional): List of columns to enable filtering in categories
        - searchColumns (list, optional): List of columns to enable search
        - linkedColumns (list, optional): List of columns to render link
        - rawhtmlColumns (list, optional): List of columns to render raw html
        - checkboxColumns (list, optional): List of columns for checkbox rendering
        - checkboxGroupColumns (list, optional): List of columns for checkbox group rendering
        - radioColumns (list, optional): List of columns for radio rendering
        - radioGroupColumns (list, optional): List of columns for radio group rendering
        - tagColumns (list, optional): List of columns for tag rendering
        - tagsColumns (list, optional): List of columns for multi-tags rendering
        - selectedValues (list | dict, optional): List of selected values | Dict of selected values
        - pagination (dict; default { defaultPageSize: 20, hideOnSinglePage: True, showSizeChanger: False,})
            Config of pagination. You can ref table pagination config or full
            pagination document, hide it by setting it to False.

            `pagination` is a dict with keys:

            - current (number; optional)

            - disabled (boolean; optional)

            - hideOnSinglePage (boolean; optional)

            - pageSize (number; optional)

            - pageSizeOptions (list of numbers; optional)

            - position (a value equal to: 'topLeft', 'topCenter', 'topRight', 'bottomLeft', 'bottomCenter', 'bottomRight'; optional)

            - showQuickJumper (boolean; optional)

            - showSizeChanger (boolean; optional)

            - showTotal (boolean; optional)

            - showTotalPrefix (string; optional)

            - showTotalSuffix (string; optional)

            - simple (boolean; optional)

            - size (a value equal to: 'default', 'small'; optional)

            - total (number; optional) | boolean | dict
        """
        self.dataframe = dataframe
        self.id = str(id)
        self.className = str(className)
        self.rename = rename
        self.pagination = pagination
        self.groupby = groupby
        self.verticalTh = verticalTh
        self.style = style
        self.columnalign= columnalign
        self.columnclassNames = columnclassNames
        self.maxHeight = maxHeight
        self.maxWidth = maxWidth
        self.filterColumns = filterColumns
        self.searchColumns = searchColumns
        self.linkedColumns = linkedColumns
        self.checkboxColumns= checkboxColumns
        self.checkboxGroupColumns = checkboxGroupColumns
        self.radioGroupColumns = radioGroupColumns
        self.tagColumns = tagColumns
        self.tagsColumns = tagsColumns
        self.selectedValues = selectedValues
        self.rawhtmlColumns = rawhtmlColumns
        self.pubColumns = pubColumns
        self.loadScript = loadScript
        self.pubURL = pubURL

    def dash(self):
        table = DvpTable(
            id=self.id,
            className=self.className,
            columns=self.columns,
            data=self.data,
            pagination=self.pagination,
            size='small',
            bordered=True,
            style=self.style,
            maxHeight=self.maxHeight,
            maxWidth=self.maxWidth,
            selectedValues=self.selectedValues,
            loadScript=self.loadScript,
            pubURL=self.pubURL
        )
        return table

    @property
    def columns(self):
        cols = []
        for col in self.dataframe.columns:
            col_dt = {
                'dataIndex': str(col),
                'title': col
            }
            if self.rename:
                if self.rename.get(col):
                    col_dt.update({'title': self.rename[col]})
            if col in self.groupby:
                rowspan = self.rowSpan(self.dataframe[col])
                col_dt.update({'rowSpan': rowspan})
            if col in self.verticalTh:
                col_dt.update({'rotated': True})
            if col in self.columnalign:
                col_dt.update({'align': self.columnalign[col]})
            if col in self.columnclassNames:
                col_dt.update({'className': self.columnclassNames[col]})
            if col in self.filterColumns:
                cats = self.dataframe[col].unique().tolist()
                cats.sort()
                col_dt.update({'filters': [{'text': cat, 'value': cat} for cat in cats]})
            if col in self.searchColumns:
                col_dt.update({'search': True})
            if col in self.linkedColumns:
                col_dt.update({'renderOptions': {'renderType': 'link'}})
            elif col in self.checkboxColumns:
                col_dt.update({'renderOptions': {'renderType': 'checkbox'}})
            elif col in self.checkboxGroupColumns:
                col_dt.update({'renderOptions': {'renderType': 'checkboxgroup'}})
            elif col in self.radioGroupColumns:
                col_dt.update({'renderOptions': {'renderType': 'radiogroup'}})
            elif col in self.tagColumns:
                col_dt.update({'renderOptions': {'renderType': 'tag'}})
            elif col in self.tagsColumns:
                col_dt.update({'renderOptions': {'renderType': 'tags'}})
            elif col in self.rawhtmlColumns:
                col_dt.update({'renderOptions': {'renderType': 'rawhtml'}})
            elif col in self.pubColumns:
                col_dt.update({'renderOptions': {'renderType': 'publication'}})
            cols.append(col_dt)
        return cols

    @property
    def data(self):
        if self.selectedValues and (self.checkboxGroupColumns or self.radioGroupColumns):
            df = self.dataframe.copy()
            for col in self.checkboxGroupColumns:
                df[col] = df[col].apply(lambda x: self.updateValues(x, self.selectedValues))
            for col in self.radioGroupColumns:
                df[col] = df[col].apply(lambda x: self.updateValues(x, self.selectedValues))
            df.insert(0, 'key', range(len(df)))
            records = df.to_dict('records')
        else:
            df = self.dataframe.copy()
            df.insert(0, 'key', range(len(df)))
            records = df.to_dict('records')
        return records
    
    @staticmethod
    def updateValues(dt, sel_dt):
        if dt['id'] in sel_dt.keys():
            dt.update({'value': sel_dt[dt['id']]})
        return dt
    
    @staticmethod
    def rowSpan(values):
        """
        Arguments:
        - values (pandas.Series): a column in a pandas dataframe or a pandas series
        """
        val_count = dict(values.value_counts())
        val_index = dict(values.drop_duplicates())
        rowspan = {k: val_count[v] for k, v in val_index.items()}
        rowspan = Series(values.index).map(rowspan).fillna(0).astype(int)
        rowspan = dict(rowspan)
        return rowspan