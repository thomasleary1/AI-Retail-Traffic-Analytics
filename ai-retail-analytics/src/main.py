import cv2
import numpy as np
from camera import Camera
from analytics import Analytics
from customer_tracking import CustomerTracking

def main():
    camera = Camera()
    analytics = Analytics()
    customer_tracking = CustomerTracking()

    camera.start_capture()

    while True:
        frame = camera.get_frame()
        if frame is None:
            break

        current_customers = customer_tracking.track_customer(frame)

        if analytics.analyze_traffic(current_customers):
            print("Hourly Traffic (Hour: Number of Customers):")
            for hour, count in analytics.get_hourly_traffic().items():
                print(f"  Hour {hour} : {count} Customer(s)")

      
        for customer_id in current_customers:
            centroid, (x, y, w, h) = customer_tracking.customers[customer_id]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Retail Traffic Analytics', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# Exit on 'q' key press