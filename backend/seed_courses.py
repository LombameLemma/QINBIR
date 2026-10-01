import sqlite3


DB_NAME = "qinbir.db"


# ---------------------------------------------------------
# COURSE CATALOG
# ---------------------------------------------------------

course_catalog = {

    # =====================================================
    # COMPUTATIONAL AND NATURAL SCIENCE
    # =====================================================

    "CS": [
        ("CS101", "Introduction to Programming", 3),
        ("CS102", "Programming II", 3),
        ("CS201", "Data Structures and Algorithms", 3),
        ("CS202", "Object-Oriented Programming", 3),
        ("CS203", "Discrete Mathematics", 3),
        ("CS204", "Computer Organization", 3),
        ("CS301", "Database Systems", 3),
        ("CS302", "Operating Systems", 3),
        ("CS303", "Computer Networks", 3),
        ("CS304", "Software Engineering", 3),
        ("CS305", "Web Programming", 3),
        ("CS306", "Mobile Application Development", 3),
        ("CS307", "Artificial Intelligence", 3),
        ("CS308", "Machine Learning", 3),
        ("CS309", "Computer Graphics", 3),
        ("CS310", "Theory of Computation", 3),
        ("CS401", "Information Security", 3),
        ("CS402", "Senior Project", 3),
    ],

    "IS": [
        ("IS101", "Introduction to Information Systems", 3),
        ("IS102", "Programming Fundamentals", 3),
        ("IS201", "Database Systems", 3),
        ("IS202", "Systems Analysis and Design", 3),
        ("IS203", "Information Systems Development", 3),
        ("IS204", "Web Development", 3),
        ("IS301", "Business Process Management", 3),
        ("IS302", "Enterprise Information Systems", 3),
        ("IS303", "IT Project Management", 3),
        ("IS304", "Information Security", 3),
        ("IS305", "Data Communications", 3),
        ("IS306", "Human-Computer Interaction", 3),
        ("IS307", "Information Management", 3),
        ("IS308", "E-Commerce", 3),
        ("IS309", "Business Intelligence", 3),
        ("IS401", "Systems Administration", 3),
        ("IS402", "Information Systems Project", 3),
    ],

    "MATH": [
        ("MATH101", "Calculus I", 3),
        ("MATH102", "Calculus II", 3),
        ("MATH201", "Calculus III", 3),
        ("MATH202", "Linear Algebra", 3),
        ("MATH203", "Analytical Geometry", 3),
        ("MATH204", "Differential Equations", 3),
        ("MATH301", "Abstract Algebra", 3),
        ("MATH302", "Real Analysis", 3),
        ("MATH303", "Complex Analysis", 3),
        ("MATH304", "Numerical Analysis", 3),
        ("MATH305", "Probability Theory", 3),
        ("MATH306", "Mathematical Statistics", 3),
        ("MATH307", "Number Theory", 3),
        ("MATH308", "Mathematical Modeling", 3),
        ("MATH401", "Operations Research", 3),
        ("MATH402", "Discrete Mathematics", 3),
    ],

    "PHY": [
        ("PHY101", "General Physics I", 3),
        ("PHY102", "General Physics II", 3),
        ("PHY201", "Classical Mechanics", 3),
        ("PHY202", "Electricity and Magnetism", 3),
        ("PHY203", "Mathematical Physics", 3),
        ("PHY204", "Waves and Optics", 3),
        ("PHY301", "Thermodynamics", 3),
        ("PHY302", "Quantum Mechanics", 3),
        ("PHY303", "Atomic Physics", 3),
        ("PHY304", "Nuclear Physics", 3),
        ("PHY305", "Solid State Physics", 3),
        ("PHY306", "Electronics", 3),
        ("PHY307", "Computational Physics", 3),
        ("PHY401", "Experimental Physics", 3),
    ],

    "STAT": [
        ("STAT101", "Introduction to Statistics", 3),
        ("STAT102", "Probability Theory", 3),
        ("STAT201", "Statistical Methods I", 3),
        ("STAT202", "Statistical Methods II", 3),
        ("STAT203", "Mathematical Statistics", 3),
        ("STAT301", "Regression Analysis", 3),
        ("STAT302", "Experimental Design", 3),
        ("STAT303", "Sampling Techniques", 3),
        ("STAT304", "Time Series Analysis", 3),
        ("STAT305", "Multivariate Statistics", 3),
        ("STAT306", "Statistical Computing", 3),
        ("STAT307", "Econometrics", 3),
        ("STAT308", "Survey Methodology", 3),
        ("STAT401", "Data Analysis", 3),
    ],

    "CHEM": [
        ("CHEM101", "General Chemistry I", 3),
        ("CHEM102", "General Chemistry II", 3),
        ("CHEM201", "Analytical Chemistry", 3),
        ("CHEM202", "Organic Chemistry I", 3),
        ("CHEM203", "Organic Chemistry II", 3),
        ("CHEM204", "Physical Chemistry I", 3),
        ("CHEM301", "Physical Chemistry II", 3),
        ("CHEM302", "Inorganic Chemistry", 3),
        ("CHEM303", "Biochemistry", 3),
        ("CHEM304", "Instrumental Analysis", 3),
        ("CHEM305", "Environmental Chemistry", 3),
        ("CHEM306", "Industrial Chemistry", 3),
        ("CHEM307", "Chemical Safety", 3),
        ("CHEM401", "Laboratory Techniques", 3),
    ],

    "BIO": [
        ("BIO101", "General Biology", 3),
        ("BIO102", "Cell Biology", 3),
        ("BIO201", "Genetics", 3),
        ("BIO202", "Microbiology", 3),
        ("BIO203", "Ecology", 3),
        ("BIO204", "Evolutionary Biology", 3),
        ("BIO301", "Plant Biology", 3),
        ("BIO302", "Animal Biology", 3),
        ("BIO303", "Biochemistry", 3),
        ("BIO304", "Molecular Biology", 3),
        ("BIO305", "Developmental Biology", 3),
        ("BIO306", "Conservation Biology", 3),
        ("BIO307", "Biotechnology", 3),
        ("BIO401", "Biological Techniques", 3),
    ],


    # =====================================================
    # SOCIAL SCIENCE
    # =====================================================

    "ECON": [
        ("ECON101", "Principles of Economics I", 3),
        ("ECON102", "Principles of Economics II", 3),
        ("ECON201", "Microeconomics I", 3),
        ("ECON202", "Macroeconomics I", 3),
        ("ECON203", "Microeconomics II", 3),
        ("ECON204", "Macroeconomics II", 3),
        ("ECON301", "Mathematics for Economists", 3),
        ("ECON302", "Statistics for Economists", 3),
        ("ECON303", "Econometrics I", 3),
        ("ECON304", "Econometrics II", 3),
        ("ECON305", "Development Economics", 3),
        ("ECON306", "International Economics", 3),
        ("ECON307", "Public Economics", 3),
        ("ECON308", "Monetary Economics", 3),
        ("ECON401", "Ethiopian Economy", 3),
        ("ECON402", "Economic Policy", 3),
        ("ECON403", "Research Methods", 3),
    ],

    "MGT": [
        ("MGT101", "Principles of Management", 3),
        ("MGT102", "Principles of Marketing", 3),
        ("MGT201", "Financial Management", 3),
        ("MGT202", "Human Resource Management", 3),
        ("MGT203", "Organizational Behavior", 3),
        ("MGT204", "Operations Management", 3),
        ("MGT301", "Strategic Management", 3),
        ("MGT302", "Entrepreneurship", 3),
        ("MGT303", "Business Communication", 3),
        ("MGT304", "Management Information Systems", 3),
        ("MGT305", "Project Management", 3),
        ("MGT306", "Business Research Methods", 3),
        ("MGT307", "International Business", 3),
        ("MGT401", "Leadership", 3),
        ("MGT402", "Small Business Management", 3),
    ],

    "AF": [
        ("AF101", "Financial Accounting I", 3),
        ("AF102", "Financial Accounting II", 3),
        ("AF201", "Cost Accounting", 3),
        ("AF202", "Management Accounting", 3),
        ("AF203", "Intermediate Accounting I", 3),
        ("AF204", "Intermediate Accounting II", 3),
        ("AF301", "Auditing I", 3),
        ("AF302", "Auditing II", 3),
        ("AF303", "Taxation", 3),
        ("AF304", "Financial Management", 3),
        ("AF305", "Corporate Finance", 3),
        ("AF306", "Accounting Information Systems", 3),
        ("AF307", "Public Finance", 3),
        ("AF308", "Investment Analysis", 3),
        ("AF401", "Financial Reporting", 3),
        ("AF402", "Accounting Research", 3),
    ],

    "SOC": [
        ("SOC101", "Introduction to Sociology", 3),
        ("SOC201", "Sociological Theory", 3),
        ("SOC202", "Social Research Methods", 3),
        ("SOC203", "Social Statistics", 3),
        ("SOC204", "Sociology of Family", 3),
        ("SOC301", "Sociology of Education", 3),
        ("SOC302", "Sociology of Development", 3),
        ("SOC303", "Urban Sociology", 3),
        ("SOC304", "Rural Sociology", 3),
        ("SOC305", "Sociology of Religion", 3),
        ("SOC306", "Gender and Society", 3),
        ("SOC307", "Social Stratification", 3),
        ("SOC308", "Population Studies", 3),
        ("SOC401", "Ethiopian Society", 3),
    ],

    "PSY": [
        ("PSY101", "Introduction to Psychology", 3),
        ("PSY201", "Developmental Psychology", 3),
        ("PSY202", "Social Psychology", 3),
        ("PSY203", "Cognitive Psychology", 3),
        ("PSY204", "Personality Psychology", 3),
        ("PSY205", "Biological Psychology", 3),
        ("PSY301", "Abnormal Psychology", 3),
        ("PSY302", "Psychological Assessment", 3),
        ("PSY303", "Research Methods in Psychology", 3),
        ("PSY304", "Counseling Psychology", 3),
        ("PSY305", "Educational Psychology", 3),
        ("PSY306", "Industrial and Organizational Psychology", 3),
        ("PSY307", "Health Psychology", 3),
        ("PSY401", "Psychology of Learning", 3),
    ],

    "PSIR": [
        ("PSIR101", "Introduction to Political Science", 3),
        ("PSIR201", "Political Theory", 3),
        ("PSIR202", "Comparative Politics", 3),
        ("PSIR203", "Ethiopian Government and Politics", 3),
        ("PSIR204", "International Relations", 3),
        ("PSIR301", "International Organizations", 3),
        ("PSIR302", "International Political Economy", 3),
        ("PSIR303", "Public Administration", 3),
        ("PSIR304", "Public Policy", 3),
        ("PSIR305", "Political Sociology", 3),
        ("PSIR306", "African Politics", 3),
        ("PSIR307", "Conflict Resolution", 3),
        ("PSIR308", "Diplomacy", 3),
        ("PSIR309", "Human Rights", 3),
        ("PSIR401", "Research Methods", 3),
    ],

    "GEOG": [
        ("GEOG101", "Introduction to Geography", 3),
        ("GEOG102", "Physical Geography", 3),
        ("GEOG201", "Human Geography", 3),
        ("GEOG202", "Economic Geography", 3),
        ("GEOG203", "Population Geography", 3),
        ("GEOG204", "Urban Geography", 3),
        ("GEOG301", "Regional Geography", 3),
        ("GEOG302", "Cartography", 3),
        ("GEOG303", "Geographic Information Systems", 3),
        ("GEOG304", "Remote Sensing", 3),
        ("GEOG305", "Environmental Management", 3),
        ("GEOG306", "Climate Change", 3),
        ("GEOG307", "Geomorphology", 3),
        ("GEOG401", "Land Use Planning", 3),
        ("GEOG402", "Research Methods", 3),
    ],

    "SW": [
        ("SW101", "Introduction to Social Work", 3),
        ("SW201", "Social Work Practice", 3),
        ("SW202", "Social Work Methods", 3),
        ("SW203", "Human Behavior and Social Environment", 3),
        ("SW204", "Community Development", 3),
        ("SW301", "Social Welfare Policy", 3),
        ("SW302", "Child Welfare", 3),
        ("SW303", "Family Social Work", 3),
        ("SW304", "Medical Social Work", 3),
        ("SW305", "School Social Work", 3),
        ("SW306", "Social Work Research", 3),
        ("SW307", "Case Management", 3),
        ("SW308", "Counseling Skills", 3),
        ("SW401", "Social Work Practicum", 3),
    ],


    # =====================================================
    # HEALTH
    # =====================================================

    "PH": [
        ("PH101", "Introduction to Public Health", 3),
        ("PH201", "Epidemiology I", 3),
        ("PH202", "Epidemiology II", 3),
        ("PH203", "Biostatistics", 3),
        ("PH204", "Environmental Health", 3),
        ("PH301", "Community Health", 3),
        ("PH302", "Health Promotion", 3),
        ("PH303", "Maternal and Child Health", 3),
        ("PH304", "Nutrition in Public Health", 3),
        ("PH305", "Communicable Diseases", 3),
        ("PH306", "Non-Communicable Diseases", 3),
        ("PH307", "Health Policy and Management", 3),
        ("PH308", "Public Health Research", 3),
        ("PH401", "Field Epidemiology", 3),
        ("PH402", "Public Health Practicum", 3),
    ],

    "NUR": [
        ("NUR101", "Fundamentals of Nursing", 3),
        ("NUR102", "Anatomy and Physiology", 3),
        ("NUR201", "Microbiology", 3),
        ("NUR202", "Pharmacology", 3),
        ("NUR203", "Adult Health Nursing I", 3),
        ("NUR204", "Adult Health Nursing II", 3),
        ("NUR301", "Pediatric Nursing", 3),
        ("NUR302", "Maternal and Newborn Nursing", 3),
        ("NUR303", "Mental Health Nursing", 3),
        ("NUR304", "Community Health Nursing", 3),
        ("NUR305", "Emergency Nursing", 3),
        ("NUR306", "Nursing Research", 3),
        ("NUR307", "Nursing Leadership", 3),
        ("NUR401", "Clinical Practicum", 3),
    ],

    "MLS": [
        ("MLS101", "General Biology", 3),
        ("MLS102", "Anatomy and Physiology", 3),
        ("MLS103", "General Chemistry", 3),
        ("MLS201", "Medical Microbiology", 3),
        ("MLS202", "Clinical Chemistry", 3),
        ("MLS203", "Hematology", 3),
        ("MLS204", "Immunology", 3),
        ("MLS301", "Parasitology", 3),
        ("MLS302", "Histopathology", 3),
        ("MLS303", "Molecular Diagnostics", 3),
        ("MLS304", "Blood Banking", 3),
        ("MLS305", "Laboratory Management", 3),
        ("MLS401", "Clinical Laboratory Practice", 3),
        ("MLS402", "Medical Laboratory Research", 3),
    ],

    "MID": [
        ("MID101", "Anatomy and Physiology", 3),
        ("MID102", "Fundamentals of Midwifery", 3),
        ("MID201", "Reproductive Health", 3),
        ("MID202", "Antenatal Care", 3),
        ("MID203", "Normal Labor and Delivery", 3),
        ("MID204", "Complicated Pregnancy", 3),
        ("MID301", "Emergency Obstetric Care", 3),
        ("MID302", "Newborn Care", 3),
        ("MID303", "Postnatal Care", 3),
        ("MID304", "Family Planning", 3),
        ("MID305", "Maternal and Child Health", 3),
        ("MID306", "Midwifery Research", 3),
        ("MID401", "Clinical Midwifery Practicum", 3),
    ],

    "PHARM": [
        ("PHARM101", "General Chemistry", 3),
        ("PHARM102", "Organic Chemistry", 3),
        ("PHARM103", "Biochemistry", 3),
        ("PHARM104", "Human Anatomy and Physiology", 3),
        ("PHARM201", "Pharmacology", 3),
        ("PHARM202", "Pharmaceutics", 3),
        ("PHARM203", "Pharmaceutical Chemistry", 3),
        ("PHARM204", "Pharmacognosy", 3),
        ("PHARM301", "Clinical Pharmacy", 3),
        ("PHARM302", "Drug Information", 3),
        ("PHARM303", "Pharmaceutical Microbiology", 3),
        ("PHARM304", "Toxicology", 3),
        ("PHARM305", "Pharmacy Practice", 3),
        ("PHARM306", "Community Pharmacy", 3),
        ("PHARM307", "Hospital Pharmacy", 3),
        ("PHARM401", "Pharmacy Research", 3),
    ],

    "HI": [
        ("HI101", "Introduction to Health Informatics", 3),
        ("HI102", "Programming Fundamentals", 3),
        ("HI201", "Database Systems", 3),
        ("HI202", "Health Information Systems", 3),
        ("HI203", "Medical Terminology", 3),
        ("HI204", "Health Data Management", 3),
        ("HI301", "Biostatistics", 3),
        ("HI302", "Health Information Standards", 3),
        ("HI303", "Electronic Health Records", 3),
        ("HI304", "Health Data Analytics", 3),
        ("HI305", "Health Information Security", 3),
        ("HI306", "Digital Health", 3),
        ("HI307", "Health Systems Management", 3),
        ("HI401", "Health Informatics Project", 3),
    ],

    "NUT": [
        ("NUT101", "Introduction to Human Nutrition", 3),
        ("NUT102", "Human Anatomy and Physiology", 3),
        ("NUT103", "Biochemistry", 3),
        ("NUT201", "Nutritional Assessment", 3),
        ("NUT202", "Community Nutrition", 3),
        ("NUT203", "Clinical Nutrition", 3),
        ("NUT204", "Maternal and Child Nutrition", 3),
        ("NUT301", "Food Science", 3),
        ("NUT302", "Food Microbiology", 3),
        ("NUT303", "Public Health Nutrition", 3),
        ("NUT304", "Nutrition Epidemiology", 3),
        ("NUT305", "Therapeutic Dietetics", 3),
        ("NUT401", "Nutrition Research", 3),
        ("NUT402", "Nutrition Practicum", 3),
    ],


    # =====================================================
    # INSTITUTE OF TECHNOLOGY
    # =====================================================

    "SE": [
        ("SE101", "Introduction to Programming", 3),
        ("SE102", "Programming II", 3),
        ("SE201", "Data Structures and Algorithms", 3),
        ("SE202", "Object-Oriented Programming", 3),
        ("SE203", "Discrete Mathematics", 3),
        ("SE204", "Database Systems", 3),
        ("SE301", "Software Engineering Fundamentals", 3),
        ("SE302", "Software Requirements Engineering", 3),
        ("SE303", "Software Design and Architecture", 3),
        ("SE304", "Web Application Development", 3),
        ("SE305", "Mobile Application Development", 3),
        ("SE306", "Software Testing", 3),
        ("SE307", "Software Project Management", 3),
        ("SE308", "DevOps", 3),
        ("SE309", "Artificial Intelligence", 3),
        ("SE310", "Software Security", 3),
        ("SE401", "Senior Software Project", 3),
    ],

    "IT": [
        ("IT101", "Introduction to Information Technology", 3),
        ("IT102", "Programming Fundamentals", 3),
        ("IT201", "Data Structures", 3),
        ("IT202", "Database Systems", 3),
        ("IT203", "Computer Networks", 3),
        ("IT204", "Network Administration", 3),
        ("IT301", "Operating Systems", 3),
        ("IT302", "Linux Administration", 3),
        ("IT303", "Web Technologies", 3),
        ("IT304", "Information Security", 3),
        ("IT305", "Cloud Computing", 3),
        ("IT306", "IT Project Management", 3),
        ("IT307", "Systems Administration", 3),
        ("IT308", "IT Infrastructure", 3),
        ("IT401", "IT Support and Service Management", 3),
        ("IT402", "IT Capstone Project", 3),
    ],

    "CE": [
        ("CE101", "Engineering Mathematics I", 3),
        ("CE102", "Engineering Mathematics II", 3),
        ("CE103", "Engineering Physics", 3),
        ("CE104", "Engineering Drawing", 3),
        ("CE201", "Engineering Mechanics", 3),
        ("CE202", "Strength of Materials", 3),
        ("CE203", "Fluid Mechanics", 3),
        ("CE204", "Surveying", 3),
        ("CE301", "Structural Analysis", 3),
        ("CE302", "Reinforced Concrete Design", 3),
        ("CE303", "Steel Structures", 3),
        ("CE304", "Geotechnical Engineering", 3),
        ("CE305", "Transportation Engineering", 3),
        ("CE306", "Hydraulics", 3),
        ("CE307", "Construction Management", 3),
        ("CE308", "Environmental Engineering", 3),
        ("CE401", "Civil Engineering Project", 3),
    ],

    "ECE": [
        ("ECE101", "Engineering Mathematics I", 3),
        ("ECE102", "Engineering Mathematics II", 3),
        ("ECE103", "Engineering Physics", 3),
        ("ECE201", "Circuit Theory", 3),
        ("ECE202", "Digital Logic Design", 3),
        ("ECE203", "Electronics I", 3),
        ("ECE204", "Electronics II", 3),
        ("ECE301", "Electrical Machines", 3),
        ("ECE302", "Signals and Systems", 3),
        ("ECE303", "Microprocessors", 3),
        ("ECE304", "Embedded Systems", 3),
        ("ECE305", "Control Systems", 3),
        ("ECE306", "Communication Systems", 3),
        ("ECE307", "Power Systems", 3),
        ("ECE308", "Computer Architecture", 3),
        ("ECE401", "Computer Networks", 3),
        ("ECE402", "Electrical Engineering Project", 3),
    ],

    "ME": [
        ("ME101", "Engineering Mathematics I", 3),
        ("ME102", "Engineering Mathematics II", 3),
        ("ME103", "Engineering Physics", 3),
        ("ME104", "Engineering Drawing", 3),
        ("ME201", "Engineering Mechanics", 3),
        ("ME202", "Thermodynamics I", 3),
        ("ME203", "Thermodynamics II", 3),
        ("ME204", "Fluid Mechanics", 3),
        ("ME301", "Heat Transfer", 3),
        ("ME302", "Materials Science", 3),
        ("ME303", "Manufacturing Processes", 3),
        ("ME304", "Machine Design", 3),
        ("ME305", "Mechanical Vibrations", 3),
        ("ME306", "Control Systems", 3),
        ("ME307", "Mechatronics", 3),
        ("ME308", "Industrial Engineering", 3),
        ("ME401", "Mechanical Engineering Project", 3),
    ],

    "CHE": [
        ("CHE101", "Engineering Mathematics", 3),
        ("CHE102", "General Chemistry", 3),
        ("CHE103", "Physical Chemistry", 3),
        ("CHE201", "Material and Energy Balances", 3),
        ("CHE202", "Fluid Mechanics", 3),
        ("CHE203", "Heat Transfer", 3),
        ("CHE204", "Mass Transfer", 3),
        ("CHE301", "Thermodynamics", 3),
        ("CHE302", "Chemical Reaction Engineering", 3),
        ("CHE303", "Process Control", 3),
        ("CHE304", "Process Design", 3),
        ("CHE305", "Chemical Engineering Laboratory", 3),
        ("CHE306", "Transport Phenomena", 3),
        ("CHE307", "Petroleum and Petrochemical Engineering", 3),
        ("CHE308", "Environmental Engineering", 3),
        ("CHE401", "Chemical Engineering Project", 3),
    ],

    "IE": [
        ("IE101", "Engineering Mathematics", 3),
        ("IE102", "Engineering Statistics", 3),
        ("IE103", "Engineering Economics", 3),
        ("IE201", "Operations Research", 3),
        ("IE202", "Production Systems", 3),
        ("IE203", "Manufacturing Processes", 3),
        ("IE204", "Quality Control", 3),
        ("IE301", "Industrial Organization", 3),
        ("IE302", "Supply Chain Management", 3),
        ("IE303", "Inventory Management", 3),
        ("IE304", "Work Study", 3),
        ("IE305", "Operations Management", 3),
        ("IE306", "Simulation", 3),
        ("IE307", "Optimization", 3),
        ("IE308", "Project Management", 3),
        ("IE401", "Industrial Engineering Project", 3),
    ],

    "ARCH": [
        ("ARCH101", "Architectural Design I", 3),
        ("ARCH102", "Architectural Design II", 3),
        ("ARCH103", "Architectural Graphics", 3),
        ("ARCH201", "History of Architecture", 3),
        ("ARCH202", "Building Construction", 3),
        ("ARCH203", "Building Materials", 3),
        ("ARCH204", "Structural Systems", 3),
        ("ARCH301", "Environmental Design", 3),
        ("ARCH302", "Urban Design", 3),
        ("ARCH303", "Landscape Architecture", 3),
        ("ARCH304", "Computer-Aided Design", 3),
        ("ARCH305", "Building Services", 3),
        ("ARCH306", "Sustainable Architecture", 3),
        ("ARCH401", "Professional Practice", 3),
        ("ARCH402", "Architectural Design Project", 3),
    ],

    "CTM": [
        ("CTM101", "Construction Materials", 3),
        ("CTM102", "Construction Methods", 3),
        ("CTM103", "Engineering Drawing", 3),
        ("CTM104", "Surveying", 3),
        ("CTM201", "Building Construction", 3),
        ("CTM202", "Construction Estimating", 3),
        ("CTM203", "Quantity Surveying", 3),
        ("CTM301", "Construction Planning", 3),
        ("CTM302", "Construction Project Management", 3),
        ("CTM303", "Construction Contracts", 3),
        ("CTM304", "Construction Safety", 3),
        ("CTM305", "Structural Fundamentals", 3),
        ("CTM306", "Construction Economics", 3),
        ("CTM307", "Building Services", 3),
        ("CTM401", "Construction Technology Project", 3),
    ],
}


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

db = sqlite3.connect(DB_NAME)

cursor = db.cursor()

print("=" * 60)
print("QINBIR COURSE CATALOG SEED")
print("=" * 60)


# ---------------------------------------------------------
# CHECK PROGRAMS
# ---------------------------------------------------------

programs = cursor.execute(
    "SELECT id, name, code FROM programs ORDER BY id"
).fetchall()

program_by_code = {
    code: {
        "id": program_id,
        "name": name
    }
    for program_id, name, code in programs
}

print(f"\nPrograms found in database: {len(programs)}")


# ---------------------------------------------------------
# DELETE OLD TEMPORARY COURSE
# ---------------------------------------------------------

old_course = cursor.execute(
    "SELECT id FROM courses WHERE code = 'math01'"
).fetchone()

if old_course:

    old_course_id = old_course[0]

    cursor.execute(
        "DELETE FROM program_courses WHERE course_id = ?",
        (old_course_id,)
    )

    cursor.execute(
        "DELETE FROM courses WHERE id = ?",
        (old_course_id,)
    )

    print("\nRemoved temporary course: math01")


# ---------------------------------------------------------
# SHARED COURSES
# ---------------------------------------------------------

shared_courses = [
    (
        "MATH101",
        "Calculus I",
        3,
        ["CS", "IS", "MATH", "STAT", "PHY", "SE", "IT"]
    ),
    (
        "MATH102",
        "Calculus II",
        3,
        ["CS", "IS", "MATH", "STAT", "PHY", "SE", "IT"]
    ),
    (
        "CS101",
        "Introduction to Programming",
        3,
        ["CS", "SE"]
    ),
    (
        "CS201",
        "Data Structures and Algorithms",
        3,
        ["CS", "SE"]
    ),
    (
        "CS202",
        "Object-Oriented Programming",
        3,
        ["CS", "SE"]
    ),
    (
        "CS301",
        "Database Systems",
        3,
        ["CS", "IS", "SE", "IT", "HI"]
    ),
    (
        "CS303",
        "Computer Networks",
        3,
        ["CS", "IT", "ECE"]
    ),
    (
        "CHEM101",
        "General Chemistry I",
        3,
        ["CHEM"]
    ),
]


# ---------------------------------------------------------
# CREATE COURSES
# ---------------------------------------------------------

created_courses = 0
existing_courses = 0
relationships_created = 0


def create_course(code, name, credit_hours):

    global created_courses
    global existing_courses

    existing = cursor.execute(
        "SELECT id FROM courses WHERE code = ?",
        (code,)
    ).fetchone()

    if existing:
        existing_courses += 1
        return existing[0]

    cursor.execute(
        """
        INSERT INTO courses
        (code, name, credit_hours)
        VALUES (?, ?, ?)
        """,
        (code, name, credit_hours)
    )

    created_courses += 1

    return cursor.lastrowid


def connect_course_to_program(course_id, program_code):

    global relationships_created

    program = program_by_code.get(program_code)

    if not program:
        print(
            f"WARNING: Program {program_code} "
            f"was not found."
        )
        return

    program_id = program["id"]

    existing = cursor.execute(
        """
        SELECT id
        FROM program_courses
        WHERE program_id = ?
        AND course_id = ?
        """,
        (program_id, course_id)
    ).fetchone()

    if existing:
        return

    cursor.execute(
        """
        INSERT INTO program_courses
        (program_id, course_id)
        VALUES (?, ?)
        """,
        (program_id, course_id)
    )

    relationships_created += 1


# ---------------------------------------------------------
# INSERT SHARED COURSES
# ---------------------------------------------------------

print("\nAdding shared courses...")

for code, name, credit_hours, program_codes in shared_courses:

    course_id = create_course(
        code,
        name,
        credit_hours
    )

    for program_code in program_codes:

        connect_course_to_program(
            course_id,
            program_code
        )


# ---------------------------------------------------------
# INSERT PROGRAM-SPECIFIC COURSES
# ---------------------------------------------------------

print("Adding program-specific courses...")

for program_code, courses in course_catalog.items():

    if program_code not in program_by_code:

        print(
            f"WARNING: Program {program_code} "
            f"does not exist in database."
        )

        continue

    for code, name, credit_hours in courses:

        course_id = create_course(
            code,
            name,
            credit_hours
        )

        connect_course_to_program(
            course_id,
            program_code
        )


# ---------------------------------------------------------
# COMMIT
# ---------------------------------------------------------

db.commit()


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

total_courses = cursor.execute(
    "SELECT COUNT(*) FROM courses"
).fetchone()[0]

total_relationships = cursor.execute(
    "SELECT COUNT(*) FROM program_courses"
).fetchone()[0]

print("\n" + "=" * 60)
print("COURSE SEED COMPLETE")
print("=" * 60)

print(f"Programs:              {len(programs)}")
print(f"Courses created:       {created_courses}")
print(f"Existing courses:      {existing_courses}")
print(f"Total courses:         {total_courses}")
print(f"Program relationships: {total_relationships}")


# ---------------------------------------------------------
# PROGRAM SUMMARY
# ---------------------------------------------------------

print("\nCOURSES PER PROGRAM")
print("-" * 60)

for program_id, program_name, program_code in programs:

    count = cursor.execute(
        """
        SELECT COUNT(*)
        FROM program_courses
        WHERE program_id = ?
        """,
        (program_id,)
    ).fetchone()[0]

    print(
        f"{program_code:8} "
        f"{program_name:45} "
        f"{count:3} courses"
    )


# ---------------------------------------------------------
# CLOSE
# ---------------------------------------------------------

db.close()

print("\nDatabase connection closed.")
print("QINBIR course catalog is ready.")