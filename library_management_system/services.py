class PetGroomingServices:
    def __init__(self):
        self.services = {
            "1": {"name": "Bath and Brush", "description": "Basic cleaning, brushing, and drying."},
            "2": {"name": "Haircut", "description": "Trimming or cutting your pet's fur according to the desired style."},
            "3": {"name": "Nail Trimming", "description": "Trimming your pet's nails to a safe and comfortable length."},
            "4": {"name": "Ear Cleaning", "description": "Cleaning your pet's ears to remove wax and dirt."},
            "5": {"name": "Teeth Cleaning", "description": "Brushing your pet's teeth and providing dental care."},
            # Add more services as needed
        }

    def display_services(self):
        print("Available Pet Grooming Services:")
        for key, service in self.services.items():
            print(f"{key}. {service['name']}: {service['description']}")

# Example Usage
pet_grooming = PetGroomingServices()
pet_grooming.display_services()
