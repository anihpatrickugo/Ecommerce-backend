import strgen

def generate_random_reference():
    random_str =  strgen.StringGenerator("[\w\d]{12}").render()
    return random_str


generate_random_reference()