
import json
#Economic Groups

# Major Advanced Economies
major_advanced_economies = ["Canada", "France", "Germany", "Italy", "Japan", "United Kingdom", "United States"]

# Other Advanced Economies
other_advanced_economies = ["Andorra", "Australia", "Czech Republic", "Denmark", 
                            "Hong Kong SAR", "Iceland", "Israel", "Republic of Korea", "Macao SAR", 
                            "New Zealand", "Norway", "Puerto Rico", "San Marino", "Singapore", "Sweden", "Switzerland", 
                            "Taiwan Province of China"]

# European Union
european_union = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", 
                  "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary",
                  "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                  "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", "Slovenia", "Spain", "Sweden"]

# ASEAN-5
asean_5 = ["Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand"]

# Euro Area
euro_area = ["Austria", "Belgium", "Croatia", "Cyprus", "Estonia", "Finland", "France", "Germany", "Greece", "Ireland",
             "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal", "Slovak Republic", 
             "Slovenia", "Spain"]

# Emerging Developing Asia
emerging_developing_asia = ["Bangladesh", "Bhutan", "Brunei Darussalam", "Cambodia", "People's Republic of China", "Fiji", "India", "Indonesia",
                            "Kiribati", "Lao P.D.R.", "Malaysia", "Maldives", "Marshall Islands", "Fed. States of Micronesia", 
                            "Mongolia", "Myanmar", "Nauru", "Nepal", "Palau", "Papua New Guinea", "Philippines", "Samoa",
                            "Solomon Islands", "Sri Lanka", "Thailand", "Timor-Leste", "Tonga", "Tuvalu", "Vanuatu",
                            "Vietnam"]

# Emerging Developing Europe
emerging_developing_europe = ["Albania", "Belarus", "Bosnia and Herzegovina", "Bulgaria", "Hungary", "Kosovo", "Moldova",
                              "Montenegro", "North Macedonia", "Poland", "Romania", "Russian Federation", "Serbia", "Republic of Türkiye", "Ukraine"]

# Latin American and Caribbean
latin_american_caribbean = ["Antigua and Barbuda", "Argentina", "Aruba", "The Bahamas", "Barbados",
                            "Belize", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Dominica", 
                            "Dominican Republic", "Ecuador", "El Salvador", "Grenada", "Guatemala", "Guyana",
                            "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", 
                            "Suriname", "Trinidad and Tobago", "Uruguay", "Venezuela"]

# Middle East and Central Asia
middle_east_central_asia = ["Afghanistan", "Algeria", "Armenia", "Azerbaijan", "Bahrain", "Djibouti", "Egypt", "Georgia",
                            "Iran", "Iraq", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyz Republic", "Lebanon", "Libya",
                            "Mauritania", "Morocco", "Oman", "Pakistan", "Qatar", "Saudi Arabia", "Somalia", "Sudan",
                            "Syria", "Tajikistan", "Tunisia", "Turkmenistan", "United Arab Emirates", "Uzbekistan", 
                            "West Bank and Gaza", "Yemen"]

# Sub-Saharan Africa
sub_saharan_africa = ["Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", 
                      "Central African Republic", "Chad", "Comoros", "Dem. Rep. of the Congo",
                      "Republic of Congo", "Côte d'Ivoire", "Equatorial Guinea", "Eritrea", "Eswatini",
                      "Ethiopia", "Gabon", "The Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho",
                      "Liberia", "Madagascar", "Malawi", "Mali", "Mauritius", "Mozambique", "Namibia", "Niger",
                      "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone",
                      "South Africa", "Republic of South Sudan", "Tanzania", "Togo", "Uganda", "Zambia", "Zimbabwe"]


economic_groups =  {'major_advanced_economies':major_advanced_economies,
    'other_advanced_economies':other_advanced_economies,
    'european_union':european_union,
    'asean_5':asean_5,
    'euro_area':euro_area,
    'emerging_developing_asia':emerging_developing_asia,
    'emerging_developing_europe':emerging_developing_europe,
    'latin_american_caribean':latin_american_caribbean,
    'middle_east_central_asia':middle_east_central_asia,
    'sub_saharan_africa':sub_saharan_africa}


#Continents and regions

africa = ['Algeria','Angola','Benin','Botswana','Burkina Faso','Burundi','Cabo Verde','Cameroon','Central African Republic',
          'Chad','Comoros','Republic of Congo','Djibouti','Egypt','Equatorial Guinea','Eritrea','Eswatini','Ethiopia',
          'Gabon','The Gambia','Ghana','Guinea','Guinea-Bissau','Kenya','Lesotho','Liberia','Libya','Madagascar',
          'Malawi','Mali','Mauritania','Mauritius','Morocco','Mozambique','Namibia','Niger','Nigeria','Rwanda','Senegal',
          'Seychelles','Sierra Leone','Somalia','South Africa','Republic of South Sudan','Sudan','Tanzania','Togo','Tunisia','Uganda',
          'Zambia','Zimbabwe']

central_asia_causasus_countries = ['Uzbekistan', 'Kazakhstan','Kyrgyz Republic', 'Tajikistan', 
                                   'Turkmenistan', 'Azerbaijan', 'Armenia', 'Georgia']

continents_regions = {'africa':africa, 'central_asia_causasus_countries':central_asia_causasus_countries}

#Groups for MICE in Neighbour imputation
group_Afghanistan = ['Afghanistan','Pakistan', 'Iran', 'Turkmenistan', 'Uzbekistan','Tajikistan']
group_Armenia = ['Armenia','Georgia', 'Azerbaijan', 'Iran','Republic of Türkiye']
group_Azerbaijan = ['Azerbaijan','Armenia', 'Georgia', 'Iran','Russian Federation']
group_Djibouti = ['Djibouti','Eritrea', 'Ethiopia','Somalia']
group_Georgia = ['Georgia', 'Armenia','Azerbaijan','Russian Federation','Republic of Türkiye']
group_Iraq = ['Iraq','Kuwait', 'Iran', 'Syria', 'Jordan','Saudi Arabia','Republic of Türkiye']
group_Kuwait = ['Kuwait','Iraq','Saudi Arabia']
group_Kazakhstan = ['Kazakhstan', 'Kyrgyz Republic', 'Uzbekistan','Turkmenistan','Russian Federation',"People's Republic of China"]
group_Kyrgyz_Republic = ['Kyrgyz Republic','Kazakhstan', 'Uzbekistan', 'Tajikistan',"People's Republic of China"]
group_Lebanon = ['Lebanon','Israel','Syria' ]
group_Mauritania = ['Mauritania','Algeria','Mali','Senegal']
group_Somalia = ['Somalia','Kenya','Ethiopia','Djibouti']
group_Syria = ['Syria','Iraq','Jordan','Lebanon','Republic of Türkiye']
group_Tajikistan = ['Tajikistan','Kyrgyz Republic', 'Afghanistan','Uzbekistan',"People's Republic of China"]
group_Turkmenistan = ['Turkmenistan','Kazakhstan','Uzbekistan', 'Afghanistan','Iran']
group_Uzbekistan = ['Uzbekistan','Kazakhstan','Kyrgyz Republic', 'Tajikistan', 'Afghanistan','Turkmenistan']
group_West_Bank = ['West Bank and Gaza','Jordan','Israel']
group_Yemen = ['Yemen','Saudi Arabia','Oman']

group_Eritrea = ['Eritrea','Ethiopia', 'Sudan', 'Djibouti']
group_Guinea_Bissau =['Guinea-Bissau','Guinea', 'Senegal']
group_Liberia =['Liberia','Guinea', 'Sierra Leone']
group_Namibia =['Namibia','Angola', 'Zambia', 'Botswana', 'South Africa']
group_Nigeria =['Nigeria','Benin','Chad', 'Niger','Cameroon']
group_Zimbabwe =['Zimbabwe','Botswana', 'Mozambique', 'South Africa', 'Zambia']
group_South_Sudan =['Republic of South Sudan','Sudan', 'Ethiopia', 'Uganda', 'Dem. Rep. of the Congo','Central African Republic']


african_groups = [
    group_Eritrea,
    group_Guinea_Bissau,
    group_Liberia,
    group_Namibia,
    group_Nigeria,
    group_Zimbabwe,
    group_South_Sudan
]

african_group_names = [
    'group_Eritrea',
    'group_Guinea_Bissau',
    'group_Liberia',
    'group_Namibia',
    'group_Nigeria',
    'group_Zimbabwe',
    'group_South_Sudan'
]

middle_east_groups = [
    group_Afghanistan,
    group_Armenia,
    group_Azerbaijan,
    group_Djibouti,
    group_Georgia,
    group_Iraq,
    group_Kuwait,
    group_Kazakhstan,
    group_Kyrgyz_Republic,
    group_Lebanon,
    group_Mauritania,
    group_Somalia,
    group_Syria,
    group_Tajikistan,
    group_Turkmenistan,
    group_Uzbekistan,
    group_West_Bank,
    group_Yemen
]

middle_east_group_names = [
    'group_Afghanistan',
    'group_Armenia',
    'group_Azerbaijan',
    'group_Djibouti',
    'group_Georgia',
    'group_Iraq',
    'group_Kuwait',
    'group_Kazakhstan',
    'group_Kyrgyz_Republic',
    'group_Lebanon',
    'group_Mauritania',
    'group_Somalia',
    'group_Syria',
    'group_Tajikistan',
    'group_Turkmenistan',
    'group_Uzbekistan',
    'group_West_Bank',
    'group_Yemen'
]

mice_groups = {'african_groups':african_groups, 'middle_east_groups':middle_east_groups, 'african_group_names':african_group_names,
              'middle_east_group_names':middle_east_group_names}

#Groups of countries with missing data

missing_african_countries = ['Eritrea',
    'Guinea-Bissau',
    'Liberia',
    'Namibia',
    'Nigeria',
    'Zimbabwe',
    'Republic of South Sudan']

missing_middle_east_countries = ['Afghanistan',
'Armenia',
'Azerbaijan',
'Djibouti',
'Georgia',
'Iraq',
'Kuwait',
'Kazakhstan',
'Kyrgyz Republic',
'Lebanon',
'Mauritania',
'Somalia',
'Syria',
'Tajikistan',
'Turkmenistan',
'Uzbekistan',
'West Bank and Gaza',
'Yemen']

remaining_missing_countries = {
'other_advanced_economies':
    ['Andorra',                     
'Czech Republic',              
'Macao SAR',                   
'Puerto Rico',                 
'San Marino'],
    
'euro_area':
    ['Croatia',          
'Estonia',         
'Latvia',
'Netherlands',
'Lithuania',       
'Slovak Republic', 
'Slovenia'],
    
'emerging_developing_asia':
    ['Bangladesh',           
'Brunei Darussalam',    
'Cambodia',             
'Marshall Islands',
'Fed. States of Micronesia',
'Myanmar',
'Sri Lanka',             
'Nauru',                
'Palau',                
'Timor-Leste',          
'Tuvalu'],
    
'latin_american_caribean':
    ['Aruba',
'Venezuela'],
    
'emerging_developing_europe':
    ['Belarus',               
'Bosnia and Herzegovina',
'Kosovo',                
'Moldova',
'North Macedonia',
'Montenegro',            
'Serbia',
'Russian Federation',
'Ukraine']
}


missing_countries = {'missing_african_countries':missing_african_countries,'missing_middle_east_countries':missing_middle_east_countries,
                     'remaining_missing_countries':remaining_missing_countries}

with open("json_files/mice_groups.json", "w") as outfile:
    json.dump(mice_groups, outfile)

with open("json_files/economic_groups.json", "w") as outfile:
    json.dump(economic_groups, outfile)

with open("json_files/continents_regions.json", "w") as outfile:
    json.dump(continents_regions, outfile)

with open("json_files/missing_countries.json", "w") as outfile:
    json.dump(missing_countries, outfile)

