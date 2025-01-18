import cv2
import csv
import requests  # Import requests to fetch the array from the web app
from datetime import date, datetime

# Time and date setup
today = date.today()
date_str = today.strftime("%d-%b-%Y")
now = datetime.now()
timeRN = now.strftime("%H:%M:%S")

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access the camera")
    exit()

detector = cv2.QRCodeDetector()

# URL to fetch product array from the web app
PRODUCTS_URL = "https://autocart-production.up.railway.app/get_products"  # Replace <WEB_APP_IP> with the actual IP address

# Infinite loop for QR code detection
while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None and len(bbox) > 0:
        bbox = bbox.astype(int)  # Ensure bounding box points are integers
        for i in range(len(bbox[0])):
            start_point = tuple(bbox[0][i])
            end_point = tuple(bbox[0][(i + 1) % len(bbox[0])])
            cv2.line(img, start_point, end_point, color=(255, 0, 0), thickness=2)

        if data:
            print("Data found in Qr: ", data, date_str, timeRN)
            with open('Database.csv', mode='a') as csvfile:
                csvfileWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                csvfileWriter.writerow([data, date_str, timeRN])

            try:
                # Fetch product array from the web app
                response = requests.get(PRODUCTS_URL)
                response.raise_for_status()
                products = response.json()  # Assuming the web app sends a JSON list
                print(products)
                product_list = products.get("products", [])  # Extract the list of products safely
                print(product_list)

                if data in product_list:
                    print("Product is in the list: ", data)
                else:
                    print("Product is not in the list: ", data)
            except Exception as e:
                print("Error fetching products:", e)

    cv2.imshow("QR Code Detector", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
