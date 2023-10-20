import pendulum
import pandas as pd


class Transform:
    
    def __init__(self, df):
        self.df = df

    def lower_case_columns(self):
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')
        return self

    def add_updated_timestamp(self):
        # Add a UTC timestamp
        self.df['updated_at'] = pendulum.now().strftime('%Y-%m-%d %H:%M:%S %p')
        self.df['updated_at'] = self.df['updated_at'].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S %p', utc=True)
        return self

    def filter_today(self, date_fmt=None):

        """
        Pass in a pandas dataframe to:

        1. Lower case col names
        2. Cast date col as datetime
        3. Set datetime col as index
        4. Return where datetime == today
        """

        if date_fmt is None:
            date_fmt = '%d/%m/%Y'

        today = pendulum.today().naive()

        self.df.columns = self.df.columns.str.lower()
        self.df['date'] = pd.to_datetime(self.df['date'], format=date_fmt)
        self.df.set_index('date', inplace=True)
        return self.df.loc[today]

    def filter_up_to_today(self, date_fmt=None):

        if date_fmt is None:
            date_fmt = '%d/%m/%Y'

        today = pendulum.today().naive()

        self.df.columns = self.df.columns.str.lower()
        self.df['date'] = pd.to_datetime(self.df['date'], format=date_fmt)
        self.df.set_index('date', inplace=True)
        return self.df.loc[:today]