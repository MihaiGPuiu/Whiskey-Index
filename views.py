from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import pandas as pd
from django.shortcuts import render

def home(request):
    # Render the homepage template without any additional data
    return render(request, "whiskey_list.html")


#def whiskey_list(request):

    ua = UserAgent()
    random_user_agent = ua.random
    HEADERS = {
        'user-agent': ua.random
    }

    def scraper_finebar(url):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            whiskey_name_tags = soup.find_all("div", class_="woocommerce-loop-product__title")
            name_list = []
            for tag in whiskey_name_tags:
                name = tag.get_text(strip=True)
                if not (name.endswith(("0.05L", "0.5L", "Pahare", "1L", "1.0L", "3L", "1.5L", "0.35L", "200 ml")) or name.startswith(("Set", "Pachet"))):
                    name_list.append(name)
            return name_list
        else:
            print("Error occurred:", response.status_code)
            return None

    def scrape_multiple_pages(base_url, num_pages):
        all_whiskey_names = []
        for page_num in range(1, num_pages + 1):
            url = f"{base_url}/{page_num}?_attribute_tara=scotia"
            whiskey_names = scraper_finebar(url)
            if whiskey_names is not None:
                all_whiskey_names.extend(whiskey_names)
        return all_whiskey_names

    url = "https://www.finebar.ro/whisky-single-malt/page"
    num_pages = 2
    whiskey_names = scrape_multiple_pages(url, num_pages)

    # Create a DataFrame from the list of whiskey names
    df = pd.DataFrame(whiskey_names, columns=["Whiskey Name"])

    # Save the DataFrame to an Excel file
    df.to_excel("whiskey_names.xlsx", index=False)

    # Pass the whiskey names to the template for rendering
    return render(request, "whiskey_list.html", {"whiskey_names": whiskey_names})

from collections import defaultdict

from django.shortcuts import render
import pandas as pd
from collections import defaultdict

from collections import defaultdict
from django.shortcuts import render
import pandas as pd

def whiskey_list(request):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel("whiskey_names.xlsx")

        # Get the search query from the request
        query = request.GET.get('query')

        # If there's a search query, filter the whiskeys based on it
        if query:
            filtered_df = df[df["Whiskey Name"].str.contains(query, case=False, na=False)]
            whiskey_names = filtered_df["Whiskey Name"].tolist()
            if not whiskey_names:
                no_results_message = f"Nu s-a gasit nimic pentru  '{query}'"
            else:
                no_results_message = None
        else:
            whiskey_names = df["Whiskey Name"].tolist()
            no_results_message = None

        # Organize whiskey names alphabetically
        whiskey_names.sort()

        # Group whiskey names by their first letter
        whiskey_dict = defaultdict(list)
        for whiskey in whiskey_names:
            first_letter = whiskey[0].upper()
            whiskey_dict[first_letter].append(whiskey)

        # Sort the whiskey dictionary by keys (A-Z)
        sorted_whiskey_dict = dict(sorted(whiskey_dict.items()))

        # Pass the sorted whiskey dictionary and no results message to the template context
        return render(request, "whiskey_list.html", {
            "whiskey_dict": sorted_whiskey_dict, 
            "query": query, 
            "no_results_message": no_results_message
        })
    except Exception as e:
        # Handle the exception if the file doesn't exist or there's any other issue
        return render(request, "whiskey_list.html", {"whiskey_dict": {}, "error_message": str(e)})


import os
import random

def whiskey_of_the_day(request):
    try:
        query = request.GET.get('query')
        
        # If there's a search query, filter the whiskeys based on it
        if query:
            filtered_whiskeys = Whiskey.objects.filter(name__icontains=query)
            # Convert filtered_whiskeys queryset to list of whiskey names
            whiskey_names = [whiskey.name for whiskey in filtered_whiskeys]
        else:
        # List all files in the folder containing downloaded images
            image_folder = r"C:\Users\savai\Whiskey pictures\whiskey_images"
            image_files = os.listdir(image_folder)
            whiskey_names = [os.path.splitext(image)[0] for image in image_files]

        # Select a random whiskey name from the list
        random_whiskey_name = random.choice(whiskey_names)

        # Construct the URL of the random image
        picture_url = os.path.join(image_folder, f"{random_whiskey_name}.jpg")  # Assuming images are jpg format

        # Pass the whiskey name and picture URL to the template
        context = {
            'whiskey_name': random_whiskey_name,
            'picture_url': picture_url,
            }

            # Select a random image file from the list
        random_image = random.choice(image_files)

            # Extract the whiskey name from the image file name
        whiskey_name, _ = os.path.splitext(random_image) 
            # Remove the file extension

            # Construct the URL of the random image
        picture_url = os.path.join(image_folder, random_image)

            # Pass the whiskey name and picture URL to the template
        context = {
                'whiskey_name': whiskey_name,
                'picture_url': picture_url,
            }

            # Render the template with the context
        return render(request, 'whiskey_of_the_day.html', context)

    except Exception as e:
        # Handle exceptions, such as folder not found or other errors
        return render(request, 'error.html', {'error_message': str(e)})
def irish(request):
    try:
        
        query = request.GET.get('query')
        
        # If there's a search query, filter the whiskeys based on it
        if query:
            filtered_whiskeys = Whiskey.objects.filter(name__icontains=query)
            # Convert filtered_whiskeys queryset to list of whiskey names
            whiskey_names = [whiskey.name for whiskey in filtered_whiskeys]
        else:
        # List all files in the folder containing downloaded images
            image_folder = r"C:\Users\savai\Whiskey pictures\irish_whiskey"
            image_files = os.listdir(image_folder)
            whiskey_names = [os.path.splitext(image)[0] for image in image_files]

        # Select a random whiskey name from the list
        random_whiskey_name = random.choice(whiskey_names)

        # Construct the URL of the random image
        picture_url = os.path.join(image_folder, f"{random_whiskey_name}.jpg")  # Assuming images are jpg format

        # Pass the whiskey name and picture URL to the template
        context = {
            'whiskey_name': random_whiskey_name,
            'picture_url': picture_url,
            }

            # Render the template with the context
        return render(request, 'irish.html', context)

    except Exception as e:
        # Handle exceptions, such as folder not found or other errors
        return render(request, 'error.html', {'error_message': str(e)})
def japanese(request):
    try:
        query = request.GET.get('query')
        
        # If there's a search query, filter the whiskeys based on it
        if query:
            filtered_whiskeys = Whiskey.objects.filter(name__icontains=query)
            # Convert filtered_whiskeys queryset to list of whiskey names
            whiskey_names = [whiskey.name for whiskey in filtered_whiskeys]
        else:
        # List all files in the folder containing downloaded images
            image_folder = r"C:\Users\savai\Whiskey pictures\japanese"
            image_files = os.listdir(image_folder)
            whiskey_names = [os.path.splitext(image)[0] for image in image_files]

        # Select a random whiskey name from the list
        random_whiskey_name = random.choice(whiskey_names)

        # Construct the URL of the random image
        picture_url = os.path.join(image_folder, f"{random_whiskey_name}.jpg")  # Assuming images are jpg format

        # Pass the whiskey name and picture URL to the template
        context = {
            'whiskey_name': random_whiskey_name,
            'picture_url': picture_url,
            }
            # Render the template with the context
        return render(request, 'japanese.html', context)

    except Exception as e:
        # Handle exceptions, such as folder not found or other errors
        return render(request, 'error.html', {'error_message': str(e)})
import os
import random
from django.shortcuts import render
from .models import Whiskey

def bourbon(request):
    try:
        # Check if a search query is present
        query = request.GET.get('query')
        
        # If there's a search query, filter the whiskeys based on it
        if query:
            filtered_whiskeys = Whiskey.objects.filter(name__icontains=query)
            # Convert filtered_whiskeys queryset to list of whiskey names
            whiskey_names = [whiskey.name for whiskey in filtered_whiskeys]
        else:
            # If no search query, list all files in the folder containing downloaded images
            image_folder = r"C:\Users\savai\Whiskey pictures\bourbon"
            image_files = os.listdir(image_folder)
            whiskey_names = [os.path.splitext(image)[0] for image in image_files]

        # Select a random whiskey name from the list
        random_whiskey_name = random.choice(whiskey_names)

        # Construct the URL of the random image
        picture_url = os.path.join(image_folder, f"{random_whiskey_name}.jpg")  # Assuming images are jpg format

        # Pass the whiskey name and picture URL to the template
        context = {
            'whiskey_name': random_whiskey_name,
            'picture_url': picture_url,
        }
        
        # Render the template with the context
        return render(request, 'bourbon.html', context)

    except Exception as e:
        # Handle exceptions, such as folder not found or other errors
        return render(request, 'error.html', {'error_message': str(e)})

    
from django.shortcuts import render
from .models import Whiskey

from django.shortcuts import render
from .models import Whiskey

def random_whiskey_search(request):
    try:
        query = request.GET.get('query')
        if query:
            # Perform case-insensitive search across name and category fields for all whiskeys
            whiskeys = Whiskey.objects.filter(name__icontains=query) | Whiskey.objects.filter(category__icontains=query)
        else:
            whiskeys = Whiskey.objects.all()

        # Group search results alphabetically
        whiskey_dict = {}
        for whiskey in whiskeys:
            first_letter = whiskey.name[0].upper()
            if first_letter not in whiskey_dict:
                whiskey_dict[first_letter] = []
            whiskey_dict[first_letter].append(whiskey.name)

        return render(request, 'whiskey_list.html', {'whiskey_dict': whiskey_dict})
    except Exception as e:
        return render(request, 'error.html', {'error_message': str(e)})
