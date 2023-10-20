import pprint
import json

info_dict = {
    'Name': 'Vibhakar Solanki',
    'mail': 'solankivibhakar82@gmail.com',
    'aliases': [
        'gala',
        'gala_vs',
        'p0lygun',
    ],
    'country': 'India',
    'socials': {
        'GitHub': 'p0lygun',
        'Discord': 'gala_vs',
        'twitter': 'vibahakarsolanki',
        'linkedin': 'vibahakarsolanki'
    },
    'links': {
        'blog': 'https://stilllearning.tech',
        'portfolio': 'https://vibhakar.dev',
    },
    'projects': {
        'bfportal': 'https://bfportal.gg',
        'gametools_network': 'https://gametools.network'
    },
    'resume': 'https://drive.google.com/file/d/1NkpwiLwOf_wiNVeSPaKFKsBzwj80DA3N/view?usp=share_link',
}


def show_info():
    print(json.dumps(info_dict, indent=4))


show_info()

