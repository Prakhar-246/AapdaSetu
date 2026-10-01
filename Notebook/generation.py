import pandas as pd
import numpy as np
from faker import Faker

# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------

fake = Faker("en_IN")

# Reproducibility
np.random.seed(42)
Faker.seed(42)


# ---------------------------------------------------------
# INDIA STATE + DISTRICT LIST
# Prototype administrative district list
# ---------------------------------------------------------

india_districts = {

    "Andhra Pradesh": [
        "Alluri Sitharama Raju", "Anakapalli", "Anantapur",
        "Annamayya", "Bapatla", "Chittoor", "Dr. B.R. Ambedkar Konaseema",
        "East Godavari", "Eluru", "Guntur", "Kakinada", "Krishna",
        "Kurnool", "Nandyal", "NTR", "Palnadu", "Parvathipuram Manyam",
        "Prakasam", "Srikakulam", "Sri Sathya Sai", "Tirupati",
        "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa"
    ],

    "Arunachal Pradesh": [
        "Anjaw", "Bichom", "Changlang", "Dibang Valley",
        "East Kameng", "East Siang", "Itanagar Capital Complex",
        "Kamle", "Keyi Panyor", "Kra Daadi", "Kurung Kumey",
        "Lepa Rada", "Lohit", "Longding", "Lower Dibang Valley",
        "Lower Siang", "Lower Subansiri", "Namsai", "Pakke Kessang",
        "Papum Pare", "Shi Yomi", "Siang", "Tawang",
        "Tirap", "Upper Siang", "Upper Subansiri", "West Kameng",
        "West Siang"
    ],

    "Assam": [
        "Baksa", "Bajali", "Barpeta", "Biswanath", "Bongaigaon",
        "Cachar", "Charaideo", "Chirang", "Darrang", "Dhemaji",
        "Dhubri", "Dibrugarh", "Dima Hasao", "Goalpara", "Golaghat",
        "Hailakandi", "Hojai", "Jorhat", "Kamrup", "Kamrup Metropolitan",
        "Karbi Anglong", "Karimganj", "Kokrajhar", "Lakhimpur",
        "Majuli", "Morigaon", "Nagaon", "Nalbari", "Sivasagar",
        "Sonitpur", "South Salmara-Mankachar", "Tamulpur",
        "Tinsukia", "Udalguri", "West Karbi Anglong"
    ],

    "Bihar": [
        "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai",
        "Bhagalpur", "Bhojpur", "Buxar", "Darbhanga", "East Champaran",
        "Gaya", "Gopalganj", "Jamui", "Jehanabad", "Kaimur",
        "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura",
        "Madhubani", "Munger", "Muzaffarpur", "Nalanda", "Nawada",
        "Patna", "Purnia", "Rohtas", "Saharsa", "Samastipur",
        "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan",
        "Supaul", "Vaishali", "West Champaran"
    ],

    "Chhattisgarh": [
        "Balod", "Baloda Bazar", "Balrampur-Ramanujganj", "Bastar",
        "Bemetara", "Bijapur", "Bilaspur", "Dantewada", "Dhamtari",
        "Durg", "Gariaband", "Gaurela-Pendra-Marwahi", "Janjgir-Champa",
        "Jashpur", "Kabirdham", "Kanker", "Kondagaon", "Korba",
        "Korea", "Mahasamund", "Manendragarh-Chirmiri-Bharatpur",
        "Mohla-Manpur-Ambagarh Chowki", "Mungeli", "Narayanpur",
        "Raigarh", "Raipur", "Rajnandgaon", "Sakti", "Sarangarh-Bilaigarh",
        "Sukma", "Surajpur", "Surguja"
    ],

    "Goa": [
        "North Goa", "South Goa"
    ],

    "Gujarat": [
        "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha",
        "Bharuch", "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod",
        "Dang", "Devbhoomi Dwarka", "Gandhinagar", "Gir Somnath",
        "Jamnagar", "Junagadh", "Kheda", "Kutch", "Mahisagar",
        "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal",
        "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat",
        "Surendranagar", "Tapi", "Vadodara", "Valsad"
    ],

    "Haryana": [
        "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad",
        "Fatehabad", "Gurugram", "Hisar", "Jhajjar", "Jind",
        "Kaithal", "Karnal", "Kurukshetra", "Mahendragarh",
        "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari",
        "Rohtak", "Sirsa", "Sonipat", "Yamunanagar"
    ],

    "Himachal Pradesh": [
        "Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur",
        "Kullu", "Lahaul and Spiti", "Mandi", "Shimla",
        "Sirmaur", "Solan", "Una"
    ],

    "Jharkhand": [
        "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka",
        "East Singhbhum", "Garhwa", "Giridih", "Godda", "Gumla",
        "Hazaribagh", "Jamtara", "Khunti", "Koderma", "Latehar",
        "Lohardaga", "Pakur", "Palamu", "Ramgarh", "Ranchi",
        "Sahibganj", "Seraikela Kharsawan", "Simdega", "West Singhbhum"
    ],

    "Karnataka": [
        "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural",
        "Bengaluru Urban", "Bidar", "Chamarajanagar", "Chikkaballapur",
        "Chikkamagaluru", "Chitradurga", "Dakshina Kannada",
        "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri",
        "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya",
        "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
        "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura",
        "Yadgir"
    ],

    "Kerala": [
        "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod",
        "Kollam", "Kottayam", "Kozhikode", "Malappuram",
        "Palakkad", "Pathanamthitta", "Thiruvananthapuram",
        "Thrissur", "Wayanad"
    ],

    "Madhya Pradesh": [
        "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat",
        "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur",
        "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas",
        "Dhar", "Dindori", "Guna", "Gwalior", "Harda", "Indore",
        "Jabalpur", "Jhabua", "Katni", "Khandwa", "Khargone",
        "Maihar", "Mandla", "Mandsaur", "Mauganj", "Morena",
        "Narmadapuram", "Narsinghpur", "Neemuch", "Niwari", "Panna",
        "Raisen", "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna",
        "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur",
        "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain",
        "Umaria", "Vidisha"
    ],

    "Maharashtra": [
        "Ahmednagar", "Akola", "Amravati", "Aurangabad", "Beed",
        "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli",
        "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur",
        "Latur", "Mumbai City", "Mumbai Suburban", "Nagpur", "Nanded",
        "Nandurbar", "Nashik", "Osmanabad", "Palghar", "Parbhani",
        "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara",
        "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim",
        "Yavatmal"
    ],

    "Manipur": [
        "Bishnupur", "Chandel", "Churachandpur", "Imphal East",
        "Imphal West", "Jiribam", "Kakching", "Kamjong",
        "Kangpokpi", "Noney", "Pherzawl", "Senapati", "Tamenglong",
        "Tengnoupal", "Thoubal", "Ukhrul"
    ],

    "Meghalaya": [
        "East Garo Hills", "East Jaintia Hills", "East Khasi Hills",
        "Eastern West Khasi Hills", "North Garo Hills",
        "Ri Bhoi", "South Garo Hills", "South West Garo Hills",
        "South West Khasi Hills", "West Garo Hills",
        "West Jaintia Hills", "West Khasi Hills"
    ],

    "Mizoram": [
        "Aizawl", "Champhai", "Hnahthial", "Khawzawl",
        "Kolasib", "Lawngtlai", "Lunglei", "Mamit",
        "Saiha", "Serchhip", "Saitual"
    ],

    "Nagaland": [
        "Chumoukedima", "Dimapur", "Kiphire", "Kohima", "Longleng",
        "Mokokchung", "Mon", "Niuland", "Noklak", "Peren",
        "Phek", "Shamator", "Tuensang", "Wokha", "Zunheboto"
    ],

    "Odisha": [
        "Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak",
        "Boudh", "Cuttack", "Deogarh", "Dhenkanal", "Gajapati",
        "Ganjam", "Jagatsinghpur", "Jajpur", "Jharsuguda",
        "Kalahandi", "Kandhamal", "Kendrapara", "Keonjhar",
        "Khordha", "Koraput", "Malkangiri", "Mayurbhanj", "Nabarangpur",
        "Nayagarh", "Nuapada", "Puri", "Rayagada", "Sambalpur",
        "Subarnapur", "Sundargarh"
    ],

    "Punjab": [
        "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib",
        "Fazilka", "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar",
        "Kapurthala", "Ludhiana", "Malerkotla", "Mansa", "Moga",
        "Pathankot", "Patiala", "Rupnagar", "Sahibzada Ajit Singh Nagar",
        "Sangrur", "Shahid Bhagat Singh Nagar", "Sri Muktsar Sahib",
        "Tarn Taran"
    ],

    "Rajasthan": [
        "Ajmer", "Alwar", "Anupgarh", "Balotra", "Banswara",
        "Baran", "Barmer", "Beawar", "Bharatpur", "Bhilwara",
        "Bikaner", "Bundi", "Chittorgarh", "Churu", "Dausa",
        "Deeg", "Dholpur", "Didwana-Kuchamana", "Dudu", "Dungarpur",
        "Hanumangarh", "Jaipur", "Jaisalmer", "Jalore", "Jhalawar",
        "Jhunjhunu", "Jodhpur", "Karauli", "Kekri", "Khairthal-Tijara",
        "Kota", "Kotputli-Behror", "Nagaur", "Neem Ka Thana",
        "Pali", "Phalodi", "Pratapgarh", "Rajsamand", "Salumbar",
        "Sawai Madhopur", "Sikar", "Sirohi", "Sri Ganganagar",
        "Tonk", "Udaipur"
    ],

    "Sikkim": [
        "Gangtok", "Gyalshing", "Mangan", "Namchi", "Pakyong", "Soreng"
    ],

    "Tamil Nadu": [
        "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore",
        "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kallakurichi",
        "Kancheepuram", "Karur", "Krishnagiri", "Madurai",
        "Mayiladuthurai", "Nagapattinam", "Namakkal", "Nilgiris",
        "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet",
        "Salem", "Sivaganga", "Tenkasi", "Thanjavur", "Theni",
        "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur",
        "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur",
        "Vellore", "Viluppuram", "Virudhunagar"
    ],

    "Telangana": [
        "Adilabad", "Bhadradri Kothagudem", "Hanamkonda", "Hyderabad",
        "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal",
        "Kamareddy", "Karimnagar", "Khammam", "Komaram Bheem",
        "Mahabubabad", "Mahbubnagar", "Mancherial", "Medak",
        "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda",
        "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
        "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet",
        "Suryapet", "Vikarabad", "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri"
    ],

    "Tripura": [
        "Dhalai", "Gomati", "Khowai", "North Tripura",
        "Sepahijala", "South Tripura", "Unakoti", "West Tripura"
    ],

    "Uttar Pradesh": [
        "Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha",
        "Auraiya", "Ayodhya", "Azamgarh", "Baghpat", "Bahraich",
        "Ballia", "Balrampur", "Banda", "Barabanki", "Bareilly",
        "Basti", "Bhadohi", "Bijnor", "Budaun", "Bulandshahr",
        "Chandauli", "Chitrakoot", "Deoria", "Etah", "Etawah",
        "Farrukhabad", "Fatehpur", "Firozabad", "Gautam Buddha Nagar",
        "Ghaziabad", "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur",
        "Hapur", "Hardoi", "Hathras", "Jalaun", "Jaunpur",
        "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar",
        "Kasganj", "Kaushambi", "Kheri", "Kushinagar", "Lalitpur",
        "Lucknow", "Maharajganj", "Mahoba", "Mainpuri", "Mathura",
        "Mau", "Meerut", "Mirzapur", "Moradabad", "Muzaffarnagar",
        "Pilibhit", "Pratapgarh", "Prayagraj", "Raebareli",
        "Rampur", "Saharanpur", "Sambhal", "Sant Kabir Nagar",
        "Shahjahanpur", "Shamli", "Shravasti", "Siddharthnagar",
        "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"
    ],

    "Uttarakhand": [
        "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun",
        "Haridwar", "Nainital", "Pauri Garhwal", "Pithoragarh",
        "Rudraprayag", "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"
    ],

    "West Bengal": [
        "Alipurduar", "Bankura", "Paschim Bardhaman", "Purba Bardhaman",
        "Birbhum", "Cooch Behar", "Dakshin Dinajpur", "Darjeeling",
        "Hooghly", "Howrah", "Jalpaiguri", "Jhargram", "Kalimpong",
        "Kolkata", "Maldah", "Murshidabad", "Nadia", "North 24 Parganas",
        "South 24 Parganas", "Uttar Dinajpur", "Paschim Medinipur",
        "Purba Medinipur"
    ],

    # Union Territories

    "Andaman and Nicobar Islands": [
        "Nicobars", "North and Middle Andaman", "South Andaman"
    ],

    "Chandigarh": [
        "Chandigarh"
    ],

    "Dadra and Nagar Haveli and Daman and Diu": [
        "Dadra and Nagar Haveli", "Daman", "Diu"
    ],

    "Delhi": [
        "Central Delhi", "East Delhi", "New Delhi",
        "North Delhi", "North East Delhi", "North West Delhi",
        "Shahdara", "South Delhi", "South East Delhi",
        "South West Delhi", "West Delhi"
    ],

    "Jammu and Kashmir": [
        "Anantnag", "Bandipora", "Baramulla", "Budgam", "Doda",
        "Ganderbal", "Jammu", "Kathua", "Kishtwar", "Kulgam",
        "Kupwara", "Poonch", "Pulwama", "Rajouri", "Ramban",
        "Reasi", "Samba", "Shopian", "Srinagar", "Udhampur"
    ],

    "Ladakh": [
        "Kargil", "Leh"
    ],

    "Lakshadweep": [
        "Agatti", "Amini", "Andrott", "Bitra", "Chetlat",
        "Kadmat", "Kalpeni", "Kavaratti", "Kiltan", "Minicoy"
    ],

    "Puducherry": [
        "Karaikal", "Mahe", "Puducherry", "Yanam"
    ]
}


# ---------------------------------------------------------
# GENERATE DATA
# ---------------------------------------------------------

rows = []

area_counter = 1

for state, districts in india_districts.items():

    for district in districts:

        # -------------------------------
        # Population
        # -------------------------------

        population = int(
            np.clip(
                np.random.lognormal(mean=13.0, sigma=1.0),
                50000,
                8000000
            )
        )

        # -------------------------------
        # Urban percentage
        # -------------------------------

        urban_percentage = np.random.uniform(0.15, 0.85)

        urban_population = int(population * urban_percentage)
        rural_population = population - urban_population

        # -------------------------------
        # Gender
        # -------------------------------

        male_percentage = np.random.uniform(0.49, 0.53)

        male_population = int(population * male_percentage)
        female_population = population - male_population

        # -------------------------------
        # Age groups
        # -------------------------------

        children_percentage = np.random.uniform(0.08, 0.16)
        elderly_percentage = np.random.uniform(0.05, 0.14)

        children_population_0_6 = int(
            population * children_percentage
        )

        elderly_population_60_plus = int(
            population * elderly_percentage
        )

        # -------------------------------
        # Households
        # -------------------------------

        avg_household_size = np.random.uniform(3.5, 5.5)

        households = int(
            population / avg_household_size
        )

        # -------------------------------
        # Geographic area
        # -------------------------------

        area_sq_km = int(
            np.random.uniform(300, 15000)
        )

        # -------------------------------
        # Population density
        # -------------------------------

        population_density = round(
            population / area_sq_km,
            2
        )

        # -------------------------------
        # Hospitals
        #
        # Higher population → more hospitals
        # -------------------------------

        hospital_count = max(
            1,
            int(
                population / np.random.uniform(
                    40000,
                    70000
                )
            )
        )

        # -------------------------------
        # Ambulances
        #
        # Roughly related to population
        # -------------------------------

        ambulance_count = max(
            1,
            int(
                population / np.random.uniform(
                    20000,
                    50000
                )
            )
        )

        # -------------------------------
        # Shelter capacity
        # -------------------------------

        shelter_capacity = int(
            population * np.random.uniform(
                0.03,
                0.15
            )
        )

        # -------------------------------
        # Rescue teams
        # -------------------------------

        rescue_team_count = max(
            1,
            int(
                population / np.random.uniform(
                    100000,
                    250000
                )
            )
        )

        # -------------------------------
        # Store row
        # -------------------------------

        rows.append({

            "area_id":
                f"A{area_counter:04d}",

            "state":
                state,

            "district":
                district,

            "population":
                population,

            "households":
                households,

            "male_population":
                male_population,

            "female_population":
                female_population,

            "urban_population":
                urban_population,

            "rural_population":
                rural_population,

            "children_population_0_6":
                children_population_0_6,

            "elderly_population_60_plus":
                elderly_population_60_plus,

            "area_sq_km":
                area_sq_km,

            "population_density":
                population_density,

            "hospital_count":
                hospital_count,

            "ambulance_count":
                ambulance_count,

            "shelter_capacity":
                shelter_capacity,

            "rescue_team_count":
                rescue_team_count,

            "data_status":
                "synthetic_prototype"
        })

        area_counter += 1


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

areas_df = pd.DataFrame(rows)


# ---------------------------------------------------------
# SAVE CSV
# ---------------------------------------------------------

areas_df.to_csv(
    "areas.csv",
    index=False
)


# ---------------------------------------------------------
# BASIC CHECKS
# ---------------------------------------------------------

print("✅ areas.csv created successfully!")

print("\nDataset shape:")
print(areas_df.shape)

print("\nFirst 5 rows:")
print(areas_df.head())

print("\nColumns:")
print(list(areas_df.columns))

print("\nMissing values:")
print(areas_df.isnull().sum())

print("\nStates:")
print(areas_df["state"].nunique())

print("\nDistricts:")
print(areas_df["district"].nunique())



# =========================================================
# 3. GENERATE RESOURCES DATASET
# =========================================================

print("\nGenerating resources.csv...")

resources = []

resource_counter = 1

# Resource types
resource_types = [
    "Ambulance",
    "Rescue Team",
    "Medical Supply",
    "Shelter",
    "Hospital"
]

for _, area in areas_df.iterrows():

    state = area["state"]
    district = area["district"]

    population = int(area["population"])

    # -----------------------------------------------------
    # Number of resources for this area
    # -----------------------------------------------------

    ambulance_count = int(area["ambulance_count"])
    rescue_team_count = int(area["rescue_team_count"])
    hospital_count = int(area["hospital_count"])
    shelter_capacity = int(area["shelter_capacity"])

    # -----------------------------------------------------
    # Ambulances
    # -----------------------------------------------------

    for i in range(ambulance_count):

        resources.append({

            "resource_id": f"RES{resource_counter:05d}",

            "area_id": area["area_id"],

            "state": state,

            "district": district,

            "resource_type": "Ambulance",

            "resource_name":
                f"{fake.company()} Emergency Ambulance",

            "quantity": 1,

            "capacity":
                np.random.randint(2, 6),

            "availability_status":
                np.random.choice(
                    ["Available", "Busy", "Maintenance"],
                    p=[0.75, 0.20, 0.05]
                ),

            "condition":
                np.random.choice(
                    ["Good", "Average", "Needs Maintenance"],
                    p=[0.75, 0.20, 0.05]
                ),

            "data_status":
                "synthetic_prototype"
        })

        resource_counter += 1

    # -----------------------------------------------------
    # Rescue Teams
    # -----------------------------------------------------

    for i in range(rescue_team_count):

        resources.append({

            "resource_id": f"RES{resource_counter:05d}",

            "area_id": area["area_id"],

            "state": state,

            "district": district,

            "resource_type": "Rescue Team",

            "resource_name":
                f"{fake.company()} Rescue Team",

            "quantity":
                np.random.randint(4, 12),

            "capacity":
                np.random.randint(10, 30),

            "availability_status":
                np.random.choice(
                    ["Available", "Deployed", "Standby"],
                    p=[0.65, 0.25, 0.10]
                ),

            "condition":
                "Operational",

            "data_status":
                "synthetic_prototype"
        })

        resource_counter += 1

    # -----------------------------------------------------
    # Hospitals
    # -----------------------------------------------------

    for i in range(hospital_count):

        resources.append({

            "resource_id": f"RES{resource_counter:05d}",

            "area_id": area["area_id"],

            "state": state,

            "district": district,

            "resource_type": "Hospital",

            "resource_name":
                f"{fake.company()} General Hospital",

            "quantity": 1,

            "capacity":
                np.random.randint(50, 500),

            "availability_status":
                np.random.choice(
                    ["Available", "High Load", "Full"],
                    p=[0.55, 0.35, 0.10]
                ),

            "condition":
                np.random.choice(
                    ["Good", "Average"],
                    p=[0.85, 0.15]
                ),

            "data_status":
                "synthetic_prototype"
        })

        resource_counter += 1

    # -----------------------------------------------------
    # Medical Supplies
    # -----------------------------------------------------

    medical_quantity = max(
        100,
        int(
            population *
            np.random.uniform(0.001, 0.005)
        )
    )

    resources.append({

        "resource_id": f"RES{resource_counter:05d}",

        "area_id": area["area_id"],

        "state": state,

        "district": district,

        "resource_type": "Medical Supply",

        "resource_name":
            f"{fake.company()} Medical Supply Stock",

        "quantity":
            medical_quantity,

        "capacity":
            medical_quantity,

        "availability_status":
            np.random.choice(
                ["Available", "Low Stock", "Critical Stock"],
                p=[0.60, 0.30, 0.10]
            ),

        "condition":
            "Good",

        "data_status":
            "synthetic_prototype"
    })

    resource_counter += 1

    # -----------------------------------------------------
    # Shelter
    # -----------------------------------------------------

    resources.append({

        "resource_id": f"RES{resource_counter:05d}",

        "area_id": area["area_id"],

        "state": state,

        "district": district,

        "resource_type": "Shelter",

        "resource_name":
            f"{fake.company()} Emergency Shelter",

        "quantity": 1,

        "capacity":
            shelter_capacity,

        "availability_status":
            np.random.choice(
                ["Available", "Partially Occupied", "Full"],
                p=[0.60, 0.30, 0.10]
            ),

        "condition":
            np.random.choice(
                ["Good", "Average"],
                p=[0.85, 0.15]
            ),

        "data_status":
            "synthetic_prototype"
    })

    resource_counter += 1


# =========================================================
# CREATE DATAFRAME
# =========================================================

resources_df = pd.DataFrame(resources)


# =========================================================
# SAVE RESOURCES DATASET
# =========================================================

resources_df.to_csv(
    "resources.csv",
    index=False
)


# =========================================================
# CHECK
# =========================================================

print("\n✅ resources.csv created successfully!")

print("\nShape:")
print(resources_df.shape)

print("\nFirst 10 rows:")
print(resources_df.head(10))

print("\nResource types:")
print(
    resources_df["resource_type"]
    .value_counts()
)

print("\nMissing values:")
print(
    resources_df.isnull().sum()
)


# ============================================================
# 4. INCIDENT DATASET GENERATION
# ============================================================

print("\nGenerating incident_dataset.csv...")

# Disaster data load karo
disasters_df = pd.read_csv("disaster_dataset_cleaned.csv")

# Randomness reproducible rakho
np.random.seed(42)

incident_rows = []

# Disaster types ke base severity factors
severity_map = {
    "Earthquake": 0.90,
    "Tsunami": 0.95,
    "Cyclone": 0.85,
    "Flood": 0.75,
    "Flash Flood": 0.80,
    "Landslide": 0.75,
    "Wildfire": 0.70,
    "Extreme temperature": 0.65,
    "Drought": 0.45,
    "Epidemic": 0.70,
    "Storm": 0.80,
    "Volcanic activity": 0.90,
    "Mass movement (dry)": 0.70,
    "Insect infestation": 0.35
}


# ------------------------------------------------------------
# RESOURCE SUMMARY AREA-WISE
# ------------------------------------------------------------

resource_summary = []

for area_id, group in resources_df.groupby("area_id"):

    # Ambulances
    ambulance_rows = group[group["resource_type"] == "Ambulance"]

    available_ambulances = (
        ambulance_rows["availability_status"]
        .eq("Available")
        .sum()
    )

    total_ambulances = len(ambulance_rows)

    # Rescue teams
    rescue_rows = group[group["resource_type"] == "Rescue Team"]

    available_rescue_teams = (
        rescue_rows["availability_status"]
        .eq("Available")
        .sum()
    )

    total_rescue_teams = len(rescue_rows)

    # Hospitals
    hospital_rows = group[group["resource_type"] == "Hospital"]

    hospital_capacity = hospital_rows.loc[
        hospital_rows["availability_status"] != "Full",
        "capacity"
    ].sum()

    # Medical supplies
    medical_rows = group[
        group["resource_type"] == "Medical Supply"
    ]

    medical_supply = medical_rows["quantity"].sum()

    # Shelter
    shelter_rows = group[
        group["resource_type"] == "Shelter"
    ]

    available_shelter_capacity = shelter_rows.loc[
        shelter_rows["availability_status"] != "Full",
        "capacity"
    ].sum()

    resource_summary.append({
        "area_id": area_id,
        "available_ambulances": int(available_ambulances),
        "total_ambulances": int(total_ambulances),
        "available_rescue_teams": int(available_rescue_teams),
        "total_rescue_teams": int(total_rescue_teams),
        "hospital_capacity": int(hospital_capacity),
        "medical_supply": int(medical_supply),
        "available_shelter_capacity": int(
            available_shelter_capacity
        )
    })


resource_summary_df = pd.DataFrame(resource_summary)


# ------------------------------------------------------------
# MERGE AREA + RESOURCE INFORMATION
# ------------------------------------------------------------

area_resource_df = areas_df.merge(
    resource_summary_df,
    on="area_id",
    how="left"
)


# ------------------------------------------------------------
# GENERATE INCIDENTS
# ------------------------------------------------------------

# Har historical disaster ke multiple scenarios banayenge
# 12 scenarios × 432 disasters = ~5184 rows

SCENARIOS_PER_DISASTER = 12

for _, disaster in disasters_df.iterrows():

    disaster_type = str(
        disaster["Disaster Type"]
    )

    disaster_subtype = str(
        disaster["Disaster Subtype"]
    )

    disaster_id = str(
        disaster["DisNo."]
    )

    # Historical impact
    historical_affected = disaster["Total Affected"]

    if pd.isna(historical_affected):
        historical_affected = disaster["No. Affected"]

    if pd.isna(historical_affected):
        historical_affected = 0

    historical_affected = max(
        0,
        float(historical_affected)
    )

    # Historical deaths
    historical_deaths = disaster["Total Deaths"]

    if pd.isna(historical_deaths):
        historical_deaths = 0

    historical_deaths = max(
        0,
        float(historical_deaths)
    )

    # Historical injured
    historical_injured = disaster["No. Injured"]

    if pd.isna(historical_injured):
        historical_injured = 0

    historical_injured = max(
        0,
        float(historical_injured)
    )

    # Base severity
    base_severity = severity_map.get(
        disaster_type,
        0.60
    )

    for scenario in range(SCENARIOS_PER_DISASTER):

        # Random area select
        area = area_resource_df.sample(
            n=1
        ).iloc[0]

        population = int(area["population"])

        # ----------------------------------------------------
        # IMPACT MULTIPLIER
        # ----------------------------------------------------

        impact_multiplier = np.random.uniform(
            0.5,
            1.5
        )

        # Historical affected population se impact
        if historical_affected > 0:

            people_affected = int(
                historical_affected
                * impact_multiplier
            )

        else:

            affected_ratio = np.random.uniform(
                0.02,
                0.30
            )

            people_affected = int(
                population
                * affected_ratio
            )

        # Population se zyada affected nahi ho sakte
        people_affected = min(
            people_affected,
            int(population * 0.80)
        )

        people_affected = max(
            people_affected,
            10
        )

        # ----------------------------------------------------
        # DEATHS
        # ----------------------------------------------------

        if historical_affected > 0:

            death_rate = (
                historical_deaths
                / historical_affected
            )

            death_rate = np.clip(
                death_rate,
                0.0001,
                0.08
            )

        else:

            death_rate = np.random.uniform(
                0.001,
                0.03
            )

        deaths = int(
            people_affected
            * death_rate
            * np.random.uniform(0.7, 1.3)
        )

        deaths = min(
            deaths,
            people_affected
        )

        # ----------------------------------------------------
        # INJURED
        # ----------------------------------------------------

        if historical_affected > 0:

            injured_rate = (
                historical_injured
                / historical_affected
            )

            injured_rate = np.clip(
                injured_rate,
                0.005,
                0.15
            )

        else:

            injured_rate = np.random.uniform(
                0.01,
                0.08
            )

        injured = int(
            people_affected
            * injured_rate
            * np.random.uniform(0.7, 1.3)
        )

        injured = min(
            injured,
            people_affected
        )

        # ----------------------------------------------------
        # CRITICAL PATIENTS
        # ----------------------------------------------------

        critical_patients = int(
            injured
            * np.random.uniform(
                0.15,
                0.35
            )
        )

        # ----------------------------------------------------
        # VULNERABLE POPULATION
        # ----------------------------------------------------

        children_affected = int(
            people_affected
            * area["children_population_0_6"]
            / area["population"]
        )

        elderly_affected = int(
            people_affected
            * area["elderly_population_60_plus"]
            / area["population"]
        )

        vulnerable_ratio = (
            children_affected
            + elderly_affected
        ) / max(
            people_affected,
            1
        )

        # ----------------------------------------------------
        # SEVERITY SCORE
        # ----------------------------------------------------

        severity_score = (
            base_severity
            + np.random.uniform(-0.10, 0.10)
        )

        severity_score = np.clip(
            severity_score,
            0,
            1
        )

        # ----------------------------------------------------
        # RESOURCE DEMAND
        # ----------------------------------------------------

        ambulance_demand = max(
            1,
            int(np.ceil(
                critical_patients / 4
            ))
        )

        rescue_team_demand = max(
            1,
            int(np.ceil(
                people_affected / 5000
            ))
        )

        shelter_demand = int(
            people_affected
            * np.random.uniform(
                0.30,
                0.70
            )
        )

        medical_supply_demand = int(
            injured
            * np.random.uniform(
                3,
                8
            )
        )

        # ----------------------------------------------------
        # RESOURCE SHORTAGE
        # ----------------------------------------------------

        available_ambulances = int(
            area["available_ambulances"]
        )

        available_rescue_teams = int(
            area["available_rescue_teams"]
        )

        hospital_capacity = int(
            area["hospital_capacity"]
        )

        available_shelter_capacity = int(
            area["available_shelter_capacity"]
        )

        medical_supply = int(
            area["medical_supply"]
        )

        ambulance_shortage = max(
            0,
            ambulance_demand
            - available_ambulances
        ) / max(
            ambulance_demand,
            1
        )

        rescue_shortage = max(
            0,
            rescue_team_demand
            - available_rescue_teams
        ) / max(
            rescue_team_demand,
            1
        )

        shelter_shortage = max(
            0,
            shelter_demand
            - available_shelter_capacity
        ) / max(
            shelter_demand,
            1
        )

        medical_shortage = max(
            0,
            medical_supply_demand
            - medical_supply
        ) / max(
            medical_supply_demand,
            1
        )

        hospital_load = min(
            injured / max(
                hospital_capacity,
                1
            ),
            1
        )

        resource_shortage = (
            0.30 * ambulance_shortage
            + 0.20 * rescue_shortage
            + 0.25 * shelter_shortage
            + 0.15 * medical_shortage
            + 0.10 * hospital_load
        )

        resource_shortage = np.clip(
            resource_shortage,
            0,
            1
        )

        # ----------------------------------------------------
        # PRIORITY SCORE
        # ----------------------------------------------------

        affected_ratio = (
            people_affected
            / population
        )

        affected_score = min(
            affected_ratio / 0.50,
            1
        )

        critical_ratio = (
            critical_patients
            / max(
                people_affected,
                1
            )
        )

        critical_score = min(
            critical_ratio / 0.10,
            1
        )

        priority_score = (
            30 * affected_score
            + 25 * critical_score
            + 20 * severity_score
            + 15 * resource_shortage
            + 10 * min(
                vulnerable_ratio / 0.30,
                1
            )
        )

        priority_score = np.clip(
            priority_score,
            0,
            100
        )

        # ----------------------------------------------------
        # PRIORITY LEVEL
        # ----------------------------------------------------

        if priority_score <= 25:

            priority_level = "LOW"

        elif priority_score <= 50:

            priority_level = "MEDIUM"

        elif priority_score <= 75:

            priority_level = "HIGH"

        else:

            priority_level = "CRITICAL"

        # ----------------------------------------------------
        # INCIDENT ROW
        # ----------------------------------------------------

        incident_rows.append({

            "incident_id":
                f"INC{len(incident_rows)+1:06d}",

            "disaster_id":
                disaster_id,

            "area_id":
                area["area_id"],

            "state":
                area["state"],

            "district":
                area["district"],

            "disaster_type":
                disaster_type,

            "disaster_subtype":
                disaster_subtype,

            "population":
                population,

            "people_affected":
                people_affected,

            "deaths":
                deaths,

            "injured":
                injured,

            "critical_patients":
                critical_patients,

            "children_affected":
                children_affected,

            "elderly_affected":
                elderly_affected,

            "hospital_count":
                int(area["hospital_count"]),

            "ambulance_count":
                int(area["total_ambulances"]),

            "available_ambulances":
                available_ambulances,

            "rescue_team_count":
                int(area["total_rescue_teams"]),

            "available_rescue_teams":
                available_rescue_teams,

            "shelter_capacity":
                int(area["shelter_capacity"]),

            "available_shelter_capacity":
                available_shelter_capacity,

            "hospital_capacity":
                hospital_capacity,

            "medical_supply":
                medical_supply,

            "ambulance_demand":
                ambulance_demand,

            "rescue_team_demand":
                rescue_team_demand,

            "shelter_demand":
                shelter_demand,

            "medical_supply_demand":
                medical_supply_demand,

            "resource_shortage":
                round(
                    resource_shortage,
                    4
                ),

            "severity_score":
                round(
                    severity_score,
                    4
                ),

            "vulnerable_ratio":
                round(
                    vulnerable_ratio,
                    4
                ),

            "priority_score":
                round(
                    priority_score,
                    2
                ),

            "priority_level":
                priority_level,

            "data_status":
                "synthetic_scenario"
        })


# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

incident_df = pd.DataFrame(
    incident_rows
)


# ------------------------------------------------------------
# SAVE DATASET
# ------------------------------------------------------------

incident_df.to_csv(
    "incident_dataset.csv",
    index=False
)


print("\n✅ incident_dataset.csv created successfully!")

print(
    "Dataset shape:",
    incident_df.shape
)

print("\nPriority distribution:")

print(
    incident_df["priority_level"]
    .value_counts()
)

print("\nFirst 5 rows:")

print(
    incident_df.head()
)