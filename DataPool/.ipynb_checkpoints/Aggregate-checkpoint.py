import numpy as np
import os
import pandas as pd
import pickle

from DataPool           import DSFormat
from DataPool.Holiday   import HolidayUtility
from DataPool.Partition import Partition

# Predefined file locations for each dataset
DATASETS_DIR           = "../datasets"
HOLIDAY_DATASET        = "holidays_events.csv"
OIL_DATASET            = "oil.csv"
STORE_DATASET         = "stores.csv"
TRANSACTION_DATASET   = "transactions.csv"
TEST_DATASET_FILENAME  = "test.csv"
TRAIN_DATASET_FILENAME = "train.csv"

PICKLE_SAVE = "DataPool/agg.pkl"


class Aggregate:
    def aggregate_training_set(self, ignore = False):
        print("Started")
        if not self.load_formatted_datasets() or ignore:
            print("Loading datasets...")
            self.load_datasets()

            print("Formatting datasets...")
            self.format_datasets()

            print("Partitioning datasets...")
            self.init_partition()

            print("Joining datasets...")
            self.join_datasets()

            self.save_datasets()
            
            print("Aggregation of the training set complete!")
        else:
            print("Complete")
            
            
    
    def load_datasets(self):
        self.holiday = self.load_dataset(HOLIDAY_DATASET)
        self.oil = self.load_dataset(OIL_DATASET)
        self.store = self.load_dataset(STORE_DATASET)
        self.transaction = self.load_dataset(TRANSACTION_DATASET)
        self.train = self.load_dataset(TRAIN_DATASET_FILENAME)
    
    
    def load_dataset(self, filename: str):
        return pd.read_csv(os.path.join(DATASETS_DIR, filename))
    
    
    def format_datasets(self):
        self.holiday = DSFormat.format_holidays(self.holiday)
        self.oil = DSFormat.format_oil(self.oil)
        self.store = DSFormat.format_stores(self.store)
        self.transaction = DSFormat.format_transactions(self.transaction)
        self.train = DSFormat.format_train(self.train)
    
    
    def init_partition(self):
        self.partitioned = Partition(self.train)
    
    
    def join_datasets(self):
        self.join_oil()
        self.join_store()
        self.join_transaction()
        
        # Dataset joined be narrowed down beforehand
        self.narrow_dataset(10)
        self.join_holiday()
        
    
    def join_oil(self):
        self.train = self.train.merge(self.oil, how="left", on="date")

        
    def join_store(self):
        self.train = self.train.merge(self.store, how="left", on="store_nbr")
        self.train = self.train.rename(columns={'type':'store_type'})
        
        
    def join_transaction(self):
        trans_col = pd.Series(np.zeros(self.train.shape[0]))

        for index, row in self.transaction.iterrows():
            location = self.partitioned.find_data_interval(row.date, row.store_nbr)
            for i in range(location[0],location[1]+1):
                trans_col[i] = row.transactions

        self.train["transactions"] = trans_col

        
    def join_holiday(self):
        hol_util = HolidayUtility(self.holiday)
        values = []
        print("Joining Holiday...")
        for index, row in self.train.iterrows():
            values.append(hol_util.calculateHolidayValues(row))
            if index%(int(len(self.train)/10)) == 0:
                print(10*int(index/((int(len(self.train)/10)))),'%')
        self.train = pd.concat([self.train,pd.DataFrame(values, columns=["holi_importance","holi_type"])], axis=1)
        self.train.holi_type = self.train.holi_type.astype("category")
        print("Holiday Joined!")
    
    def narrow_dataset(self, jump):
        indices = [i for i in range(0, len(self.train), jump)]
        self.train = self.train.iloc[indices].copy()
        self.train = self.train.reset_index().drop("id", axis=1).drop("index", axis=1)
        
    
    def save_datasets(self):
        print("Saving Formatted Dataset...")
        try:
            with open(PICKLE_SAVE, 'wb') as f:
                pickle.dump(self,f)
            print("Save successful...")
            return True
        except:
            print("Save failed...")
            return False
            
    
    def load_formatted_datasets(self):
        print("Searching for previously formatted datasets...")
        try:
            with open(PICKLE_SAVE,"rb") as f:
                temp = pickle.load(f)
                print("Previously formatted dataset found...")
                print("Loading contents...")
                self.holiday = temp.holiday
                self.oil = temp.oil
                self.store = temp.store
                self.transaction = temp.transaction
                self.train = temp.train
                self.partitioned = temp.partitioned
                print("Contents loaded...")
                return True
        except:
            print("No previously formatted datasets found...")
            return False
        