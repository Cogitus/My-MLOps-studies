"""import libraries"""
import pandas as pd



autos = pd.read_csv('autos.csv', encoding='Latin-1')

columns_new_names = {
    'dateCrawled': 'date_crawled',
    'name': 'name',
    'seller': 'seller',
    'offerType': 'offer_type',
    'price': 'price',
    'abtest': 'abtest',
    'vehicleType': 'vehicle_type',
    'yearOfRegistration': 'registration_year',
    'gearbox': 'gearbox',
    'powerPS': 'power_ps',
    'model': 'model',
    'odometer': 'odometer',
    'monthOfRegistration': 'registration_month',
    'fuelType': 'fuel_type',
    'brand': 'brand',
    'notRepairedDamage': 'unrepaired_damage',
    'dateCreated': 'ad_created',
    'nrOfPictures': 'nr_of_pictures',
    'postalCode': 'postal_code',
    'lastSeen': 'last_seen'
}

autos.rename(columns=columns_new_names, inplace=True)

# dropping unecessary columns
autos.drop(columns=['seller', 'offer_type'], inplace=True)
autos['unrepaired_damage'].replace({'nein': 'no', 'ja': 'yes'}, inplace=True)

autos['price'].replace([r'\$', ','], '', regex=True, inplace=True)
autos['price'] = [float(price) for price in autos.price]

autos['odometer'].replace([',', 'km'], '', regex=True, inplace=True)
autos['odometer'] = [float(distance) for distance in autos.odometer]
autos.rename(columns={'odometer': 'odometer_km'}, inplace=True)

# remove outliers
autos = autos[autos['price'].between(1.0, 350000.0)]

# first 20 is the criteria
brand_list = autos['brand'].value_counts().head(20).index

dictionary_cars_brand = {}
dictinary_odometer_mean = {}
for brand in brand_list:
    dictionary_cars_brand[brand] = autos[autos['brand'] == brand]['price'].mean()
    dictinary_odometer_mean[brand] = autos[autos['brand'] == brand]['odometer_km'].mean()

mean_brand_price = pd.Series(dictionary_cars_brand)
mean_odometer_km = pd.Series(dictinary_odometer_mean)

dataframe_brand = pd.DataFrame(mean_brand_price, columns = ['mean_price'])
dataframe_brand['mean_odometer_km'] = mean_odometer_km
