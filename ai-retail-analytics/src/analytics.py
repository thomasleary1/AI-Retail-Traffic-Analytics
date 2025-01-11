from collections import defaultdict
from datetime import datetime

class Analytics:
    def __init__(self):
        self.total_customers = 0
        self.seen_customers = set() 
        self.current_customers = set() 
        self.hourly_traffic = defaultdict(int)

    def analyze_traffic(self, current_customer_ids):
        new_customers = 0

        for customer_id in current_customer_ids:
            if customer_id not in self.seen_customers:
           
                self.seen_customers.add(customer_id)
                new_customers += 1

           
                current_hour = datetime.now().hour
                self.hourly_traffic[current_hour] += 1

        self.total_customers += new_customers

        self.current_customers = set(current_customer_ids) 

        return new_customers > 0

    def get_total_customers(self):
        return self.total_customers

    def get_hourly_traffic(self):
        return dict(self.hourly_traffic)