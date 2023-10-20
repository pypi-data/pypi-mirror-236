import scipy.stats as st
import pandas as pd

class chartData(object):
    def __init__(
        self,
        data,
        column,
        column2='',
        labels={},
        alias={},
        groupby=None,
        missingVals=[99999]
    ):
        self.df = data
        self.labels = labels
        self.column = column
        self.column2 = column2
        self.groupby = groupby
        self.missing = missingVals
        self.alias = alias

    @staticmethod
    def calPert(df, column='value'):
        perts = round(df[column] / df[column].sum() * 100, 2)
        perts = perts.apply(lambda x: '{:.2f}'.format(x))
        return perts

    @staticmethod
    def tryInt(n):
        try:
            return int(float(n))
        except:
            return n

    @staticmethod
    def sortPvalue(n):
        if n < 0.01:
            return 'p < 0.01'
        elif n < 0.05:
            return 'p < 0.05'
        else:
            return 'p = {:.2f}'.format(n)

    @staticmethod
    def linearRegress(x, y):
        result = {}
        try:
            slope, intercept, r_value, p_value, _ = st.linregress(
                x.astype(float), y.astype(float))
            if pd.notna(p_value):
                p_value = chartData.sortPvalue(p_value)
                if intercept > 0:
                    intercept = ' + {:.2f}'.format(intercept)
                else:
                    intercept = ' - ' + '{:.2f}'.format(intercept).replace('-', '')
                result = {'k': '{:.2f}'.format(slope), 'b': intercept,
                          'r2': '{:.2f}'.format(r_value ** 2), 'p': p_value}
                          
        except:
            pass
        return result

    @staticmethod
    def mapLabel(df, column, label_dt):
        label_dt.update({99999: 'Unknown'})
        vals = df[column].apply(
            lambda x: chartData.tryInt(x) if pd.notna(x) else pd.NA)
        if all([label_dt.get(v) for v in vals.unique().tolist()]):
            vals = vals.map(label_dt).fillna(df[column])
        return vals

    def sortCorrValues(self):
        df = self.df.copy()
        corrs = []
        for col in [self.column, self.column2]:
            df[col] = df[col].apply(
                lambda x: float(x) if pd.notna(x) else pd.NA)
            df[col] = df[col].apply(lambda x: pd.NA if pd.isna(
                x) else pd.NA if x in self.missing else x)

        df = df.dropna(subset=[self.column, self.column2])

        if self.groupby:
            df[self.groupby] = df[self.groupby].apply(
                lambda x: int(x) if pd.notna(x) else 99999).astype(int)
            df = df.sort_values(by=[self.groupby])
            df = df[[self.column, self.column2, self.groupby]]
            gs = df[self.groupby].unique().tolist()
            for g in gs:
                _ = df[df[self.groupby] == g]
                result = self.linearRegress(_[self.column], _[self.column2])
                if result:
                    result.update({'group': g})
                corrs.append(result)

        else:
            df = df[[self.column, self.column2]]
            result = self.linearRegress(df[self.column], df[self.column2])
            if result:
                result.update({'group': ''})
            corrs.append(result)

        corrs = [x for x in corrs if x]

        if self.labels.get(self.groupby):
            for i in range(len(corrs)):
                corrs[i]['group'] = self.labels.get(self.groupby)[corrs[i]['group']] + ': '

        for col in df.columns:
            if self.labels:
                if self.labels.get(col):
                    df[col] = self.mapLabel(df, col, self.labels.get(col))

        data = df.to_dict('records')        
        return data, corrs

    def sortValues(self):
        df = self.df.copy()
        for col in [self.column, self.groupby]:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: float(x) if pd.notna(x) else pd.NA)
                df[col] = df[col].apply(lambda x: pd.NA if pd.isna(
                    x) else pd.NA if x in self.missing else x)
        if self.groupby:
            df[self.groupby] = df[self.groupby].apply(
                lambda x: int(x) if pd.notna(x) else 99999).astype(int)
            df = df.sort_values(by=[self.groupby])
        df = df.dropna(subset=[self.column])
        for col in df.columns:
            if self.labels:
                if self.labels.get(col):
                    df[col] = self.mapLabel(df, col, self.labels.get(col))
        return df

    def CountValues(self):
        df = self.df.copy()
        for col in [self.column, self.groupby]:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: int(x) if pd.notna(x) else pd.NA)
                df[col] = df[col].apply(lambda x: pd.NA if pd.isna(
                    x) else pd.NA if x in self.missing else x)

        if not self.groupby:
            data = df[self.column].dropna()
            data = data.value_counts().to_frame('value').reset_index()
            data.columns = [self.column, 'value']
            data['pert'] = self.calPert(data, 'value')
            data = data.sort_values(by=[self.column])
        else:
            df = df.dropna(subset=[self.groupby]).fillna(99999)
            df = df.groupby(self.groupby)[self.column].value_counts()
            df = df.to_frame('value').reset_index()
            data = []
            gs = df[self.groupby].unique().tolist()
            for g in gs:
                _ = df[df[self.groupby] == g].drop(columns=[self.groupby])
                _.insert(1, 'category', [g] * len(_))
                data.append(_)
            data = pd.concat(data)
            data = data.sort_values(by=[self.column, 'category'])
            data['pert'] = 100 * data['value'] / \
                data.groupby(self.column)['value'].transform('sum')
            data['pert'] = data['pert'].apply(lambda x: '{:.2f}'.format(x))
        for col in data.columns:
            if self.labels:
                if self.labels.get(col):
                    data[col] = self.mapLabel(data, col, self.labels.get(col))
        data['pert'] = data.apply(
            lambda x: '{} ({}%)'.format(x['value'], x.pert), axis=1)
        data = data.rename(columns=self.alias)
        return data.to_dict('records')