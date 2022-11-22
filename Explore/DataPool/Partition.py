class Partition:
    def __init__(self, main_ds):
        self.main_ds = main_ds
        self.store_types = 33
        self.total_stores = 54
        self.segment_dates()
        self.find_order_of_stores()
    
    ## UTILITY ##
    def segment_dates(self):
        dates = []
        start = 0
        end = -1
        curr_date = self.main_ds.date[0]
        for i, date in enumerate(self.main_ds.date):
            if date != curr_date:
                end = i-1
                dates.append((curr_date, start, end))
                start = i
                curr_date = date
        self.date_segments = dates

    # Index = store_nbr, value = order
    def find_order_of_stores(self):
        store_nbrs = []
        for i in range(self.total_stores+1):
            store_nbrs.append(0)
        for i in range(0,self.date_segments[0][2]+1,self.store_types):
            store_nbrs[self.main_ds.iloc[i].store_nbr] = int(i/self.store_types)
        self.store_order = store_nbrs


     # Given a date and store number it finds where the corresponding section is
    # in the train_dsf DataFrame
    def find_data_interval(self, tgt_date, tgt_store_nbr):
        low = 0
        high = len(self.date_segments)-1
        date_found_index = -1
        while low <= high:
            mid = int((low+high)/2)
            if(self.date_segments[mid][0] == tgt_date):
                date_found_index = mid
                break
            elif(self.date_segments[mid][0] > tgt_date):
                high = mid-1
            else:
                low = mid+1

        store_nbr_index = self.store_order[tgt_store_nbr]
        low_found = self.date_segments[date_found_index][1]+store_nbr_index*self.store_types
        high_found = low_found + self.store_types - 1
        return low_found, high_found