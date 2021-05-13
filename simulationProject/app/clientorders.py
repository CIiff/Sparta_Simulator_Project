import pandas as pd
import random


class ClientOrders:
    def __init__(self, current_month, courses):
        self.current_month = current_month
        self.client_orders_df = pd.DataFrame(columns=['Client ID', 'Month advert placed', 'Month advert removed',
                                                      'Course requested', 'Spartans requested', 'Spartans obtained',
                                                      'Happy? (T/F)'])
        self.courses = courses
    # clients data frame - create OUTSIDE month-iterating loop!!

    # --- place following in month-iteration loop (ITERATOR = current_month) ---
    def initialize_order(self):

        if self.current_month >= 13:
            # variables below apply for returning AND new clients
            client_course = random.choice(self.courses)
            spartans_needed_rand = random.choice(range(15, 51))
            new_order = {'Client ID': max(self.client_orders_df['Client ID']) + 1,
                         'Month advert placed': self.current_month, 'Month advert removed': self.current_month + 12,
                         'Course requested': client_course, 'Spartans requested': spartans_needed_rand,
                         'Spartans obtained': 0, 'Happy? (T/F)': True}

            # append new_order to the dataframe
            self.client_orders_df.append(new_order, ignore_index=True)

            # Currently needs a manual initialisation for the very first order

            happy_client_index_list = self.client_orders_df.index[self.client_orders_df['Happy? (T/F)']].tolist()
            for happy_index in happy_client_index_list:
                # get row info for each index with a 'happy' client - so unhappy clients never place new orders.
                retrieval_row = self.client_orders_df.iloc[happy_index, :]
                if retrieval_row['Month advert removed'] == (self.current_month - 12):
                    # only take new orders from existing happy clients 12 months after their previous order was
                    # successfully completed
                    old_client_new_order = {'Client ID': retrieval_row['Client ID'],
                                            'Month advert placed': self.current_month,
                                            'Month advert removed': self.current_month + 12,
                                            'Course requested': client_course,
                                            'Spartans requested': spartans_needed_rand, 'Spartans obtained': 0,
                                            'Happy? (T/F)': True}
                    self.client_orders_df.append(old_client_new_order, ignore_index=True)

                # END-OF-ORDER CODE
                fulfilled_index_list = self.client_orders_df.index[self.client_orders_df['Spartans requested'] ==
                                                                   self.client_orders_df['Spartans obtained']].tolist()
                time_up_index_list = self.client_orders_df.index[self.current_month ==
                                                                 self.client_orders_df['Month advert removed']].tolist()
                for index, i_row in self.client_orders_df.iterrows():  # i = index, row= all row info
                    if (index in fulfilled_index_list) and (self.current_month <= i_row['Month advert removed']):
                        i_row['Month advert removed'] = self.current_month
                    elif index in time_up_index_list:
                        i_row['Happy? (T/F)'] = False

# --- END of month-specific code ---
