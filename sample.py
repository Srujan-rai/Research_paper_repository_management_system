data = [(0, '1', 2024, '1', '1', '1', '1', 1.0), 
        (0, '1', 2024, '1', '1', '1', '1', 1.0), 
        (0, '1', 2024, '1', '1', '1', '1', 1.0), 
        (0, '1', 2024, '1', '1', '1', '1', 1.0)]


department_id={
    0: "AIML",
    1: "CSE",
    2: "ISE",
    3: "EC",
    4: "MECH"
}


for i, tup in enumerate(data):
    department_id_value = tup[0]
    department_name = department_id.get(department_id_value)
    modified_tup = (department_name,) + tup[1:]  
    data[i] = modified_tup  

print(data)