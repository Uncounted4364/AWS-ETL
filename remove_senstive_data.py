import csv

#removes the sensitve data ("name" and "card_number" from the dictionaries)                
def extract(Filename):
    with open(Filename,"r") as f:
        reader = csv.DictReader(f)
        data= list(reader)
        
        for row in data:
            del row["name"]
            del row["card_number"]
            
    return data

#To see it works as intended        
print(extract("oneders\chesterfield_25-08-2021_09-00-00.csv"))
    

            
                
                        
        
    
                
